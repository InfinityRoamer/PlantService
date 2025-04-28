from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.common.db import get_db
from app.modules.models import User
from app.modules.schemas.users import UserResponse


router = APIRouter(prefix='/users')


@router.get('/', response_model=list[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users if users else 'No users registered.'
