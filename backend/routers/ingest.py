from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from clickhouse_connect import get_client
import pandas as pd
import io
import logging

# Set up logger
logger = logging.getLogger(__name__)

router = APIRouter()

# Function to get the ClickHouse client
def get_clickhouse_client(config):
    try:
        return get_client(
            host=config.host,
            port=config.port,
            username=config.username,
            password=config.jwt_token,
            database=config.database,
            secure=True if config.port in [8443, 9440] else False
        )
    except Exception as e:
        logger.error(f"Error while getting ClickHouse client: {e}")
        raise HTTPException(status_code=500, detail="Failed to connect to ClickHouse")

# ------------------------ Base Models ------------------------

class ClickHouseConfig(BaseModel):
    host: str
    port: int
    username: str
    jwt_token: str
    database: str

class TableColumnRequest(ClickHouseConfig):
    table_name: str

# ------------------------ ClickHouse Endpoints ------------------------

@router.post("/connect-clickhouse")
async def connect_clickhouse(config: ClickHouseConfig):
    try:
        client = get_clickhouse_client(config)
        tables = client.query("SHOW TABLES").result_rows
        return {"status": "success", "tables": tables}
    except Exception as e:
        logger.error(f"Error in connect-clickhouse: {e}")
        raise HTTPException(status_code=500, detail="Failed to connect to ClickHouse")

@router.post("/get-columns")
async def get_table_columns(request: TableColumnRequest):
    try:
        client = get_clickhouse_client(request)
        query = f"DESCRIBE TABLE {request.table_name}"
        result = client.query(query).result_rows
        columns = [{"name": col[0], "type": col[1]} for col in result]
        return {"columns": columns}
    except Exception as e:
        logger.error(f"Error in get-columns for table {request.table_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get columns for table {request.table_name}")

# ------------------------ CSV Upload Endpoint ------------------------

@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...), delimiter: str = Form(",")):
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")), delimiter=delimiter)

        if len(df.columns) == 1:
            df = df[df.columns[0]].str.split(",", expand=True)

        columns = list(df.columns)
        preview = df.head(5).to_dict(orient="records")

        return {
            "filename": file.filename,
            "columns": columns,
            "preview": preview
        }
    except Exception as e:
        logger.error(f"Error uploading CSV file: {e}")
        raise HTTPException(status_code=500, detail="Failed to process CSV file")

# ------------------------ Ingest CSV to ClickHouse ------------------------

@router.post("/ingest-csv-to-clickhouse")
async def ingest_csv_to_clickhouse(
    file: UploadFile = File(...),
    table_name: str = Form(...),
    delimiter: str = Form(","),
    host: str = Form(...),
    port: int = Form(...),
    username: str = Form(...),
    jwt_token: str = Form(...),
    database: str = Form(...),
):
    try:
        # Step 1: Read CSV
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")), delimiter=delimiter)

        if len(df.columns) == 1:
            df = df[df.columns[0]].str.split(",", expand=True)

        # Step 2: Connect to ClickHouse
        client = get_client(
            host=host,
            port=port,
            username=username,
            password=jwt_token,
            database=database,
            secure=True if port in [8443, 9440] else False
        )

        # Step 3: Insert data into ClickHouse
        client.insert_df(table_name, df)

        return {
            "status": "success",
            "rows_inserted": len(df),
            "table": table_name
        }
    except Exception as e:
        logger.error(f"Error ingesting CSV to ClickHouse: {e}")
        raise HTTPException(status_code=500, detail="Failed to ingest CSV data to ClickHouse")
