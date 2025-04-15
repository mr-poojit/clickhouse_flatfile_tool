from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import ingest
from fastapi.responses import JSONResponse

app = FastAPI(
    title="ClickHouse ↔ Flat File Integration Tool",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include the ingest router
app.include_router(ingest.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to the ClickHouse Integration Tool"}


@app.options("/api/connect-clickhouse")
async def options_connect_clickhouse():
    return JSONResponse(content={"ok": True}, status_code=200)

