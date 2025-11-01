# backend/main.py
# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.backend_app.database import init_db
from backend.backend_app.api import users, admin
from backend.backend_app.core.config import settings


# Đường dẫn tới project root

app = FastAPI(title=settings.PROJECT_NAME)

# Đăng ký router
app.include_router(users.router)
app.include_router(admin.router)

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
app.mount("/frontend", StaticFiles(directory=settings.STATIC_DIR, html=True), name="frontend")

# Route gốc
@app.get("/")
async def serve_index():
    return FileResponse(settings.STATIC_DIR / "ThietKeWeb.html")

@app.get("/admin")
async def serve_admin():
    return FileResponse(settings.STATIC_DIR / "admin.html")