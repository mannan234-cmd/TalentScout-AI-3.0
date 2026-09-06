# TalentScout AI 3.0

Intelligent, multi-agent student discovery & career-matching platform —
built for **every field, not just Computer Science**. AI agents
generate advisory recommendations; a human reviewer must explicitly Approve a
candidate before the Matching & Application Support stages run.

## Hackathon Pitch: Inclusive Across Fields

Most "AI talent matching" demos only work for CS/tech students because the
skill vocabulary is tech-only. TalentScout AI's Discovery, Evidence &
Signals, and Matching agents run on a **cross-field vocabulary** spanning
Software & AI, Business & Marketing, Design & Creative Media, Healthcare,
Education, Law, Agriculture, and Hospitality — so a Business, Design, or
Healthcare student gets the same quality of AI analysis and matching as a
Computer Science student. Two seeded demo accounts prove this:

- `sara@student.com` — BS Computer Science student → matched to Data
  Analyst / Python Developer opportunities.
- `ayesha@student.com` — BBA Marketing student → matched to a Digital
  Marketing Internship at 91.8% (100% required-skill coverage), proving
  the pipeline isn't tech-biased.

(Password for both: `student123`)

## Quick Start (Demo Mode — no external services required)

Demo mode uses an in-memory data store and a rule-based "AI" provider, so the
whole platform runs immediately with zero API keys.

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example ../.env      # already done if you unzipped as-is
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

Demo login accounts (seeded automatically):
- Admin:   admin@talentscout.ai  / admin123
- Student: sara@student.com      / student123

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:5173

## Switching to real services

- Set `DATA_PROVIDER=supabase` and fill in `SUPABASE_URL` / `SUPABASE_KEY` to
  persist data in Supabase (Postgres) instead of memory.
- Set `AI_PROVIDER=groq` and fill in `GROQ_API_KEY` to have the Evidence &
  Signals Agent and Application Agent use a real LLM (Groq) instead of the
  rule-based demo logic.

Both providers implement the same interface (`base_provider.py` /
`agents` call the provider, never a specific vendor), so swapping is a
one-line `.env` change — no code changes required.

## Pipeline

1. **Discovery Agent** — filters/categorizes new student submissions.
2. **Evidence & Signals Agent** — extracts technical signals from profile +
   evidence text.
3. Pipeline **pauses** — status becomes `pending_review`. Nothing further
   happens until an admin/reviewer clicks **Approve** in Human Review.
4. **Matching Agent** — (only after approval) scores the candidate against
   all active opportunities.
5. **Application Agent** — (only for shortlisted matches) drafts a tailored
   cover letter / application packet.
6. **Send Application (real email)** — the student connects their own Gmail
   account with a Gmail App Password (myaccount.google.com/apppasswords —
   not OAuth, not their real password) and clicks **Send Application**.
   TalentScout AI then sends a real SMTP email, from the student's own
   Gmail account, to the opportunity's contact address, with the
   AI-generated cover letter as the body. This is a genuine send, not a
   simulation — see `backend/app/services/email_service.py`.

   Notes for the demo: the seeded sample opportunities use
   `*.example.com` contact addresses on purpose (so nothing gets emailed
   to a real company by accident) — replace `contact_email` on an
   opportunity with a real address to test an actual send. The app
   password is kept only in the in-memory demo store for the life of the
   process; a production build should swap this for Gmail OAuth2 and an
   encrypted secrets store instead of a shared app password.

Real-time-ish analytics (Total Students, Pending Reviews, High-Potential
Candidates, Active Opportunities, Approved Matches) are exposed via
`GET /api/analytics` and polled by the frontend `RealtimeBanner`.
