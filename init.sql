-- Auto-create schemas on first container init
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

-- Grant permissions (user matches POSTGRES_USER in .env)
GRANT ALL ON SCHEMA bronze TO "olist_Kin";
GRANT ALL ON SCHEMA silver TO "olist_Kin";
GRANT ALL ON SCHEMA gold TO "olist_Kin";
