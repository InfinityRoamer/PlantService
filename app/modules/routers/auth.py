from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.common.db import get_db
from app.modules.models.user import User
from app.modules.schemas.users import UserCreate, UserToken
from app.common.utils import get_password_hash, create_access_token, verify_password, TOKEN_EXPIRES

router = APIRouter()


@router.post("/registration", response_model=UserToken)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token = create_access_token(
        data={"sub": user_data.username},
        expires_delta=timedelta(minutes=TOKEN_EXPIRES)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/login", response_model=UserToken)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=TOKEN_EXPIRES)
    )
    
    return {"access_token": access_token, "token_type": "bearer"}