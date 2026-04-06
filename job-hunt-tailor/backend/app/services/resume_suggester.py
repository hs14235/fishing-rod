"""Generate actionable resume bullet suggestions for a given role.

Rules
-----
- Suggestions are specific to Hamza's actual experience; nothing invented.
- No fabricated metrics or inflated claims.
- Each suggestion tells him *what* to change and *why* (brief).
- Keyword coverage analysis is included when JD keywords overlap with his stack.
- Capped at 8 suggestions total.
"""

from __future__ import annotations

from typing import List

from app.services.role_classifier import (
    AI_ML,
    BACKEND,
    FRONTEND,
    FULL_STACK,
    LEADERSHIP,
    PLATFORM,
    SOFTWARE_ENGINEER,
)

# Skills Hamza can truthfully claim — used for honest keyword-coverage analysis.
_HAMZA_SKILLS: set[str] = {
    "python", "java", "javascript", "typescript", "sql", "html", "html5", "css",
    "django", "node.js", "spring", "spring boot", "fastapi", "flask",
    "react", "vite", "next.js",
    "postgresql", "sqlite",
    "docker", "github", "postman", "git",
    "rest", "rest api",
    "authentication", "jwt", "role-based authentication",
    "faiss", "sentence-transformers", "rag", "ollama", "llm",
    "blender", "unreal engine 5", "machine learning",
    "agile",
}

