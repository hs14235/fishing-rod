"""Cover letter assembly for Hamza Salahuddin.

Structure
---------
Paragraph 1 — Opening + targeted experience (~100-120 words, 20% variable)
Paragraph 2 — Engineering philosophy (~65 words, 80% fixed / user-editable)
Paragraph 3 — Credentials + working style (~40 words, 80% fixed / user-editable)
Paragraph 4 — Closing (~15 words)

Total target: 230-310 words.

Quality rules enforced here
---------------------------
- All claims grounded in the master profile; nothing invented.
- No generic praise ("passionate", "dynamic team", "innovative company").
- No buzzword stacking or metric fabrication.
- Sentence structures vary deliberately across paragraphs.
- Framing is honest about career stage (student / new-grad).
- Output is a draft for human editing, not a finished product.
"""

from __future__ import annotations

import re
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

# ---------------------------------------------------------------------------
# Fixed defaults (used when the user has not set custom values in Settings)
# ---------------------------------------------------------------------------

_DEFAULT_PHILOSOPHY = (
    "I think about software in terms of where it is most likely to break — usually at the "
    "boundary between components, or in assumptions baked in early. That shapes how I build: "
    "get something working end-to-end quickly, even if it is rough, then tighten constraints "
    "and handle edge cases from a real foundation. I would rather ship a working system that "
    "needs polish than a polished design that has not been tested against real data."
)

_DEFAULT_CLOSING = (
    "I would welcome a chance to discuss this further. Thank you for your time."
)

_JD_LEAK_HEADINGS = (
    "about ",
    "location:",
    "schedule:",
    "what you'll do",
    "what you will do",
    "required skills",
    "qualifications",
    "responsibilities",
    "preferred qualifications",
)

# ---------------------------------------------------------------------------
# Role-specific opening + targeted experience blocks (the 20% variable part)
#
# Rules applied to each block:
#   - Opens with a direct statement of interest, not a formulaic "I am writing to express..."
#   - Paragraph 2 gives concrete project details with named technologies.
#   - Honest framing: "I built / I owned / I led" — no inflated verbs.
#   - No invented numbers, no claimed production traffic, no vague scale claims.
#   - Sentence length varies (short declarative + longer explanatory, alternating).
# ---------------------------------------------------------------------------

