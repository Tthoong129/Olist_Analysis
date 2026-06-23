import sys
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.ingestion.logger import setup_logger
import kagglehub

logger = setup_logger()

EXPECTED_FILES = [
    "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "product_category_name_translation.csv"
]

def get_data_dir():
    return Path(__file__).resolve().parent.parent.parent / "data" / "raw"

def check_files(data_dir):
    existing = [f for f in EXPECTED_FILES if (data_dir / f).exists()]
    missing = [f for f in EXPECTED_FILES if f not in existing]
    return existing, missing

def download_data(data_dir):
    try:
        logger.info("Đang tải data từ Kaggle...")
        cache_path = Path(kagglehub.dataset_download("olistbr/brazilian-ecommerce"))
        
        csv_files = list(cache_path.rglob("*.csv"))
        if not csv_files:
            logger.error("Không tìm thấy file CSV nào.")
            return False
            
        for f in csv_files:
            shutil.copy2(str(f), str(data_dir / f.name))
            
        logger.info(f"Đã copy {len(csv_files)} files vào {data_dir}")
        return True
    except Exception as e:
        logger.error(f"Lỗi tải data: {e}")
        return False

def prep_data():
    data_dir = get_data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)
    
    _, missing = check_files(data_dir)
    if not missing:
        logger.info("Đã có đủ các file CSV thô.")
        return True
        
    logger.info(f"Thiếu {len(missing)} files. Bắt đầu tải...")
    if download_data(data_dir):
        _, missing = check_files(data_dir)
        if not missing:
            return True
            
    print("\n" + "="*50)
    print("CẦN TẢI THỦ CÔNG:")
    print("Vào trang https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce")
    print(f"Giải nén các file CSV vào: {data_dir}")
    print("="*50 + "\n")
    return False

if __name__ == "__main__":
    prep_data()
