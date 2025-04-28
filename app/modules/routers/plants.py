from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from sqlalchemy.orm import Session
from app.common.db import get_db
from app.modules.models import Plant, PlantType, User
from app.modules.schemas.plants import PlantBase, PlantInDB, PlantUpdate
from app.common.utils import get_current_user

router = APIRouter(prefix='/plants')


@router.get('/')
async def get_plants(db: Session = Depends(get_db)):
    plants = db.query(Plant).all()
    return plants if plants else 'No plants added.'


@router.post("/", response_model=PlantInDB)
async def create_plant(
    plant_data: PlantBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not db.query(PlantType).filter(PlantType.id == plant_data.type_id).first():
        raise HTTPException(status_code=404, detail="Plant type not found")
    
    db_plant = Plant(
        **plant_data.model_dump(),
        responsible_id=current_user.id
    )
    
    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)
    return db_plant


@router.put("/{plant_id}", response_model=PlantInDB)
async def update_plant(
    plant_id: int,
    plant: PlantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not db_plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Plant not found.'
        )
    
    if db_plant.responsible_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You can only update your own plants.'
        )

    if plant.type_id:
        db_plant_type = db.query(PlantType).filter(PlantType.id == plant.type_id).first()
        if not db_plant_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Plant type not found.'
            )

    for var, value in plant.model_dump(exclude_unset=True).items():
        setattr(db_plant, var, value)
    
    db.commit()
    db.refresh(db_plant)
    return db_plant


@router.delete("/{plant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plant(
    plant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not db_plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plant not found."
        )
    
    if db_plant.responsible_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own plants."
        )
    
    db.delete(db_plant)
    db.commit()
    return None


@router.get("/needs-watering") 
def get_plants_needing_water( 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user) 
): 
    today = datetime.now().date() 
    plants = db.query(Plant).filter(Plant.responsible_id == current_user.id).all() 
    result = [] 
    for plant in plants: 
        plant_type = db.query(PlantType).filter(PlantType.id == plant.type_id).first() 
        days_since_watered = (today - plant.last_watered).days 
        if days_since_watered >= plant_type.watering_interval: 
            result.append({ 
            "plant_id": plant.id, 
            "plant_name": plant.name, 
            "days_overdue": days_since_watered - plant_type.watering_interval 
        }) 
    return {"plants_needing_water": result}
