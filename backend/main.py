# backend/main.py
# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from backend.backend_app import database
from backend.backend_app.database import init_db
from backend.backend_app.api import users


# Đường dẫn tới project root
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "frontend"

app = FastAPI(title="Du_An_WWW Backend")

# Đăng ký router
app.include_router(users.router)

# Khởi tạo database
@app.on_event("startup")
async def startup_event():
    await init_db()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/frontend", StaticFiles(directory=STATIC_DIR, html=True), name="frontend")

# Route gốc
@app.get("/")
async def serve_index():
    return FileResponse(STATIC_DIR / "ThietKeWeb.html")
