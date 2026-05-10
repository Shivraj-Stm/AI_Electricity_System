from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.database import engine, Base, SessionLocal
from app.models import User, Consumption

# --------------- Direct router imports -----------------------------
from app.routes.user_routes import router as user_router
from app.routes.chatbot import router as chatbot_router
from app.routes.prediction_routes import router as prediction_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#-------------------------- Include routers -----------------------------
app.include_router(user_router)
app.include_router(chatbot_router)
app.include_router(prediction_router)

Base.metadata.create_all(bind=engine)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

@app.get("/count")
def get_counts():
    db = SessionLocal()
    user_count = db.query(User).count()
    consumption_count = db.query(Consumption).count()
    db.close()

    return {
        "total_users": user_count,
        "total_consumptions": consumption_count
    }