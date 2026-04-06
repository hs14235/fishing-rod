from __future__ import annotations

from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field

ToneType = Literal["concise", "confident", "technical", "balanced"]
EmphasisType = Literal["auto", "backend", "full-stack", "ai-ml", "platform", "leadership"]
StatusType = Literal["draft", "applied", "interview", "rejected", "archived"]


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------

class GenerateRequest(BaseModel):
    company_name: str = Field(..., min_length=1)
    job_title: str = Field(..., min_length=1)
    job_description: str = Field(..., min_length=10)
    company_notes: str = ""
    tone: ToneType = "balanced"
    emphasis: EmphasisType = "auto"
    extra_instructions: str = ""


class GenerateResponse(BaseModel):
    keywords: List[str]
    fit_summary: str
    generated_cover_letter: str
    resume_suggestions: List[str]


# ---------------------------------------------------------------------------
# Applications
# ---------------------------------------------------------------------------

class ApplicationCreate(BaseModel):
    company_name: str = Field(..., min_length=1)
    job_title: str = Field(..., min_length=1)
    job_description: str = Field(..., min_length=10)
    company_notes: str = ""
    tone: ToneType = "balanced"
    emphasis: EmphasisType = "auto"
    status: StatusType = "draft"
    detected_keywords_json: str = "[]"
    fit_summary: str = ""
    generated_cover_letter: str = ""
    edited_cover_letter: str = ""
    generated_resume_suggestions_json: str = "[]"
    edited_notes: str = ""


class ApplicationUpdate(BaseModel):
    company_name: Optional[str] = None
    job_title: Optional[str] = None
    job_description: Optional[str] = None
    company_notes: Optional[str] = None
    tone: Optional[ToneType] = None
    emphasis: Optional[EmphasisType] = None
    status: Optional[StatusType] = None
    detected_keywords_json: Optional[str] = None
    fit_summary: Optional[str] = None
    generated_cover_letter: Optional[str] = None
    edited_cover_letter: Optional[str] = None
    generated_resume_suggestions_json: Optional[str] = None
    edited_notes: Optional[str] = None


class ApplicationOut(BaseModel):
    id: int
    company_name: str
    job_title: str
    job_description: str
    company_notes: str
    tone: str
    emphasis: str
    status: str
    detected_keywords_json: str
    fit_summary: str
    generated_cover_letter: str
    edited_cover_letter: str
    generated_resume_suggestions_json: str
    edited_notes: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

class SettingsUpdate(BaseModel):
    master_profile_text: Optional[str] = None
    fixed_philosophy_text: Optional[str] = None
    strengths_block_text: Optional[str] = None
    closing_block_text: Optional[str] = None
    default_tone: Optional[ToneType] = None
    default_emphasis: Optional[EmphasisType] = None


class SettingsOut(BaseModel):
    id: int
    master_profile_text: str
    fixed_philosophy_text: str
    strengths_block_text: str
    closing_block_text: str
    default_tone: str
    default_emphasis: str
    updated_at: datetime

    model_config = {"from_attributes": True}
