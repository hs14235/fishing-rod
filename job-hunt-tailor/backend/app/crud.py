from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models import Application, UserProfileSettings
from app.schemas import ApplicationCreate, ApplicationUpdate, SettingsUpdate


# ---------------------------------------------------------------------------
# Applications
# ---------------------------------------------------------------------------

def get_application(db: Session, app_id: int) -> Optional[Application]:
    return db.query(Application).filter(Application.id == app_id).first()


def list_applications(
    db: Session,
    *,
    search: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[Application]:
    query = db.query(Application)
    if search:
        term = f"%{search}%"
        query = query.filter(
            or_(
                Application.company_name.ilike(term),
                Application.job_title.ilike(term),
            )
        )
    if status:
        query = query.filter(Application.status == status)
    return query.order_by(Application.updated_at.desc()).offset(skip).limit(limit).all()


def create_application(db: Session, data: ApplicationCreate) -> Application:
    now = datetime.utcnow()
    app = Application(**data.model_dump(), created_at=now, updated_at=now)
    db.add(app)
    db.commit()
    db.refresh(app)
    return app


def update_application(
    db: Session, app_id: int, data: ApplicationUpdate
) -> Optional[Application]:
    app = get_application(db, app_id)
    if app is None:
        return None
    changes = data.model_dump(exclude_none=True)
    for field, value in changes.items():
        setattr(app, field, value)
    app.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(app)
    return app


def delete_application(db: Session, app_id: int) -> bool:
    app = get_application(db, app_id)
    if app is None:
        return False
    db.delete(app)
    db.commit()
    return True


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

def get_settings(db: Session) -> Optional[UserProfileSettings]:
    return db.query(UserProfileSettings).first()


def upsert_settings(db: Session, data: SettingsUpdate) -> UserProfileSettings:
    settings = db.query(UserProfileSettings).first()
    if settings is None:
        settings = UserProfileSettings(updated_at=datetime.utcnow())
        db.add(settings)
    changes = data.model_dump(exclude_none=True)
    for field, value in changes.items():
        setattr(settings, field, value)
    settings.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(settings)
    return settings
