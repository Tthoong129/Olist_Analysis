import time
from datetime import datetime
import requests
import pandas as pd
from src.ingestion.logger import setup_logger

logger = setup_logger()

def get_rate(target="USD"):
    url = "https://api.exchangerate-api.com/v4/latest/BRL"
    for attempt in range(1, 4):
        try:
            logger.debug(f"Đang lấy tỷ giá (lần {attempt}/3)...")
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            
            rate = resp.json()["rates"].get(target)
            if rate is None:
                raise ValueError(f"Không tìm thấy tỷ giá cho {target}")
                
            return {
                "base_currency": "BRL",
                "target_currency": target,
                "rate": round(rate, 6),
                "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "is_fallback": False
            }
        except Exception as e:
            logger.warning(f"Lỗi lấy tỷ giá (lần {attempt}/3): {e}")
            if attempt < 3:
                time.sleep(5)
                
    logger.warning("API sập, dùng tỷ giá fallback 0.18")
    return {
        "base_currency": "BRL",
        "target_currency": target,
        "rate": 0.18,
        "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "is_fallback": True
    }

def rate_to_df(rate_info):
    return pd.DataFrame([rate_info])
