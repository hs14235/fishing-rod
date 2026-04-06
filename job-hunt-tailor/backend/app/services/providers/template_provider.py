"""Deterministic template-based generation provider.

Used by default when no LLM API key is configured.
All output is grounded in the master profile and role-specific templates —
nothing is invented or hallucinated.
"""

from __future__ import annotations

from app.schemas import GenerateRequest, GenerateResponse
from app.services.cover_letter_builder import (
    build_cover_letter,
    build_fit_summary,
    clean_cover_letter_output,
)
from app.services.keyword_extractor import extract_keywords
from app.services.project_selector import select_projects
from app.services.providers.base import BaseGenerationProvider
from app.services.resume_suggester import build_resume_suggestions
from app.services.role_classifier import classify_role


class TemplateProvider(BaseGenerationProvider):
    def generate(self, request: GenerateRequest) -> GenerateResponse:
        keywords = extract_keywords(request.job_description, request.job_title)

        classified_role = classify_role(request.job_title, request.job_description)
        # Explicit emphasis overrides the classifier; "auto" defers to it.
        effective_role = (
            classified_role
            if request.emphasis in ("auto", "")
            else request.emphasis
        )

        selected_projects = select_projects(effective_role, keywords)

        cover_letter = build_cover_letter(
            company_name=request.company_name,
            job_title=request.job_title,
            role_type=effective_role,
            selected_projects=selected_projects,
            keywords=keywords,
            tone=request.tone,
            fixed_philosophy=self.profile_settings.fixed_philosophy_text,
            closing_block=self.profile_settings.closing_block_text,
            company_notes=request.company_notes,
            extra_instructions=request.extra_instructions,
        )
        cover_letter = clean_cover_letter_output(cover_letter, request.job_description)

        fit_summary = build_fit_summary(
            role_type=effective_role,
            keywords=keywords,
            job_title=request.job_title,
            company_name=request.company_name,
        )

        resume_suggestions = build_resume_suggestions(
            role_type=effective_role,
            keywords=keywords,
            job_title=request.job_title,
        )

        return GenerateResponse(
            keywords=keywords,
            fit_summary=fit_summary,
            generated_cover_letter=cover_letter,
            resume_suggestions=resume_suggestions,
        )
