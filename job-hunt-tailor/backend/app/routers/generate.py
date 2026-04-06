from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.db import get_db
from app.schemas import GenerateRequest, GenerateResponse
from app.services.generation_engine import run_generation

router = APIRouter(prefix="/api", tags=["generate"])


@router.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest, db: Session = Depends(get_db)) -> GenerateResponse:
    profile_settings = crud.get_settings(db)
    if profile_settings is None:
        raise HTTPException(
            status_code=500,
            detail="Profile settings not found. Run the app once to seed defaults.",
        )
    return run_generation(request, profile_settings)
