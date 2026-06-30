import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from src.ingestion.logger import setup_logger

logger = setup_logger()
load_dotenv()

def get_engine():
    url = (
        f"postgresql://{os.getenv('POSTGRES_USER')}:"
        f"{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('POSTGRES_HOST', 'localhost')}:"
        f"{os.getenv('POSTGRES_PORT', '5432')}/"
        f"{os.getenv('POSTGRES_DB')}"
    )
    return create_engine(url)

def test_db(engine):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Kết nối Postgres: OK")
        return True
    except Exception as e:
        logger.error(f"Lỗi kết nối Postgres: {e}")
        return False

def ensure_schema(engine, schema="bronze"):
    with engine.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
        conn.commit()

def load_df(engine, df, name, schema="bronze"):
    with engine.begin() as conn:
        df.to_sql(
            name=name,
            con=conn,
            schema=schema,
            if_exists="replace",
            index=False,
            method="multi",
            chunksize=5000
        )
    
    with engine.connect() as conn:
        db_count = conn.execute(text(f"SELECT COUNT(*) FROM {schema}.{name}")).scalar()
        
    csv_count = len(df)
    if db_count == csv_count:
        logger.info(f"Đã load {schema}.{name}: {db_count:,} dòng")
    else:
        logger.warning(f"Lệch số lượng dòng {schema}.{name}: CSV={csv_count:,}, DB={db_count:,}")
    return db_count

def load_all(engine, data):
    ensure_schema(engine, "bronze")
    loaded = {}
    skipped = []
    
    for name, (passed, _, df) in data.items():
        if not passed or df.empty:
            logger.warning(f"Bỏ qua bảng {name} (dữ liệu lỗi/trống)")
            skipped.append(name)
            continue
            
        loaded[name] = load_df(engine, df, name)
        
    if skipped:
        logger.warning(f"Các bảng bị bỏ qua: {', '.join(skipped)}")
    return loaded
