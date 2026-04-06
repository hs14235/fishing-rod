"""Select the most relevant projects from Hamza's profile for a given role.

Each project entry carries the role tags it fits best, so the selector can
rank and return the top matches without guessing.
"""

from __future__ import annotations

from typing import Dict, List

from app.services.role_classifier import (
    AI_ML,
    BACKEND,
    FRONTEND,
    FULL_STACK,
    LEADERSHIP,
    PLATFORM,
    SOFTWARE_ENGINEER,
)

# Canonical project catalogue drawn directly from the master profile.
# Do not add technologies or claims that are not in the profile.
PROJECTS: Dict[str, Dict] = {
    "trainline": {
        "name": "Trainline (full-stack booking platform)",
        "tags": [FULL_STACK, BACKEND, PLATFORM, SOFTWARE_ENGINEER],
        "tech": ["React", "PostgreSQL", "Docker", "REST APIs", "role-based auth", "real-time chat"],
        "summary": (
            "Full-stack booking platform: PostgreSQL schema, REST APIs with role-based auth, "
            "modular React components (seat selection, payments, notifications, real-time chat), "
            "Docker containerization."
        ),
    },
    "gulfstream": {
        "name": "Gulfstream Aerospace capstone (AI pipeline team lead)",
        "tags": [AI_ML, LEADERSHIP, SOFTWARE_ENGINEER],
        "tech": ["Blender", "Unreal Engine 5", "Meshy", "AI pipelines"],
        "summary": (
            "AI-driven 3-D asset generation pipeline: Meshy → Blender (normalization/scaling) → "
            "Unreal Engine 5 rendering, built for Gulfstream designers. Team-lead role."
        ),
    },
    "meeting_to_tasks": {
        "name": "meeting-to-tasks",
        "tags": [AI_ML, BACKEND, SOFTWARE_ENGINEER],
        "tech": ["FastAPI", "FAISS", "Sentence-Transformers", "Ollama", "GitHub Issues API"],
        "summary": (
            "RAG system converting meeting transcripts into GitHub Issues using FAISS + "
            "Sentence-Transformers for local retrieval and pluggable LLM backends via FastAPI."
        ),
    },
    "flight_booking": {
        "name": "Flight Booking Web App",
        "tags": [BACKEND, PLATFORM, SOFTWARE_ENGINEER],
        "tech": ["Spring Boot", "PostgreSQL", "HTML/CSS", "REST APIs"],
        "summary": (
            "Transactional booking system with Spring Boot, normalized PostgreSQL schema, "
            "REST APIs, and accessible authenticated user flows."
        ),
    },
}


def select_projects(role_type: str, keywords: List[str]) -> List[Dict]:
    """Return up to 3 projects ranked by relevance to *role_type* and *keywords*."""
    kw_lower = {k.lower() for k in keywords}

    scored: List[tuple] = []
    for key, proj in PROJECTS.items():
        score = 0
        if role_type in proj["tags"]:
            score += 3
        # Boost for tech-stack overlap with the JD keywords
        for tech in proj["tech"]:
            if tech.lower() in kw_lower:
                score += 1
        scored.append((score, key, proj))

    scored.sort(key=lambda x: -x[0])
    return [proj for _, _, proj in scored[:3]]
