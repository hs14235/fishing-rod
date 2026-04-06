"""Abstract base class for generation providers."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.models import UserProfileSettings
from app.schemas import GenerateRequest, GenerateResponse


class BaseGenerationProvider(ABC):
    def __init__(self, profile_settings: UserProfileSettings) -> None:
        self.profile_settings = profile_settings

    @abstractmethod
    def generate(self, request: GenerateRequest) -> GenerateResponse:
        ...
