from pydantic_settings import BaseSettings
from pathlib import Path
class Settings(BaseSettings):
    # ----------------- Dự án -----------------
    PROJECT_NAME: str = "DACA WEB"
    ENVIRONMENT: str = "development"

    # ----------------- Đường dẫn thư mục -----------------
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent  # Lên 4 cấp để ra root project
    STATIC_DIR: Path = BASE_DIR / "frontend"

    # ----------------- Database -----------------
    DATABASE_URL: str = "mysql+aiomysql://root:namnguyenngoc2608%40@localhost:3306/new_daca"

    # ----------------- JWT & Security -----------------
    SECRET_KEY: str = "supersecretkey"  # Thay khi deploy
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 2

    class Config:
        env_file = ".env"  # Tự động đọc giá trị từ file .env nếu có

# Đối tượng cấu hình toàn cục
settings = Settings()
