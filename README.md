# HireLens

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![Groq](https://img.shields.io/badge/Groq%20API-Llama%203.3-purple?logo=llama)
![React](https://img.shields.io/badge/React-19.2-blue?logo=react&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-8.0-646cff?logo=vite&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-3.4-06b6d4?logo=tailwindcss&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-20+-green?logo=node.js&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

## Overview

**HireLens** is an AI-powered resume screening system that automatically evaluates and ranks candidate resumes against a job description using the Groq API. It combines a Python backend for intelligent resume analysis with a modern React frontend dashboard for intuitive candidate evaluation.

### Key Features
- 🤖 AI-powered resume screening using Groq's Llama 3.3 model
- 📄 Support for PDF and TXT resume formats
- 📊 Real-time candidate ranking and scoring (0-100)
- 🎯 Automated fit classification (Strong Fit, Moderate Fit, Not Fit)
- 💾 JSON and CSV output formats for integration
- 🎨 Beautiful React dashboard with filtering and sorting
- ⚡ Live API server for on-demand screening
- 🔒 Environment variable-based configuration (never hardcoded secrets)
- ✅ Graceful error handling (bad files don't stop batch processing)

---

## Technology Stack

### Backend
- **Python 3.13** — Core language
- **Groq API** — LLM for resume analysis
- **pdfplumber** — PDF text extraction
- **python-dotenv** — Environment variable management
- **rich** — Terminal UI for results table
- **http.server** — Lightweight API server

### Frontend
- **React 19.2** — UI framework
- **Vite 8.0** — Build tool and dev server
- **Tailwind CSS 3.4** — Styling
- **JavaScript (ES6+)** — Client-side logic

### DevOps
- **Node.js 20+** — JavaScript runtime
- **npm** — Package management
- **Git** — Version control

---

## Project Structure

```
HireLens/
├── 📂 backend/                          # Python resume screening pipeline
│   ├── main.py                          # Entry point; runs screening & displays results
│   ├── screener.py                      # Groq API integration & resume analysis
│   ├── server.py                        # HTTP API server (GET /api/results, POST /api/screen)
│   ├── utils.py                         # PDF/TXT parsing, JSON/CSV output
│   ├── requirements.txt                 # Python dependencies
│   ├── .env                             # GROQ_API_KEY configuration
│   │
│   ├── 📂 data/
│   │   ├── jd.txt                       # Job description (paste target JD here)
│   │   └── 📂 resumes/                  # Resume files (.pdf or .txt)
│   │       ├── alex_carter.txt
│   │       ├── priya_sharma.txt
│   │       ├── meera_pillai.txt
│   │       ├── liam_obrien.txt
│   │       ├── raj_kumar.txt
│   │       ├── nina_gupta.txt
│   │       ├── marco_rossi.txt
│   │       └── sophie_davis.txt
│   │
│   └── 📂 output/
│       ├── results.json                 # Ranked candidates (consumed by frontend)
│       └── results.csv                  # Spreadsheet-friendly export
│
├── 📂 frontend/                         # React dashboard
│   ├── index.html                       # HTML entry point
│   ├── vite.config.js                   # Vite config (includes /api proxy)
│   ├── tailwind.config.js               # Tailwind CSS configuration
│   ├── package.json                     # Node dependencies
│   │
│   ├── 📂 src/
│   │   ├── App.jsx                      # Main component (loads & displays results)
│   │   ├── index.css                    # Global styles
│   │   │
│   │   ├── 📂 components/
│   │   │   ├── Header.jsx               # Dashboard header
│   │   │   ├── SummaryBar.jsx           # Stats cards (total, strong fit, avg score)
│   │   │   ├── FilterBar.jsx            # Filter & sort controls
│   │   │   └── CandidateCard.jsx        # Individual candidate card
│   │   │
│   │   └── 📂 data/
│   │       └── results.json             # Local fallback data (for development)
│   │
│   ├── 📂 public/                       # Static assets
│   └── .gitignore                       # Frontend ignore rules
│
├── .gitignore                           # Project ignore rules
├── README.md                            # This file
└── .venv/                               # Python virtual environment (created after setup)
```

---

## Setup Instructions

### Prerequisites
- Python 3.13+
- Node.js 20+ & npm
- Active Groq API key (get one at [console.groq.com](https://console.groq.com))

### 1. Backend Setup

#### Clone/Initialize
```bash
cd HireLens
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r backend/requirements.txt
```

#### Configure Environment
Edit `backend/.env` and add your Groq API key:
```env
GROQ_API_KEY=your_actual_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

#### Add Data
1. **Job Description**: Paste your target job description in `backend/data/jd.txt`
2. **Resumes**: Drop `.pdf` or `.txt` files into `backend/data/resumes/`

### 2. Frontend Setup

```bash
cd frontend
npm install
```

No additional configuration needed—Vite automatically proxies `/api` requests to `http://127.0.0.1:8000`.

---

## Running the System

### Option A: Backend Only (CLI Mode)
Useful for quick screening or batch processing.

```bash
python backend/main.py
```

Output:
- Terminal: Ranked table of all candidates
- File: `backend/output/results.json` (95 total candidates with scores)
- File: `backend/output/results.csv` (spreadsheet-friendly)

### Option B: Full Stack (Recommended)
Run both backend API and frontend dashboard in separate terminals.

#### Terminal 1: Backend API Server
```bash
python backend/server.py
```
Output: `HireLens API server running on http://127.0.0.1:8000`

#### Terminal 2: Frontend Dev Server
```bash
cd frontend
npm run dev
```
Output: `VITE ready in XXXms ➜ Local: http://localhost:5173/`

#### Open Dashboard
Visit **http://localhost:5173** (or the URL shown in Terminal 2)

The frontend will:
- Fetch live candidate data from `/api/results`
- Display ranked dashboard with filtering and sorting
- Allow real-time screening updates

### Option C: Trigger Screening via API
From any terminal, post a screening request:

```bash
curl -X POST http://127.0.0.1:8000/api/screen
```

This will run the complete pipeline and update `results.json`.

---

## API Endpoints

### GET `/health`
Health check endpoint.
```bash
curl http://127.0.0.1:8000/health
```
Response: `{"status": "ok"}`

### GET `/api/results`
Fetch latest screening results.
```bash
curl http://127.0.0.1:8000/api/results
```
Response: Array of candidate objects with scores, strengths, gaps, and recommendations.

### POST `/api/screen`
Trigger a fresh screening run.
```bash
curl -X POST http://127.0.0.1:8000/api/screen
```
Response: `{"results": [...], "errors": [...]}`

---

## Output Schema

Each candidate in `results.json` has this structure:
```json
{
  "candidate_name": "Sophie Davis",
  "match_score": 95,
  "strengths": [
    "Extensive LLM API experience",
    "RAG system implementation",
    "Production-level prompt engineering"
  ],
  "gaps": [
    "No-code tool exposure limited",
    "Prefers AI-only projects",
    "Limited internship history"
  ],
  "recommendation": "Strong Fit",
  "summary": "Sophie Davis is a highly skilled AI/ML engineer with 1 year of LLM experience, making her a strong fit for the AI Automation Intern role."
}
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GROQ_API_KEY` | *(required)* | Your Groq API key from console.groq.com |
| `GROQ_MODEL` | `llama-3.3-70b-versatile` | Groq model to use for screening |
| `VITE_API_BASE_URL` | *(optional)* | Frontend API base URL for production deploys (example: `https://your-backend-domain.com`) |

For local development, `VITE_API_BASE_URL` is not required because Vite proxy forwards `/api/*` to `http://127.0.0.1:8000`.

---

## Example Workflow

1. **Prepare Data**
   ```bash
   # Edit job description
   nano backend/data/jd.txt
   
   # Copy resumes
   cp ~/Downloads/*.pdf backend/data/resumes/
   ```

2. **Run Screening**
   ```bash
   python backend/server.py  # Terminal 1
   cd frontend && npm run dev  # Terminal 2
   ```

3. **View Results**
   - Visit http://localhost:5173
   - Filter by "Strong Fit" or sort by score
   - Export as CSV if needed

---

## Output Files

After screening, check `backend/output/`:

- **results.json** — Machine-readable candidate rankings (consumed by frontend)
- **results.csv** — Human-readable spreadsheet with all candidate details

Both are automatically sorted by `match_score` (highest first).

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "GROQ_API_KEY is missing" | Add your API key to `backend/.env` |
| "No supported resume files found" | Ensure `.pdf` or `.txt` files are in `backend/data/resumes/` |
| "Failed to load results (502)" | Start backend API server: `python backend/server.py` |
| "Port 8000 already in use" | Change port in `server.py` or kill existing process |
| Frontend shows "Loading..." forever | Check browser console for errors; ensure backend server is running |
| Vite port 5173 in use | Vite will auto-increment to 5174, 5175, etc. |

---

## Development

### Frontend Development
- Edit React components in `frontend/src/`
- Vite auto-refreshes on save
- Check browser console for errors

### Backend Development
- Modify `screener.py` to adjust AI screening logic
- Restart `server.py` to pick up changes
- Test API endpoints with `curl` or Postman

### Adding New Resume Formats
Edit `utils.py` and `screener.py` to support additional file types (e.g., `.docx`).

---

## Security Notes

- API keys are loaded via `python-dotenv` and **never hardcoded**
- Resume data is processed in-memory; no persistent storage beyond output files
- Frontend is fully decoupled and reads only from `results.json`
- Errors in one resume do not stop batch processing

---

## Demo Video

Watch the HireLens walkthrough demo here:

https://youtu.be/xAFGYGVxfp4

---

## License

MIT

---

## Support

For issues, questions, or suggestions, please check the documentation or open an issue in the repository.