_TARGETED_OPENING: dict[str, str] = {
    BACKEND: (
        "I'm applying for the {job_title} role at {company_name}. "
        "Most of my project work has been backend-focused: data modeling, API design, and "
        "getting systems to behave correctly at the edges rather than just in the happy path.\n\n"
        "My strongest relevant project is Trainline, a full-stack booking platform where I "
        "owned the backend end-to-end: I designed the PostgreSQL schema, built the REST API "
        "layer with role-based authentication, and containerized the stack with Docker. "
        "Separately, I built meeting-to-tasks — a FastAPI service that converts meeting "
        "transcripts into GitHub Issues using local FAISS retrieval and an Ollama-backed LLM. "
        "Both pushed me to think carefully about data contracts and what breaks when an "
        "assumption turns out to be wrong."
    ),
    FULL_STACK: (
        "I'm applying for the {job_title} position at {company_name}. "
        "My background is in full-stack development with a backend lean — I build systems "
        "end-to-end and care about the seams between layers.\n\n"
        "My main project is Trainline: a complete booking platform where I owned the "
        "PostgreSQL schema, REST APIs, and a React frontend covering seat selection, payments, "
        "notifications, and real-time chat, all containerized with Docker. Working both sides "
        "of the stack on the same project made it clear how much frontend complexity is driven "
        "by backend data shape decisions. I also have Python/FastAPI experience from "
        "meeting-to-tasks, a local RAG system I built to parse meeting transcripts into "
        "structured GitHub Issues."
    ),
    AI_ML: (
        "I'm applying for the {job_title} role at {company_name}. "
        "My recent work has been on AI systems where engineering constraints matter as much "
        "as the model itself — pipelines that have to stay reliable, not just accurate in "
        "controlled conditions.\n\n"
        "For my Gulfstream Aerospace capstone I lead a team building a 3-D asset generation "
        "pipeline: Meshy produces the initial models, Blender handles normalization and "
        "scaling, and Unreal Engine 5 renders the final scenes to client specifications. "
        "The hard parts have been pipeline reliability and keeping outputs consistent across "
        "the tool chain — not the model quality itself. I have also built meeting-to-tasks, "
        "a RAG system using FAISS, Sentence-Transformers, and pluggable LLM backends via "
        "FastAPI, focused on local inference rather than API dependency."
    ),
    PLATFORM: (
        "I'm applying for the {job_title} role at {company_name}. "
        "I am drawn to platform and infrastructure work because the properties I care about "
        "in application code — reproducible builds, clear data boundaries, predictable failure "
        "modes — are first-class concerns at the platform layer.\n\n"
        "My most relevant work is Trainline: I designed the PostgreSQL schema, built REST APIs "
        "with role-based auth, and containerized the full stack with Docker. Schema design and "
        "deployment configuration were not afterthoughts — I treated them as the foundation "
        "the rest of the system depends on. I approach platform work the same way: explicit "
        "about constraints, attentive to what breaks at scale or under unusual inputs."
    ),
    LEADERSHIP: (
        "I'm applying for the {job_title} role at {company_name}. "
        "I combine hands-on engineering work with real coordination and team leadership "
        "experience, which is not always easy to find in someone still finishing their degree.\n\n"
        "At Georgia Southern I serve as VP of ACM, leading event planning and execution for "
        "our 100-plus member chapter. In my Gulfstream Aerospace capstone I lead the "
        "engineering team directly: I translate requirements from Gulfstream designers into "
        "technical tasks, manage the AI pipeline work, and stay in the code myself. Earlier, "
        "I trained and led a 10-plus person team in a student assistant role, which gave me "
        "early practice in coordination without authority. I am most effective where technical "
        "depth and team coordination overlap, not where they are split between different people."
    ),
    SOFTWARE_ENGINEER: (
        "I'm applying for the {job_title} role at {company_name}. "
        "My project work spans backend systems, full-stack development, and AI pipelines, "
        "with a consistent thread of end-to-end ownership across all of it.\n\n"
        "My strongest project is Trainline — a full-stack booking platform where I owned the "
        "PostgreSQL schema, REST APIs, Docker setup, role-based auth, and a React frontend "
        "covering the full booking flow. I have also built meeting-to-tasks using FastAPI and "
        "local LLMs, and I currently lead an engineering team for my Gulfstream Aerospace "
        "capstone building an AI-driven 3-D asset pipeline. Each project gave me practice "
        "taking a system from the data model through deployment and handling the edge cases "
        "that only show up once something is actually running."
    ),
    FRONTEND: (
        "I'm applying for the {job_title} role at {company_name}. "
        "My frontend work is integration-aware — I build UIs that account for the real "
        "shape of the data and error states coming from the backend.\n\n"
        "On Trainline I built the entire React frontend: modular components for the dashboard, "
        "authentication flows, seat selection, payment integration, notifications, and "
        "real-time chat. Working directly with the API contracts on the same project meant "
        "I could make sensible assumptions in the UI rather than building against an idealized "
        "response format. I also understand the backend well enough to flag when a data shape "
        "decision will cause frontend complexity downstream."
    ),
}

# ---------------------------------------------------------------------------
# Role-specific credentials block (~40 words each)
# Honest about career stage, concrete about stack.
# ---------------------------------------------------------------------------

