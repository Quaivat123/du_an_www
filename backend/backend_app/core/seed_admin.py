from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.backend_app.models.admin_model import Admin
from backend.backend_app.core.security import hash_password

# ----------------- SEED ADMIN USER -----------------
async def seed_admin(db: AsyncSession):
    result = await db.execute(select(Admin))
    if not result.scalars().first():
        admin_user = Admin(
            username="admin",
            password=hash_password("1357")  # mật khẩu mặc định
        )
        db.add(admin_user)
        await db.commit()
        print("✅ Admin account created: admin / 1357")