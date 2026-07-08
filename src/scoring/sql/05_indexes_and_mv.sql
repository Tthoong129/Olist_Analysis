CREATE INDEX IF NOT EXISTS idx_seller_churn_score ON gold.seller_churn(churn_risk_score DESC);
CREATE INDEX IF NOT EXISTS idx_seller_churn_label ON gold.seller_churn(risk_label);
CREATE INDEX IF NOT EXISTS idx_seller_churn_state ON gold.seller_churn(seller_state);

DROP MATERIALIZED VIEW IF EXISTS gold.seller_churn_mv;
CREATE MATERIALIZED VIEW gold.seller_churn_mv AS
SELECT * FROM gold.seller_churn;

CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_seller_id ON gold.seller_churn_mv(seller_id);