_CREDENTIALS: dict[str, str] = {
    BACKEND: (
        "Stack: Python (FastAPI, Django), PostgreSQL, Docker, REST API design, "
        "with Java (Spring) and JavaScript alongside. "
        "My debugging instinct tends toward data — I check the schema and API "
        "contract before the application logic."
    ),
    FULL_STACK: (
        "Stack: Python (FastAPI, Django), React/JavaScript, PostgreSQL, Docker, "
        "Node.js, Java (Spring). "
        "Having built both sides of the same system, I have learned how much "
        "complexity moves between layers depending on where you make your data-shape decisions."
    ),
    AI_ML: (
        "Stack: Python/FastAPI, FAISS, Sentence-Transformers, Ollama, "
        "Blender scripting, Unreal Engine 5, PostgreSQL, Docker. "
        "My interest in AI work is in the engineering layer — reliable pipelines, "
        "predictable failure modes, systems that degrade gracefully."
    ),
    PLATFORM: (
        "Stack: Python, PostgreSQL, Docker, REST APIs, GitHub, with SQL "
        "and Java in the mix. "
        "I think about operational properties as much as feature delivery: "
        "what is this system guaranteed to do, and what happens when that guarantee is tested."
    ),
    LEADERSHIP: (
        "Stack: Python (FastAPI, Django), React/JavaScript, PostgreSQL, Docker, "
        "Java (Spring). "
        "I am most effective where I am expected to be in the code and coordinating — "
        "not choosing between the two."
    ),
    SOFTWARE_ENGINEER: (
        "Stack: Python (FastAPI, Django), React/JavaScript, PostgreSQL, Docker, "
        "Java (Spring), Node.js. "
        "I debug by tracing data contracts — checking what is promised at each "
        "boundary and where that promise is first broken."
    ),
    FRONTEND: (
        "Stack: React, JavaScript, CSS/HTML, with REST API integration and "
        "some Python/FastAPI on the backend side. "
        "I write frontend code with an explicit model of what the API can and "
        "cannot guarantee, which shapes how I handle loading states and errors."
    ),
}


