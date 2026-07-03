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
    logger.info(f"Đang chạy file SQL: {sql_path.name}...")
    with open(sql_path, "r", encoding="utf-8") as f:
        sql_commands = f.read()
    
    with engine.begin() as conn:
        conn.execute(text(sql_commands))
    logger.info("Chạy SQL thành công.")

def validate_silver_tables(engine):
    logger.info("Kiểm tra dữ liệu tầng Silver...")
    tables = [
        "orders", "order_items", "order_reviews", 
        "sellers", "products", "orders_master"
    ]
    
    with engine.connect() as conn:
        for table in tables:
            query = f"SELECT COUNT(*) FROM silver.{table}"
            count = conn.execute(text(query)).scalar()
            logger.info(f"Bảng silver.{table}: {count:,} dòng")
        
        logger.info("Kiểm tra giá trị NULL trong bảng orders_master...")
        cols_to_check = ["order_id", "product_id", "seller_id", "price_usd"]
        
        total_query = "SELECT COUNT(*) FROM silver.orders_master"
        total_rows = conn.execute(text(total_query)).scalar()
        
        if total_rows > 0:
            for col in cols_to_check:
                null_query = f"SELECT COUNT(*) FROM silver.orders_master WHERE {col} IS NULL"
                null_count = conn.execute(text(null_query)).scalar()
                null_pct = (null_count / total_rows) * 100
                if null_pct > 0:
                    logger.warning(f"  - {col}: {null_count:,} dòng NULL ({null_pct:.2f}%)")
                else:
                    logger.info(f"  - {col}: Sạch (0 NULL) ✓")
        else:
            logger.warning("Bảng orders_master trống!")

def run():
    start = time.time()
    logger.info("="*40)
    logger.info(" PIPELINE TẦNG SILVER")
    logger.info("="*40)
    
    engine = get_engine()
    if not test_db(engine):
        logger.error("Không kết nối được DB.")
        sys.exit(1)
        
    sql_path = Path(__file__).resolve().parent / "silver_transform.sql"
    if not sql_path.exists():
        logger.error(f"Không tìm thấy file SQL: {sql_path}")
        sys.exit(1)
        
    try:
        execute_sql_file(engine, sql_path)
        validate_silver_tables(engine)
    except Exception as e:
        logger.error(f"Quá trình Transform lỗi: {e}")
        sys.exit(1)
        
    duration = time.time() - start
    logger.info("="*40)
    logger.info(f" TRANSFORMATION HOÀN TẤT trong {duration:.1f}s")
    logger.info("="*40)

if __name__ == "__main__":
    run()
