from fastapi import APIRouter, Depends, HTTPException, status
import sqlite3
from app.auth.database import get_db
from app.auth.schemas import UserCreate, UserLogin, Token, UserResponse
from app.auth.security import get_password_hash, verify_password, create_access_token

router = APIRouter()

@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    # Check if email exists
    cursor.execute("SELECT id FROM users WHERE email = ?", (user.email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = get_password_hash(user.password)
    try:
        cursor.execute(
            "INSERT INTO users (email, hashed_password, first_name, last_name, company) VALUES (?, ?, ?, ?, ?)",
            (user.email, hashed_pw, user.first_name, user.last_name, user.company)
        )
        db.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    access_token = create_access_token(data={"sub": user.email, "first_name": user.first_name, "last_name": user.last_name})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT email, hashed_password, first_name, last_name FROM users WHERE email = ?", (user.email,))
    row = cursor.fetchone()
    
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found. Please Sign Up.", headers={"WWW-Authenticate": "Bearer"})
    if not verify_password(user.password, row["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password", headers={"WWW-Authenticate": "Bearer"})
        
    access_token = create_access_token(data={"sub": row["email"], "first_name": row["first_name"], "last_name": row["last_name"]})
    return {"access_token": access_token, "token_type": "bearer"}