# Base suggestions by role type — ordered from highest value to lowest.
_BASE_SUGGESTIONS: dict[str, List[str]] = {
    BACKEND: [
        "Lead your Trainline summary with what you owned: 'Designed normalized PostgreSQL schema, built REST API layer with role-based auth, and containerized the full stack with Docker.' Put the concrete deliverables first.",
        "Strengthen the data integrity bullet: replace passive phrasing like 'used PostgreSQL' with 'Enforced relational constraints and normalized schema across user, booking, and payment models to eliminate data redundancy.'",
        "Add a FastAPI-specific bullet under meeting-to-tasks: 'Built a FastAPI service exposing transcript-to-issue conversion; designed pluggable LLM backend interface supporting both local (Ollama) and hosted APIs.'",
        "Reorder your projects for backend roles: Trainline first, meeting-to-tasks second, Gulfstream third. The Gulfstream capstone is strong but less directly relevant to backend engineering.",
        "Check your skills section: make sure Docker, PostgreSQL, and FastAPI are explicitly listed — these are commonly screened by ATS for backend roles.",
    ],
    FULL_STACK: [
        "Lead your Trainline bullet with the full scope: 'Built end-to-end booking platform — PostgreSQL schema, REST APIs with role-based auth, and a React frontend covering seat selection, payments, notifications, and real-time chat; containerized with Docker.'",
        "Add a React architecture note: 'Structured frontend as modular React components with clearly defined API contracts, supporting complex stateful flows including authentication, payment, and real-time updates.'",
        "Mention Docker explicitly in your Trainline summary — it signals deployment ownership, which full-stack roles often expect.",
        "For roles that mention TypeScript, note your React/JavaScript base and add a line in your summary: 'Comfortable adopting TypeScript; current React work is in JavaScript.'",
        "Keep Trainline first. It is your strongest full-stack signal because it covers both layers of the stack in a single project.",
    ],
    AI_ML: [
        "Lead Gulfstream with the pipeline architecture: 'Architected AI-driven 3-D asset generation pipeline — Meshy API generation, Blender normalization and scaling, Unreal Engine 5 scene rendering — tailored to Gulfstream client specifications.'",
        "Strengthen meeting-to-tasks: 'Built retrieval-augmented generation pipeline using FAISS + Sentence-Transformers for local transcript indexing, with pluggable LLM backends (Ollama phi3:mini) served via FastAPI.'",
        "Frame Gulfstream around engineering constraints, not just the technology: 'Managed pipeline reliability and output consistency across Meshy, Blender, and UE5 tool chain under client spec requirements.'",
        "Place Gulfstream first for AI/ML roles — it is your strongest signal for production AI engineering work.",
        "In your skills section, explicitly list: FAISS, Sentence-Transformers, Ollama, Blender, Unreal Engine 5. These may be scanned by ATS for AI-adjacent roles.",
        "Avoid framing this as ML research — the profile supports AI pipeline engineering, not model training or academic ML. Keep that distinction in your language.",
    ],
    PLATFORM: [
        "Add a dedicated deployment bullet under Trainline: 'Containerized full application stack with Docker, enabling reproducible local development and consistent deployment across environments.'",
        "Strengthen your schema design bullet: 'Normalized PostgreSQL schema across user, booking, seat, and payment models — eliminated redundancy and enforced foreign key constraints for data integrity.'",
        "For platform roles, emphasize operational properties in your language: focus on reproducibility, clear failure modes, and data integrity rather than feature delivery.",
        "If you have any GitHub Actions, CI scripts, or Makefile/shell automation experience, add it — even simple pipeline config is relevant for platform roles.",
        "Check your skills section for: Docker, PostgreSQL, Git, Linux — these are commonly screened for platform engineering positions.",
    ],
    LEADERSHIP: [
        "Lead your ACM VP bullet with scale and outcomes: 'Led planning and execution of ACM chapter events for 100-plus students; managed logistics, speaker coordination, and community outreach.'",
        "Strengthen your Gulfstream team lead bullet: 'Led cross-functional engineering team on Gulfstream Aerospace capstone — decomposed client requirements into sprint tasks, coordinated with industrial designers, and maintained technical delivery.'",
        "Add a mentorship note under the student assistant role if accurate: 'Onboarded and supervised 10-plus team members on daily operations; reduced turnaround errors through process standardization.'",
        "For leadership-heavy roles, move ACM VP to a prominent position — it demonstrates coordination at scale (100+ people), not just project team management.",
    ],
    SOFTWARE_ENGINEER: [
        "Lead your Trainline bullet with scope and stack: 'Built full-stack booking platform — PostgreSQL schema, REST APIs, role-based auth, React UI, payments, real-time chat, Docker deployment.'",
        "Add a brief summary line at the top of your resume: 'Full-stack engineer with backend focus. Project experience in Python, React, PostgreSQL, Docker, and Java. End-to-end ownership across two platform-scale projects.'",
        "Reorder projects to put Trainline first — it covers the most ground and is the strongest signal for general SWE roles.",
        "In your skills section, ensure Docker, PostgreSQL, FastAPI, and React are prominent — these are likely scanned by ATS for general software engineering roles.",
        "Keep your project descriptions outcome-oriented where possible: what did the system do, what was your ownership, what was technically interesting about it.",
    ],
    FRONTEND: [
        "Lead Trainline with UI depth: 'Built modular React component library for booking platform — dashboard, authentication, seat selection, payment flow, notification center, and real-time chat.'",
        "Add an API integration note: 'Integrated React frontend with REST APIs — handled auth token management, optimistic updates, error state rendering, and loading patterns across the booking flow.'",
        "If you have any CSS architecture experience (modules, custom properties, responsive layout), add it explicitly — many frontend roles screen for CSS skill beyond basic usage.",
        "Note your backend integration awareness: understanding the data shape and auth flow behind your UI is a differentiator for full-stack-leaning frontend roles.",
    ],
}


def build_resume_suggestions(
    role_type: str,
    keywords: List[str],
    job_title: str,
) -> List[str]:
    """Return up to 8 targeted resume improvement suggestions."""
    effective_role = role_type if role_type in _BASE_SUGGESTIONS else SOFTWARE_ENGINEER
    suggestions = list(_BASE_SUGGESTIONS[effective_role])

    # Keyword coverage: find JD keywords Hamza can claim and surface them
    matching = [k for k in keywords if k.lower() in _HAMZA_SKILLS]
    if matching:
        kw_str = ", ".join(matching[:6])
        suggestions.insert(
            0,
            f"JD keyword alignment — your profile supports: {kw_str}. "
            f"Make sure these appear verbatim in your resume skills section and project bullets "
            f"where accurate, as ATS scanners match exact terms.",
        )

    return suggestions[:8]
