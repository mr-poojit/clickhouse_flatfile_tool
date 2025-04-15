from clickhouse_connect import get_client
from pydantic import BaseModel

class ClickHouseConfig(BaseModel):
    host: str
    port: int
    username: str
    jwt_token: str
    database: str

def get_clickhouse_client(config: ClickHouseConfig):
    return get_client(
        host=config.host,
        port=config.port,
        username=config.username,
        password=config.jwt_token,
        database=config.database,
        secure=True if config.port in [8443, 9440] else False
    )

def test_clickhouse_connection(config: ClickHouseConfig):
    client = get_clickhouse_client(config)
    return client.query('SHOW TABLES').result_rows

def list_clickhouse_tables(config: ClickHouseConfig):
    client = get_clickhouse_client(config)
    result = client.query("SHOW TABLES").result_rows
    return [table[0] for table in result]

def get_table_columns(config: ClickHouseConfig, table_name: str):
    client = get_clickhouse_client(config)
    result = client.query(f"DESCRIBE TABLE {table_name}").result_rows
    return [{"name": row[0], "type": row[1]} for row in result]

# --- Optional: Standalone test ---
if __name__ == "__main__":
    config = ClickHouseConfig(
        host="pb4oke9od9.asia-southeast1.gcp.clickhouse.cloud",
        port=8443,
        username="default",
        jwt_token="MvV_8usOy2jE2", 
        database="default"
    )

    print("✅ Tables:", list_clickhouse_tables(config))
    print("🧱 Columns from a table:")
    if tables := list_clickhouse_tables(config):
        print(get_table_columns(config, tables[0]))
