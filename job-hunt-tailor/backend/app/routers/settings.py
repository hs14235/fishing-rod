from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.db import get_db
from app.schemas import SettingsOut, SettingsUpdate

router = APIRouter(prefix="/api", tags=["settings"])


@router.get("/settings", response_model=SettingsOut)
def get_settings(db: Session = Depends(get_db)) -> SettingsOut:
    settings = crud.get_settings(db)
    if settings is None:
        raise HTTPException(status_code=404, detail="Settings not found")
    return settings


@router.put("/settings", response_model=SettingsOut)
def update_settings(data: SettingsUpdate, db: Session = Depends(get_db)) -> SettingsOut:
    return crud.upsert_settings(db, data)
