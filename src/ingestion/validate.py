from pathlib import Path
import pandas as pd
import great_expectations as gx
from great_expectations.core.expectation_configuration import ExpectationConfiguration
from src.ingestion.logger import setup_logger

logger = setup_logger()

VALID_STATUSES = ["created", "approved", "invoiced", "processing", "shipped", "delivered", "unavailable", "canceled"]

EXPECTATIONS = {
    "orders": [
        ExpectationConfiguration(expectation_type="expect_column_to_exist", kwargs={"column": "order_id"}),
        ExpectationConfiguration(expectation_type="expect_column_to_exist", kwargs={"column": "customer_id"}),
        ExpectationConfiguration(expectation_type="expect_column_to_exist", kwargs={"column": "order_status"}),
        ExpectationConfiguration(expectation_type="expect_column_values_to_not_be_null", kwargs={"column": "order_id"}),
        ExpectationConfiguration(expectation_type="expect_column_values_to_be_unique", kwargs={"column": "order_id"}),
        ExpectationConfiguration(expectation_type="expect_column_values_to_be_in_set", kwargs={"column": "order_status", "value_set": VALID_STATUSES}),
        ExpectationConfiguration(expectation_type="expect_table_row_count_to_be_between", kwargs={"min_value": 1})
    ],
    "order_items": [
        ExpectationConfiguration(expectation_type="expect_column_to_exist", kwargs={"column": "order_id"}),
        ExpectationConfiguration(expectation_type="expect_column_to_exist", kwargs={"column": "seller_id"}),
        ExpectationConfiguration(expectation_type="expect_column_to_exist", kwargs={"column": "price"}),
        ExpectationConfiguration(expectation_type="expect_column_values_to_not_be_null", kwargs={"column": "order_id"}),
        ExpectationConfiguration(expectation_type="expect_column_values_to_not_be_null", kwargs={"column": "seller_id"}),
        ExpectationConfiguration(expectation_type="expect_column_values_to_be_between", kwargs={"column": "price", "min_value": 0, "strict_min": True}),
        ExpectationConfiguration(expectation_type="expect_table_row_count_to_be_between", kwargs={"min_value": 1})
    ],
    "order_reviews": [
        ExpectationConfiguration(expectation_type="expect_column_to_exist", kwargs={"column": "review_id"}),
        ExpectationConfiguration(expectation_type="expect_column_to_exist", kwargs={"column": "review_score"}),
        ExpectationConfiguration(expectation_type="expect_column_values_to_not_be_null", kwargs={"column": "review_id"}),
        ExpectationConfiguration(expectation_type="expect_column_values_to_be_between", kwargs={"column": "review_score", "min_value": 1, "max_value": 5}),
        ExpectationConfiguration(expectation_type="expect_table_row_count_to_be_between", kwargs={"min_value": 1})
    ],
    "sellers": [
        ExpectationConfiguration(expectation_type="expect_column_to_exist", kwargs={"column": "seller_id"}),
        ExpectationConfiguration(expectation_type="expect_column_values_to_not_be_null", kwargs={"column": "seller_id"}),
        ExpectationConfiguration(expectation_type="expect_column_values_to_be_unique", kwargs={"column": "seller_id"}),
        ExpectationConfiguration(expectation_type="expect_table_row_count_to_be_between", kwargs={"min_value": 1})
    ],
    "products": [
        ExpectationConfiguration(expectation_type="expect_column_to_exist", kwargs={"column": "product_id"}),
        ExpectationConfiguration(expectation_type="expect_column_values_to_not_be_null", kwargs={"column": "product_id"}),
        ExpectationConfiguration(expectation_type="expect_column_values_to_be_unique", kwargs={"column": "product_id"}),
        ExpectationConfiguration(expectation_type="expect_table_row_count_to_be_between", kwargs={"min_value": 1})
    ]
}

def validate_df(df, name):
    suite_rules = EXPECTATIONS.get(name)
    if not suite_rules:
        return True, len(df), []
        
    try:
        ctx = gx.get_context(mode="ephemeral")
        ds = ctx.sources.add_pandas(f"ds_{name}")
        asset = ds.add_dataframe_asset(name=f"{name}_asset")
        batch_req = asset.build_batch_request(dataframe=df)
        
        suite = ctx.add_expectation_suite(f"{name}_suite")
        for config in suite_rules:
            suite.add_expectation(config)
        ctx.save_expectation_suite(suite)
        
        checkpoint = ctx.add_or_update_checkpoint(
            name=f"{name}_checkpoint",
            validations=[{"batch_request": batch_req, "expectation_suite_name": f"{name}_suite"}]
        )
        
        result = checkpoint.run()
        if result.success:
            logger.info(f"Kiểm tra {name}: ĐẠT")
            return True, len(df), []
            
        failures = []
        for run_res in result.run_results.values():
            for res in run_res["validation_result"]["results"]:
                if not res["success"]:
                    config = res["expectation_config"]
                    col = config["kwargs"].get("column", "table")
                    failures.append(f"{config['type']} lỗi ở {col}")
                    
        logger.error(f"Kiểm tra {name}: LỖI")
        for f in failures:
            logger.error(f"  ✗ {f}")
        return False, len(df), failures
    except Exception as e:
        logger.error(f"Lỗi hệ thống khi kiểm tra {name}: {e}")
        return True, len(df), [str(e)]

def validate_files(data_dir, mapping):
    results = {}
    for csv_file, name in mapping.items():
        path = data_dir / csv_file
        if not path.exists():
            logger.error(f"Thiếu file: {path}")
            continue
            
        df = pd.read_csv(path)
        passed, count, _ = validate_df(df, name)
        results[name] = (passed, count, df if passed else pd.DataFrame())
    return results
