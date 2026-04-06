import json
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.db import get_db
from app.schemas import (
    ApplicationCreate,
    ApplicationOut,
    ApplicationUpdate,
    GenerateRequest,
    GenerateResponse,
)
from app.services.generation_engine import run_generation

router = APIRouter(prefix="/api", tags=["applications"])


@router.post("/applications", response_model=ApplicationOut, status_code=201)
def create_application(
    data: ApplicationCreate, db: Session = Depends(get_db)
) -> ApplicationOut:
    return crud.create_application(db, data)


@router.get("/applications", response_model=List[ApplicationOut])
def list_applications(
    search: Optional[str] = Query(None, description="Filter by company or role name"),
    status: Optional[str] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> List[ApplicationOut]:
    return crud.list_applications(db, search=search, status=status, skip=skip, limit=limit)


@router.get("/applications/{app_id}", response_model=ApplicationOut)
def get_application(app_id: int, db: Session = Depends(get_db)) -> ApplicationOut:
    app = crud.get_application(db, app_id)
    if app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return app


@router.put("/applications/{app_id}", response_model=ApplicationOut)
def update_application(
    app_id: int, data: ApplicationUpdate, db: Session = Depends(get_db)
) -> ApplicationOut:
    updated = crud.update_application(db, app_id, data)
    if updated is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return updated


@router.delete("/applications/{app_id}", status_code=204)
def delete_application(app_id: int, db: Session = Depends(get_db)) -> None:
    deleted = crud.delete_application(db, app_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Application not found")


@router.post("/applications/{app_id}/regenerate", response_model=ApplicationOut)
def regenerate_application(app_id: int, db: Session = Depends(get_db)) -> ApplicationOut:
    app = crud.get_application(db, app_id)
    if app is None:
        raise HTTPException(status_code=404, detail="Application not found")

    profile_settings = crud.get_settings(db)
    if profile_settings is None:
        raise HTTPException(status_code=500, detail="Profile settings not found")

    request = GenerateRequest(
        company_name=app.company_name,
        job_title=app.job_title,
        job_description=app.job_description,
        company_notes=app.company_notes or "",
        tone=app.tone or "balanced",
        emphasis=app.emphasis or "auto",
    )

    result = run_generation(request, profile_settings)

    updated = crud.update_application(
        db,
        app_id,
        ApplicationUpdate(
            detected_keywords_json=json.dumps(result.keywords),
            fit_summary=result.fit_summary,
            generated_cover_letter=result.generated_cover_letter,
            generated_resume_suggestions_json=json.dumps(result.resume_suggestions),
        ),
    )
    return updated
