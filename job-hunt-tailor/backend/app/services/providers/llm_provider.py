"""LLM-backed generation provider (OpenAI-compatible API).

Falls back to TemplateProvider on any error so the app always works.

The LLM is used only to write the cover letter.
Keywords, fit summary, and resume suggestions are always template-generated
to keep them grounded and deterministic.
"""

from __future__ import annotations

import logging

from app.config import get_settings
from app.schemas import GenerateRequest, GenerateResponse
from app.services.providers.base import BaseGenerationProvider
from app.services.providers.template_provider import TemplateProvider

logger = logging.getLogger(__name__)


_SYSTEM_PROMPT = """\
You are writing a cover letter on behalf of Hamza Salahuddin, a CS student graduating \
May 2026 from Georgia Southern University. Use only the profile information provided — \
do not invent experience, metrics, or technologies not present in the profile.

PROFILE:
{master_profile}

ENGINEERING PHILOSOPHY (must appear in the letter, lightly paraphrased or verbatim):
{philosophy}

WRITING RULES:
- Length: 230-310 words total.
- Structure: opening + targeted experience paragraph, then philosophy paragraph, \
then credentials line, then a one-sentence close.
- Tone: {tone}.
- No generic praise ("passionate", "dynamic", "innovative", "excited to contribute").
- No buzzword stacking.
- No invented metrics or production-traffic claims.
- Vary sentence length — mix short declarative with longer explanatory sentences.
- Frame the candidate honestly as early-career / new grad.
- Ground every claim in the profile above.
- Output only the letter text. No headers, no date, no address block.\
"""

_USER_PROMPT = """\
Write a tailored cover letter for:

Company: {company_name}
Job Title: {job_title}
Role emphasis: {emphasis}
Tone: {tone}

Job Description (first 2000 chars):
{job_description}

Detected keywords: {keywords}
{company_notes_section}
{extra_instructions_section}

Start directly with the opening sentence.\
"""


class LLMProvider(BaseGenerationProvider):
    def generate(self, request: GenerateRequest) -> GenerateResponse:
        # Always run the template first for keywords / fit / suggestions.
        template_result = TemplateProvider(self.profile_settings).generate(request)

        try:
            improved_letter = self._call_llm(request, template_result.keywords)
        except Exception as exc:
            logger.warning("LLM generation failed, using template output: %s", exc)
            improved_letter = template_result.generated_cover_letter

        return GenerateResponse(
            keywords=template_result.keywords,
            fit_summary=template_result.fit_summary,
            generated_cover_letter=improved_letter,
            resume_suggestions=template_result.resume_suggestions,
        )

    def _call_llm(self, request: GenerateRequest, keywords: list[str]) -> str:
        from openai import OpenAI  # imported lazily so the package is optional

        config = get_settings()
        client = OpenAI(api_key=config.openai_api_key, base_url=config.openai_base_url)

        system_content = _SYSTEM_PROMPT.format(
            master_profile=self.profile_settings.master_profile_text,
            philosophy=self.profile_settings.fixed_philosophy_text,
            tone=request.tone,
        )

        company_notes_section = (
            f"Company notes: {request.company_notes}" if request.company_notes else ""
        )
        extra_section = (
            f"Extra instructions: {request.extra_instructions}"
            if request.extra_instructions
            else ""
        )

        user_content = _USER_PROMPT.format(
            company_name=request.company_name,
            job_title=request.job_title,
            emphasis=request.emphasis,
            tone=request.tone,
            job_description=request.job_description[:2000],
            keywords=", ".join(keywords[:10]),
            company_notes_section=company_notes_section,
            extra_instructions_section=extra_section,
        )

        response = client.chat.completions.create(
            model=config.openai_model,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content},
            ],
            max_tokens=650,
            temperature=0.6,
        )

        return response.choices[0].message.content.strip()
