"""Classify the role type from a job title and description.

Returns one of: backend, full-stack, frontend, ai-ml, platform, leadership,
or software-engineer (catch-all).
"""

from __future__ import annotations

from typing import Dict, List

RoleType = str  # one of the constants below

BACKEND = "backend"
FULL_STACK = "full-stack"
FRONTEND = "frontend"
AI_ML = "ai-ml"
PLATFORM = "platform"
LEADERSHIP = "leadership"
SOFTWARE_ENGINEER = "software-engineer"

_PATTERNS: Dict[str, List[str]] = {
    BACKEND: [
        "backend", "back-end", "back end", "server-side", "api engineer",
        "systems engineer", "api developer",
    ],
    FULL_STACK: [
        "full stack", "full-stack", "fullstack",
    ],
    FRONTEND: [
        "frontend", "front-end", "front end", "ui engineer", "ux engineer",
        "ui developer", "web developer",
    ],
    AI_ML: [
        "machine learning", "ml engineer", "ai engineer", "data scientist",
        "nlp engineer", "computer vision", "deep learning", "llm engineer",
        "ai/ml", "ai pipeline", "ml platform", "data engineer",
    ],
    PLATFORM: [
        "platform engineer", "devops", "infrastructure", "site reliability",
        "sre", "cloud engineer", "reliability engineer",
    ],
    LEADERSHIP: [
        "tech lead", "team lead", "engineering manager", "lead engineer",
        "engineering lead", "staff engineer",
    ],
}


def classify_role(job_title: str, job_description: str) -> RoleType:
    """Return the most likely role category."""
    # Use title heavily; scan first 600 chars of description for context
    text = (job_title + " " + job_description[:600]).lower()

    scores: Dict[str, int] = {role: 0 for role in _PATTERNS}
    for role, patterns in _PATTERNS.items():
        for p in patterns:
            if p in text:
                # Title matches count double
                scores[role] += 2 if p in job_title.lower() else 1

    best = max(scores, key=lambda r: scores[r])
    return best if scores[best] > 0 else SOFTWARE_ENGINEER
