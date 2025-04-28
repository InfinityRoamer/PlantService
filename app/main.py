"""
Сервис для контроля и учета растений.
"""

from fastapi import FastAPI
from app.common.db.session import engine, Base
from app.modules.routers import auth, users, plants, plant_types


Base.metadata.create_all(bind=engine)  # Конфигурация базы данных на основе импортированных моделей

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(plants.router)
app.include_router(plant_types.router)


@app.get('/')
async def root():
    return "PlantService"
