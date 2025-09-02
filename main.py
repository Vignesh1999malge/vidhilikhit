from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

from db import engine, get_db
from models import Base, User
from schemas import UserCreate, User as UserSchema, Token, Login, Message
from functions import (
    get_password_hash, 
    authenticate_user, 
    create_access_token, 
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Auth System", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main HTML page."""
    with open("templates/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/api")
async def api_root():
    """API root endpoint."""
    return {"message": "Welcome to FastAPI Auth System"}

@app.post("/register", response_model=UserSchema)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if user already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=400, 
            detail="Email already registered"
        )
    
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=400, 
            detail="Username already taken"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """Login and get access token."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserSchema)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user information."""
    return current_user

@app.get("/users", response_model=List[UserSchema])
async def read_users(
    skip: int = 0, 
    limit: int = 100, 
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get list of users (requires authentication)."""
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.put("/users/me", response_model=UserSchema)
async def update_user(
    user_update: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user information."""
    for field, value in user_update.items():
        if field == "password" and value:
            value = get_password_hash(value)
        if hasattr(current_user, field):
            setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user

@app.delete("/users/me", response_model=Message)
async def delete_user(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete current user account."""
    db.delete(current_user)
    db.commit()
    return {"message": "User account deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
