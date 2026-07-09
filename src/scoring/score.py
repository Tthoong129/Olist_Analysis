import sys
import time
from pathlib import Path
from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.ingestion.logger import setup_logger
from src.ingestion.load import get_engine, test_db

logger = setup_logger()

def execute_sql_file(engine, sql_path):
    logger.info(f"Đang chạy: {sql_path.name}")
    with open(sql_path, "r", encoding="utf-8") as f:
        sql = f.read()
    with engine.begin() as conn:
        conn.execute(text(sql))

def run():
    start = time.time()
    logger.info("="*40)
    logger.info(" PIPELINE TẦNG GOLD")
    logger.info("="*40)
    
    engine = get_engine()
    if not test_db(engine):
        sys.exit(1)
        
    sql_dir = Path(__file__).resolve().parent / "sql"
    sql_files = sorted(sql_dir.glob("*.sql"))
    
    if not sql_files:
        logger.error("Không tìm thấy file SQL.")
        sys.exit(1)
        
    for sql_file in sql_files:
        execute_sql_file(engine, sql_file)
        
    with engine.begin() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM gold.seller_churn")).scalar()
        logger.info(f"Đã tạo bảng Gold: chấm điểm {count:,} sellers.")
        
        logger.info("Đang làm mới Materialized View...")
        conn.execute(text("REFRESH MATERIALIZED VIEW gold.seller_churn_mv"))
        
    logger.info(f"CHẤM ĐIỂM HOÀN TẤT trong {time.time()-start:.1f}s")
    logger.info("="*40)
    return 0

if __name__ == "__main__":
    sys.exit(run())
