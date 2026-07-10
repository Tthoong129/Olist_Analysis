import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.ingestion.logger import setup_logger
from src.ingestion.validate import validate_files
from src.ingestion.exchange import get_rate, rate_to_df
from src.ingestion.load import get_engine, test_db, load_all, load_df
from src.ingestion.download_data import prep_data, get_data_dir
from src.transformation.transform import run as run_silver_transform
from src.scoring.score import run as run_gold_scoring

logger = setup_logger()

FILE_MAPPING = {
    "olist_orders_dataset.csv": "orders",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "olist_customers_dataset.csv": "customers",
    "olist_geolocation_dataset.csv": "geolocation",
    "product_category_name_translation.csv": "product_category_translation"
}

def run():
    start = time.time()
    logger.info("Bắt đầu chạy pipeline Ingestion...")
    
    if not prep_data():
        logger.error("Lỗi chuẩn bị dữ liệu.")
        sys.exit(1)
        
    engine = get_engine()
    if not test_db(engine):
        logger.error("Không thể kết nối Database.")
        sys.exit(1)
        
    data = validate_files(get_data_dir(), FILE_MAPPING)
    
    logger.info("Call API lấy tỷ giá...")
    rate_info = get_rate("USD")
    
    logger.info("Load dữ liệu vào Postgres...")
    loaded = load_all(engine, data)
    
    try:
        loaded["exchange_rates"] = load_df(engine, rate_to_df(rate_info), "exchange_rates")
    except Exception as e:
        logger.error(f"Lỗi load bảng tỷ giá: {e}")
        
    skipped = [k for k, v in data.items() if not v[0]]
    duration = time.time() - start
    
    logger.info("="*40)
    logger.info(" PIPELINE HOÀN TẤT")
    logger.info(f" Load thành công : {len(loaded)} bảng ({sum(loaded.values()):,} rows)")
    logger.info(f" Bỏ qua          : {len(skipped)} bảng")
    logger.info(f" Tỷ giá          : {rate_info['rate']} USD/BRL")
    logger.info(f" Tổng thời gian  : {duration:.1f}s")
    logger.info("="*40)
    
    # Chạy Transform & Scoring nếu Bronze thành công
    if not skipped:
        logger.info("\nBắt đầu chạy Silver Transform...")
        try:
            silver_status = run_silver_transform()
            if silver_status != 1:  
                logger.info("\nBắt đầu chạy Gold Scoring...")
                run_gold_scoring()
        except Exception as e:
            logger.error(f"Lỗi quá trình Transform/Scoring: {e}")
            return 1
            
    return 0 if not skipped else 1

if __name__ == "__main__":
    sys.exit(run())
