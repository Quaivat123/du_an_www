# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.api import users

# ⚙️ Tạo bảng trong database nếu chưa có
Base.metadata.create_all(bind=engine)

# 🚀 Khởi tạo ứng dụng FastAPI
app = FastAPI(title="Du_An_WWW Backend")

# 🧩 Bật CORS — Cho phép FE gọi API từ domain khác
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # "*" = cho phép tất cả; khi deploy thực tế nên giới hạn
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép mọi phương thức: GET, POST, PUT, DELETE
    allow_headers=["*"],  # Cho phép mọi header
)

# 📦 Import và đăng ký router (điểm API)
app.include_router(users.router, prefix="/contacts", tags=["Contacts"])

# ✅ Route test — kiểm tra server hoạt động
@app.get("/")
def root():
    return {"message": "Du_An_WWW backend is running 🚀"}
