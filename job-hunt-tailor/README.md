# Job Hunt Tailor — v1.5

A focused, fast-to-use application for generating tightly targeted software
job application materials. Built for Hamza Salahuddin.

**Generates per job description:**
- Tailored cover letter draft (230–310 words, editable)
- Detected keywords (ATS alignment)
- Fit summary (honest, analyst-style)
- 3–8 resume bullet improvement suggestions

**No auth, no cloud, no vector database — just a local FastAPI backend and a
React frontend.**

---

## Architecture decisions

| Choice | Reason |
|---|---|
| FastAPI + SQLite | Fast local iteration; no infra to manage |
| Pydantic v2 schemas | Validation at API boundary only |
| Template provider (default) | Works immediately, no API key required |
| LLM provider (optional) | Drop-in improvement when `OPENAI_API_KEY` is set |
| React + Vite (no CSS framework) | Fast editing UX without bundle weight |
| Proxy via Vite dev server | No CORS config needed during development |

The generation pipeline is deterministic by default: `keyword_extractor →
role_classifier → project_selector → cover_letter_builder → resume_suggester`.
All content is grounded in Hamza's profile — nothing is fabricated.

---

## Requirements

- Python 3.11+
- Node.js 18+

---

## Setup

### 1. Clone

```bash
git clone <repo>
cd job-hunt-tailor
```

### 2. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Copy and configure environment:

```bash
cp .env.example .env
# Optional: add OPENAI_API_KEY to enable LLM-powered cover letters
```

### 3. Frontend

```bash
cd ../frontend
npm install
```

---

## Running

### Backend (from `job-hunt-tailor/backend/`)

```bash
uvicorn app.main:app --reload --port 8000
```

The server seeds Hamza's default profile on first startup.

API docs available at: http://localhost:8000/docs

### Frontend (from `job-hunt-tailor/frontend/`)

```bash
npm run dev
```

App available at: http://localhost:5173

---

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | /health | Health check |
| POST | /api/generate | Generate cover letter + suggestions |
| POST | /api/applications | Save application |
| GET | /api/applications | List applications (search, status filter) |
| GET | /api/applications/{id} | Get application |
| PUT | /api/applications/{id} | Update application |
| DELETE | /api/applications/{id} | Delete application |
| POST | /api/applications/{id}/regenerate | Regenerate from stored JD |
| GET | /api/settings | Get profile settings |
| PUT | /api/settings | Update profile settings |

---

## LLM integration

Set `OPENAI_API_KEY` in `.env` to enable LLM-powered cover letter generation.
The app falls back to the deterministic template engine on any API failure.

Any OpenAI-compatible API is supported — override `OPENAI_BASE_URL` for Azure,
Ollama, or other providers.

---

## Application statuses

`draft → applied → interview → rejected → archived`

---

## Quickest v2 upgrades

1. **Multi-tone templates** — have the template engine produce meaningfully
   different output for "concise" vs "technical" tones instead of passing
   tone to the LLM only
2. **Version history** — store a `GeneratedArtifact` table keyed to
   `application_id` + `created_at` so Hamza can compare past regenerations
3. **PDF export** — add `weasyprint` and a `/applications/{id}/export` endpoint
4. **Duplicate / fork application** — POST `/applications/{id}/fork` to start
   a new application pre-filled from an existing one
5. **Bulk keyword gap report** — compare detected keywords across all saved
   applications to surface terms missing from the resume consistently

---

## File structure

```
job-hunt-tailor/
  backend/
    app/
      main.py              FastAPI app + lifespan
      config.py            Settings (pydantic-settings)
      db.py                SQLAlchemy engine + session
      models.py            Application, UserProfileSettings
      schemas.py           Pydantic request/response models
      crud.py              DB operations
      seed.py              Default profile seeder
      routers/
        health.py
        generate.py
        applications.py
        settings.py
      services/
        keyword_extractor.py
        role_classifier.py
        project_selector.py
        cover_letter_builder.py
        resume_suggester.py
        generation_engine.py
        providers/
          base.py
          template_provider.py
          llm_provider.py
    requirements.txt
    .env.example
  frontend/
    src/
      App.jsx
      api.js
      index.css
      pages/
        Dashboard.jsx
        NewApplication.jsx
        ApplicationDetail.jsx
        Settings.jsx
    index.html
    package.json
    vite.config.js
  .gitignore
  README.md
```
