"""Seed default UserProfileSettings on first startup.

Run once: if a settings row already exists it is not overwritten.
"""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models import UserProfileSettings

MASTER_PROFILE_TEXT = """\
Name: Hamza Salahuddin
Contact: 478-305-1808 | mazeadone@gmail.com | hs14235.github.io | linkedin.com/in/mazeadone

Education:
B.S. Computer Science, Georgia Southern University, Statesboro GA — Expected May 2026

Technical Skills:
Languages: Python, Java, JavaScript, SQL, HTML5, CSS
Backend: Django, Node.js, Spring, PostgreSQL, FastAPI
Frontend: React, Vite, Next.js
Tools & Databases: GitHub, Docker, Postman, DBeaver, VS Code

Leadership:
Vice President — Association for Computing Machinery (ACM), Georgia Southern University — Aug 2025–Present
- Led planning and execution of ACM events for 100+ students, increasing engagement and participation.

Work Experience:
Student Assistant — Georgia State University, Atlanta GA — Sep 2022–Dec 2024
- Led and trained a 10+ member team, improving order turnaround time and punctuality.

AI Model Generation Team Lead – Capstone, Gulfstream Aerospace Corporation, Savannah GA — Jan 2026–May 2026 (Expected)
- Leading a team building AI-driven scenarios tailored to client specifications for real-life interpretation.
- Used Meshy-generated 3D models pipelined for scaling and sizing through Blender, rendered into scenes using Unreal Engine 5.
- Collaborating with Gulfstream designers to translate custom client requirements into AI tasks.

Software Engineer (Full-Stack) – Trainline — Spring 2025–Present
- Developed a full-stack booking platform with REST APIs, role-based authentication, PostgreSQL schema, and responsive UI.
- Built modular React components covering dashboard, authenticated flows, seat selection, payments, notifications, and real-time chat.
- Normalized relational schema in PostgreSQL for improved data integrity; containerized with Docker for portability.

Projects:
Flight Booking Web App | PostgreSQL, HTML/CSS, Spring Boot | Fall 2024
- Designed a transactional booking system with authenticated user flows, normalized relational schema, and REST APIs.
- Implemented accessible UI patterns supporting user accommodations and meal data with strong data integrity.

meeting-to-tasks | FastAPI, Ollama (phi3:mini), GitHub Issues | Fall 2025
- Built a RAG-based system that converts meeting transcripts into GitHub Issues using FAISS + LLMs.
- Used Sentence-Transformers and FAISS local vector store for transcript understanding.
- Architected pluggable LLM backends supporting both local (Ollama) and hosted APIs.
"""

FIXED_PHILOSOPHY_TEXT = """\
I think about software in terms of where it is most likely to break — usually at the boundary \
between components, or in assumptions baked in early. That shapes how I build: get something \
working end-to-end quickly, even if it is rough, then tighten constraints and handle edge cases \
from a real foundation. I would rather ship a working system that needs polish than a polished \
design that has not been tested against real data.\
"""

STRENGTHS_BLOCK_TEXT = """\
I work best when I own a slice of the system end-to-end — from schema to API to UI if needed — \
and I surface blockers and tradeoffs early rather than quietly deferring them. I am adaptable \
across backend, full-stack, and AI-adjacent work, and most effective when the constraints are \
real and the edge cases matter.\
"""

CLOSING_BLOCK_TEXT = "I would welcome a chance to discuss this further. Thank you for your time."


def seed_default_settings(db: Session) -> None:
    existing = db.query(UserProfileSettings).first()
    if existing is not None:
        return

    settings = UserProfileSettings(
        master_profile_text=MASTER_PROFILE_TEXT,
        fixed_philosophy_text=FIXED_PHILOSOPHY_TEXT,
        strengths_block_text=STRENGTHS_BLOCK_TEXT,
        closing_block_text=CLOSING_BLOCK_TEXT,
        default_tone="balanced",
        default_emphasis="auto",
        updated_at=datetime.now(timezone.utc),
    )
    db.add(settings)
    db.commit()
