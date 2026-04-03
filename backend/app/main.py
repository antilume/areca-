from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api import router as api_router
from app.core.database import Base, engine
from app.models import models
import os
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Database Schema
try:
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialization successful.")
except Exception as e:
    logger.error(f"Error initializing database: {e}")

app = FastAPI(title="Startup Hiring Intelligence Copilot")

app.include_router(api_router, prefix="/api")

# Serve static files and frontend
static_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def read_index():
    index_file = os.path.join(static_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"status": "error", "message": "index.html not found"}

@app.get("/health")
def health():
    return {"status": "ok"}
