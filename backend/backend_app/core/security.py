import bcrypt

# ----------------- HASH PASSWORD -----------------
def hash_password(password: str) -> str:
    """Hash mật khẩu bằng bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    """Kiểm tra mật khẩu có khớp với hash hay không"""
    return bcrypt.checkpw(password.encode(), hashed.encode())