def _condense_line(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _build_company_signal(*, company_name: str, company_notes: str) -> str:
    """Convert optional company notes into one safe sentence.

    If notes look like pasted job-description blocks, ignore them.
    """
    raw = company_notes.strip()
    if not raw:
        return ""

    lines = [ln.strip(" -\t") for ln in raw.splitlines() if ln.strip()]
    if len(lines) > 4:
        return ""

    lowered = [ln.lower() for ln in lines]
    if any(any(h in ln for h in _JD_LEAK_HEADINGS) for ln in lowered):
        return ""

    one_line = _condense_line(" ".join(lines))
    if len(one_line.split()) > 30:
        return ""

    return (
        f"I am especially interested in {company_name} because {one_line.rstrip('.')}"
        "."
    )


def _build_tailored_closing(*, company_name: str, job_title: str, role_type: str, keywords: List[str]) -> str:
    """Generate a concise closing sentence tied to company + role context."""
    signal = {
        BACKEND: "API and data-contract reliability",
        FULL_STACK: "end-to-end product delivery across frontend and backend",
        AI_ML: "AI pipeline reliability and grounded implementation",
        PLATFORM: "platform reliability under real constraints",
        LEADERSHIP: "technical leadership while staying hands-on",
        FRONTEND: "frontend quality grounded in real API constraints",
        SOFTWARE_ENGINEER: "end-to-end engineering execution",
    }.get(role_type, "end-to-end engineering execution")

    keyword_hint = ""
    if keywords:
        top = ", ".join(keywords[:2])
        keyword_hint = f" with focus on {top}"

    article = "an" if job_title.strip().lower()[:1] in {"a", "e", "i", "o", "u"} else "a"

    return (
        f"I would welcome the chance to contribute to {company_name} as {article} {job_title} "
        f"through {signal}{keyword_hint}. Thank you for your time."
    )


def clean_cover_letter_output(letter: str, job_description: str) -> str:
    """Remove obvious job-description leakage from generated letter text."""
    jd_lines = {
        _condense_line(ln).lower()
        for ln in job_description.splitlines()
        if len(_condense_line(ln)) >= 45
    }

    cleaned_lines: list[str] = []
    for raw in letter.splitlines():
        line = raw.strip()
        if not line:
            cleaned_lines.append("")
            continue

        compact = _condense_line(line)
        lowered = compact.lower()
        if any(lowered.startswith(h) for h in _JD_LEAK_HEADINGS):
            continue
        if lowered in jd_lines:
            continue

        cleaned_lines.append(compact)

    text = "\n".join(cleaned_lines)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text

# ---------------------------------------------------------------------------
# Fit summaries — short analyst-style read, not a marketing pitch.
# Honest about fit level and any gaps.
# ---------------------------------------------------------------------------

_FIT_SUMMARIES: dict[str, str] = {
    BACKEND: (
        "Good fit for backend engineering roles. Trainline demonstrates end-to-end backend "
        "ownership: schema design, REST API layer, role-based auth, Docker. "
        "meeting-to-tasks adds FastAPI and LLM integration experience. "
        "New grad (May 2026) — best fit for junior or new-grad backend roles."
    ),
    FULL_STACK: (
        "Strong fit for full-stack roles. Trainline is a complete end-to-end project covering "
        "schema, APIs, and a React frontend with complex UX flows. "
        "Backend orientation is stronger than frontend, but both are demonstrated. "
        "New grad (May 2026)."
    ),
    AI_ML: (
        "Reasonable fit for AI-adjacent engineering roles. "
        "Gulfstream = production AI pipeline engineering (not ML research). "
        "meeting-to-tasks = practical RAG with local inference. "
        "Claims are grounded in engineering work, not academic ML coursework. "
        "Not a fit for deep-learning research or model training roles. New grad (May 2026)."
    ),
    PLATFORM: (
        "Good fit for junior platform or backend-infrastructure roles. "
        "Docker, PostgreSQL schema design, and REST API work are all demonstrated. "
        "Limited cloud or CI/CD pipeline experience in the profile — worth noting. "
        "New grad (May 2026)."
    ),
    LEADERSHIP: (
        "Reasonable fit for roles that blend technical work and coordination. "
        "ACM VP and Gulfstream team lead are genuine leadership experiences, not just titles. "
        "Still a student and early-career — best for junior or associate roles with "
        "team-lead potential, not senior engineering management. New grad (May 2026)."
    ),
    SOFTWARE_ENGINEER: (
        "Good general fit for junior software engineering roles. "
        "End-to-end project ownership across backend, full-stack, and AI-adjacent work. "
        "Strongest signals: Trainline (full-stack), meeting-to-tasks (FastAPI/AI). "
        "New grad (May 2026)."
    ),
    FRONTEND: (
        "Moderate fit for frontend roles. "
        "React experience is real and covers complex flows (Trainline), but backend "
        "orientation is stronger. Worth noting if the role is predominantly frontend. "
        "New grad (May 2026)."
    ),
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def build_cover_letter(
    *,
    company_name: str,
    job_title: str,
    role_type: str,
    selected_projects: List[dict],  # passed in but reserved for future LLM use
    keywords: List[str],  # same
    tone: str = "balanced",
    fixed_philosophy: str = "",
    closing_block: str = "",
    company_notes: str = "",
    extra_instructions: str = "",  # advisory only for template engine
) -> str:
    """Assemble a cover letter draft.

    The output is intentionally a starting point for editing, not a
    finished product.  Word count target: 230-310.
    """
    effective_role = role_type if role_type in _TARGETED_OPENING else SOFTWARE_ENGINEER

    # Paragraph 1: opening + targeted experience
    opening = _TARGETED_OPENING[effective_role].format(
        company_name=company_name,
        job_title=job_title,
    )

    # Optional: append company context if the user provided notes
    company_signal = _build_company_signal(
        company_name=company_name,
        company_notes=company_notes,
    )
    if company_signal:
        opening = opening + "\n\n" + company_signal

    # Paragraph 2: engineering philosophy (80% fixed, user-editable in Settings)
    philosophy = fixed_philosophy.strip() if fixed_philosophy.strip() else _DEFAULT_PHILOSOPHY

    # Paragraph 3: credentials
    credentials = _CREDENTIALS.get(effective_role, _CREDENTIALS[SOFTWARE_ENGINEER])

    # Paragraph 4: closing (custom user value wins; otherwise generate tailored close)
    custom_closing = closing_block.strip()
    default_closing = _build_tailored_closing(
        company_name=company_name,
        job_title=job_title,
        role_type=effective_role,
        keywords=keywords,
    )
    closing = custom_closing if custom_closing and custom_closing != _DEFAULT_CLOSING else default_closing

    letter = "\n\n".join(p.strip() for p in [opening, philosophy, credentials, closing] if p.strip())
    return clean_cover_letter_output(letter, "")


def build_fit_summary(
    role_type: str,
    keywords: List[str],
    job_title: str,
    company_name: str,
) -> str:
    """Return a short analyst-style fit summary (3-5 sentences)."""
    effective_role = role_type if role_type in _FIT_SUMMARIES else SOFTWARE_ENGINEER
    return _FIT_SUMMARIES[effective_role]
