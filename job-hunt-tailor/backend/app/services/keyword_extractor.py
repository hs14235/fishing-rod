"""Extract relevant technical keywords from a job description.

Uses a curated keyword list matched against the input text.
Returns only terms that appear in the job description — nothing fabricated.
Capped at 20 results to keep the list scannable.
"""

from __future__ import annotations

import re
from typing import List

# Ordered from most specific to most generic so the best match surfaces first.
_TECH_TERMS: List[str] = [
    # Languages
    "Python", "Java", "JavaScript", "TypeScript", "Go", "Golang", "Rust",
    "C++", "C#", "Ruby", "Swift", "Kotlin", "Scala", "SQL", "HTML5", "CSS",
    # Backend frameworks / runtimes
    "FastAPI", "Django", "Flask", "Spring Boot", "Spring", "Node.js", "Express",
    "Rails", "Laravel",
    # Frontend
    "React", "Angular", "Vue", "Next.js", "Svelte", "Redux", "Vite",
    # Databases
    "PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite", "Cassandra",
    "DynamoDB", "Elasticsearch",
    # Cloud / infra
    "AWS", "GCP", "Azure", "Docker", "Kubernetes", "Terraform",
    "GitHub Actions", "CI/CD", "Linux",
    # AI / ML
    "machine learning", "deep learning", "LLM", "NLP", "TensorFlow", "PyTorch",
    "scikit-learn", "OpenAI", "LangChain", "RAG", "embeddings",
    "FAISS", "Sentence-Transformers", "Ollama",
    # 3-D / media
    "Blender", "Unreal Engine",
    # API / architecture patterns
    "REST", "GraphQL", "gRPC", "microservices", "distributed systems",
    "system design", "data modeling", "ORM",
    # Auth / security
    "OAuth", "JWT", "authentication", "authorization",
    # Testing / process
    "unit testing", "integration testing", "TDD", "Agile", "Scrum",
    # Messaging
    "Kafka", "RabbitMQ",
    # Tools
    "Git", "GitHub", "Postman", "Jira",
]

# Lower-cased set for fast membership checks
_TERMS_LOWER: dict[str, str] = {t.lower(): t for t in _TECH_TERMS}


def extract_keywords(job_description: str, job_title: str = "") -> List[str]:
    """Return tech keywords found in *job_description* + *job_title*."""
    combined = (job_description + " " + job_title).lower()

    found: List[str] = []
    seen: set[str] = set()

    for lower_term, display_term in _TERMS_LOWER.items():
        # Use word-boundary aware search; allow slashes for C++, C#
        pattern = r"(?<![a-zA-Z0-9])" + re.escape(lower_term) + r"(?![a-zA-Z0-9])"
        if re.search(pattern, combined) and lower_term not in seen:
            found.append(display_term)
            seen.add(lower_term)

    # Preserve insertion order (roughly by specificity), cap at 20
    return found[:20]
