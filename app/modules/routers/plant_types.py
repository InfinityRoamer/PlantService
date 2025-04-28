from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.common.db import get_db
from app.modules.models import PlantType
from app.modules.schemas.plants import PlantTypeBase, PlantTypeInDB
from app.common.utils import get_current_user
from app.modules.models import User


router = APIRouter(prefix='/plant-types')


@router.get('/')
async def get_plant_types(db: Session = Depends(get_db)):
    types = db.query(PlantType).all()
    return types if types else 'No plant types added.'


@router.post('/', response_model=PlantTypeInDB, status_code=201)
async def create_plant_type(
    plant_type: PlantTypeBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_type = PlantType(**plant_type.model_dump())
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    return db_type


@router.patch("/{type_id}", response_model=PlantTypeInDB)
async def update_plant_type(
    type_id: int,
    plant_type: PlantTypeBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_type = db.query(PlantType).filter(PlantType.id == type_id).first()
    if not db_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Plant type not found.'
        )

    for field, value in plant_type.model_dump().items():
        setattr(db_type, field, value)
    
    db.commit()
    db.refresh(db_type)
    return db_type


@router.delete("/{type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plant_type(
    type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_type = db.query(PlantType).filter(PlantType.id == type_id).first()
    if not db_type:
        raise HTTPException(status_code=404, detail="Plant type not found")
    
    db.delete(db_type)
    db.commit()
