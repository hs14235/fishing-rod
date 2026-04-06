"""Generation engine — selects the right provider and runs generation."""

from __future__ import annotations

from app.config import get_settings
from app.models import UserProfileSettings
from app.schemas import GenerateRequest, GenerateResponse
from app.services.providers.base import BaseGenerationProvider
from app.services.providers.llm_provider import LLMProvider
from app.services.providers.template_provider import TemplateProvider


def get_provider(profile_settings: UserProfileSettings) -> BaseGenerationProvider:
    """Return LLMProvider if an API key is configured, else TemplateProvider."""
    config = get_settings()
    if config.openai_api_key.strip():
        return LLMProvider(profile_settings)
    return TemplateProvider(profile_settings)


def run_generation(
    request: GenerateRequest, profile_settings: UserProfileSettings
) -> GenerateResponse:
    provider = get_provider(profile_settings)
    return provider.generate(request)
