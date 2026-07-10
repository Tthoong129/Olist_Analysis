import sys
import os
import requests
from datetime import datetime
from pathlib import Path
from sqlalchemy import text
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from tenacity import retry, stop_after_attempt, wait_fixed

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.ingestion.logger import setup_logger
from src.ingestion.load import get_engine, test_db
from src.pipeline import run as execute_all_phases

logger = setup_logger()

# Test mode: 5s retry. Prod mode: 5 phút retry
RETRY_WAIT = 5 if "--test" in sys.argv else 300

def send_slack_alert(message):
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        return
    try:
        requests.post(webhook_url, json={"text": message}, timeout=10)
    except Exception as e:
        logger.warning(f"Lỗi gọi Slack Webhook: {e}")

@retry(stop=stop_after_attempt(3), wait=wait_fixed(RETRY_WAIT))
def run_full_pipeline():
    logger.info("Khởi động Auto Pipeline...")
    engine = get_engine()
    
    if not test_db(engine):
        raise Exception("Database sập. Hủy tiến trình.")
        
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5)
        r.raise_for_status()
    except Exception as e:
        logger.warning(f"Lỗi gọi API tỷ giá: {e}")
        
    started_at = datetime.now()
    
    # Ghi log bắt đầu chạy vào DB
    with engine.begin() as conn:
        result = conn.execute(text("""
            INSERT INTO gold.pipeline_runs (started_at, status) 
            VALUES (:start, 'RUNNING') RETURNING run_id
        """), {"start": started_at})
        run_id = result.scalar()
        
    try:
        exit_code = execute_all_phases()
        if exit_code != 0:
            raise Exception("Pipeline lỗi ở script chính.")
            
        # Refresh MV cho Power BI
        with engine.begin() as conn:
            conn.execute(text("REFRESH MATERIALIZED VIEW CONCURRENTLY gold.seller_churn_mv"))
            logger.info("Đã refresh Materialized View thành công.")
            
        with engine.begin() as conn:
            bronze = conn.execute(text("SELECT COUNT(*) FROM bronze.orders")).scalar()
            silver = conn.execute(text("SELECT COUNT(*) FROM silver.orders_master")).scalar()
            gold = conn.execute(text("SELECT COUNT(*) FROM gold.seller_churn")).scalar()
            
            conn.execute(text("""
                UPDATE gold.pipeline_runs 
                SET finished_at = :end, status = 'SUCCESS',
                    bronze_rows = :bronze, silver_rows = :silver, gold_rows = :gold
                WHERE run_id = :id
            """), {
                "end": datetime.now(), 
                "bronze": bronze, "silver": silver, "gold": gold, "id": run_id
            })
            
        logger.info(f"Pipeline Run {run_id} THÀNH CÔNG.")
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Pipeline Run {run_id} THẤT BẠI: {error_msg}")
        with engine.begin() as conn:
            conn.execute(text("""
                UPDATE gold.pipeline_runs 
                SET finished_at = :end, status = 'FAILED', error_message = :err
                WHERE run_id = :id
            """), {"end": datetime.now(), "err": error_msg, "id": run_id})
            
        send_slack_alert(f"🚨 *Pipeline Lỗi*\nRun ID: {run_id}\nTime: {datetime.now()}\nLỗi: {error_msg}")
        raise e

def main():
    if "--test" in sys.argv:
        logger.info("Chạy TEST MODE (1 lần)")
        try:
            run_full_pipeline()
        except Exception:
            pass
        sys.exit(0)
        
    scheduler = BlockingScheduler()
    scheduler.add_job(
        run_full_pipeline,
        trigger=CronTrigger(hour=6, minute=0),
        id='daily_pipeline',
        name='Daily ELT Pipeline',
        max_instances=1,
        misfire_grace_time=3600
    )
    
    logger.info("Scheduler đã bật. Chờ trigger 6:00 AM hàng ngày...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Đã tắt Scheduler.")

if __name__ == "__main__":
    main()
