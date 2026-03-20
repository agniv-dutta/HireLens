# HireLens

HireLens is an AI-powered resume screening backend that compares resumes against a job description and produces ranked candidate outputs.

## Project Structure

```
HireLens/
├── backend/
│   ├── main.py
│   ├── screener.py
│   ├── utils.py
│   ├── data/
│   │   ├── resumes/        # drop .pdf or .txt resume files here
│   │   └── jd.txt          # paste job description here
│   ├── output/
│   │   ├── results.json    # structured output consumed by frontend
│   │   └── results.csv     # optional reference output
│   ├── requirements.txt
│   └── .env                # GROQ_API_KEY lives here
├── frontend/
│   └── placeholder.txt
└── README.md
```

## Setup

1. Create and activate a Python environment.
2. Install dependencies:

```bash
pip install -r backend/requirements.txt
```

3. Add your key in `backend/.env`:

```env
GROQ_API_KEY=your_real_key_here
```

4. Paste your target job description in `backend/data/jd.txt`.
5. Drop resumes (`.pdf` or `.txt`) into `backend/data/resumes/`.

## Run

```bash
python backend/main.py
```

## Integrated Frontend + Backend (Recommended)

Run backend API server in one terminal:

```bash
python backend/server.py
```

Run frontend app in another terminal:

```bash
cd frontend
npm run dev
```

The frontend fetches live data from `GET /api/results` via Vite proxy.

Optional: trigger a fresh screen run through API:

```bash
curl -X POST http://127.0.0.1:8000/api/screen
```

The backend will:
- Call Groq (`llama-3.3-70b-versatile`) for each resume
- Rank candidates by `match_score`
- Write output to `backend/output/results.json` and `backend/output/results.csv`
- Print a summary table in the terminal

## Notes

- API key is loaded via `python-dotenv`; it is never hardcoded.
- Errors are handled per file so one bad resume does not stop the whole batch.
- Frontend is decoupled and should only read `backend/output/results.json`.
