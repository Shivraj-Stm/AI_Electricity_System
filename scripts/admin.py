from app.database import SessionLocal
from app.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()

admin = User(
    acct_id="ADMIN-001",
    name="System Admin",
    address="Office",
    mobile="9999999999",
    tariff_type="ADMIN",
    s_t="HQ",
    mtr_srl_no="ADMIN-METER-001",
    load=0,
    metr_status="A",
    password=pwd_context.hash("admin123"),
    is_registered=True,
    role="admin"
)

db.add(admin)
db.commit()
db.close()

print("Admin created successfully!")