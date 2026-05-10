from app.database import SessionLocal
from app.models import User, Consumption

db = SessionLocal()

db.query(Consumption).delete()
db.query(User).delete()

db.commit()
db.close()

print("Tables cleared successfully!")