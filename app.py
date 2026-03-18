from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime
import uvicorn

# Database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    assets = relationship("Asset", back_populates="owner")

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    symbol = Column(String)
    amount = Column(Float)
    owner = relationship("User", back_populates="assets")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    date = Column(DateTime, default=datetime.utcnow)
    amount = Column(Float)
    transaction_type = Column(String)

# Create tables
Base.metadata.create_all(bind=engine)

# Seed data
def seed_data(db):
    user = User(username="demo_user", email="demo@example.com", password_hash=pwd_context.hash("password"))
    db.add(user)
    db.commit()
    db.refresh(user)
    asset = Asset(user_id=user.id, name="Bitcoin", symbol="BTC", amount=1.5)
    db.add(asset)
    db.commit()

# FastAPI app
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Dependency
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/assets", response_class=HTMLResponse)
async def read_assets(request):
    return templates.TemplateResponse("assets.html", {"request": request})

@app.get("/history", response_class=HTMLResponse)
async def read_history(request):
    return templates.TemplateResponse("history.html", {"request": request})

@app.get("/profile", response_class=HTMLResponse)
async def read_profile(request):
    return templates.TemplateResponse("profile.html", {"request": request})

@app.get("/api/assets")
async def get_assets(db: SessionLocal = Depends(get_db)):
    assets = db.query(Asset).all()
    return assets

@app.post("/api/assets")
async def add_asset(asset: Asset, db: SessionLocal = Depends(get_db)):
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset

@app.get("/api/history")
async def get_history(db: SessionLocal = Depends(get_db)):
    transactions = db.query(Transaction).all()
    return transactions

@app.post("/api/auth/login")
async def login(username: str, password: str, db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not pwd_context.verify(password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"token": "fake-token-for-now"}

@app.get("/api/profile")
async def get_profile(db: SessionLocal = Depends(get_db)):
    user = db.query(User).first()
    return user

if __name__ == "__main__":
    # Seed the database with demo data
    db = SessionLocal()
    seed_data(db)
    db.close()
    uvicorn.run(app, host="0.0.0.0", port=8000)
