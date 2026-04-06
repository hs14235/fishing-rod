from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.db import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False, index=True)
    job_title = Column(String(255), nullable=False, index=True)
    job_description = Column(Text, nullable=False)
    company_notes = Column(Text, default="")
    tone = Column(String(50), default="balanced")
    emphasis = Column(String(50), default="auto")
    status = Column(String(50), default="draft", index=True)

    detected_keywords_json = Column(Text, default="[]")
    fit_summary = Column(Text, default="")
    generated_cover_letter = Column(Text, default="")
    edited_cover_letter = Column(Text, default="")
    generated_resume_suggestions_json = Column(Text, default="[]")
    edited_notes = Column(Text, default="")

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class UserProfileSettings(Base):
    __tablename__ = "user_profile_settings"

    id = Column(Integer, primary_key=True, index=True)
    master_profile_text = Column(Text, default="")
    fixed_philosophy_text = Column(Text, default="")
    strengths_block_text = Column(Text, default="")
    closing_block_text = Column(Text, default="")
    default_tone = Column(String(50), default="balanced")
    default_emphasis = Column(String(50), default="auto")

    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
