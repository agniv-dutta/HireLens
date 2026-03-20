import json
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from utils import extract_text_from_pdf, extract_text_from_txt


RECOMMENDATIONS = {"Strong Fit", "Moderate Fit", "Not Fit"}
BACKEND_DIR = Path(__file__).resolve().parent


def _build_user_prompt(job_description, resume_text, resume_filename):
    """Build the user message asking the model for strict JSON output."""
    return (
        "Analyze the resume against the job description and return exactly one JSON object.\n"
        "Do not include any extra keys and ensure valid JSON.\n\n"
        f"Job Description:\n{job_description}\n\n"
        f"Resume Filename: {resume_filename}\n"
        f"Resume Text:\n{resume_text}\n"
    )


def _get_system_prompt():
    """Strict schema contract for model output."""
    return (
        "You are a resume screening engine.\n"
        "Return ONLY raw valid JSON with this exact schema and nothing else:\n"
        "{\n"
        '  "candidate_name": string,\n'
        '  "match_score": integer (0-100),\n'
        '  "strengths": [string, string, string],\n'
        '  "gaps": [string, string, string],\n'
        '  "recommendation": "Strong Fit" | "Moderate Fit" | "Not Fit",\n'
        '  "summary": string\n'
        "}\n"
        "Rules:\n"
        "- No markdown fences.\n"
        "- No preamble or explanations.\n"
        "- Output must be parseable JSON.\n"
        "- Keep summary to 1-2 sentences.\n"
        "- match_score must be an integer between 0 and 100.\n"
        "- strengths and gaps must each contain exactly 3 strings.\n"
    )


def _extract_resume_text(file_path):
    """Dispatch parser based on file extension."""
    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        return extract_text_from_pdf(file_path)
    if suffix == ".txt":
        return extract_text_from_txt(file_path)

    raise ValueError(f"Unsupported file type: {file_path.name}")


def _validate_candidate_schema(candidate, fallback_name):
    """Validate candidate payload and coerce common model mistakes safely."""
    if not isinstance(candidate, dict):
        raise ValueError("Candidate payload is not a JSON object.")

    cleaned = {
        "candidate_name": str(candidate.get("candidate_name", fallback_name)).strip() or fallback_name,
        "match_score": int(candidate.get("match_score", 0)),
        "strengths": candidate.get("strengths", []),
        "gaps": candidate.get("gaps", []),
        "recommendation": str(candidate.get("recommendation", "Not Fit")),
        "summary": str(candidate.get("summary", "No summary generated.")).strip(),
    }

    cleaned["match_score"] = max(0, min(100, cleaned["match_score"]))

    if not isinstance(cleaned["strengths"], list):
        cleaned["strengths"] = []
    if not isinstance(cleaned["gaps"], list):
        cleaned["gaps"] = []

    cleaned["strengths"] = [str(item).strip() for item in cleaned["strengths"] if str(item).strip()][:3]
    cleaned["gaps"] = [str(item).strip() for item in cleaned["gaps"] if str(item).strip()][:3]

    while len(cleaned["strengths"]) < 3:
        cleaned["strengths"].append("Not specified")
    while len(cleaned["gaps"]) < 3:
        cleaned["gaps"].append("Not specified")

    if cleaned["recommendation"] not in RECOMMENDATIONS:
        score = cleaned["match_score"]
        if score >= 75:
            cleaned["recommendation"] = "Strong Fit"
        elif score >= 45:
            cleaned["recommendation"] = "Moderate Fit"
        else:
            cleaned["recommendation"] = "Not Fit"

    if not cleaned["summary"]:
        cleaned["summary"] = "Summary not available."

    return cleaned


def _screen_single_resume(client, model, job_description, resume_path):
    """Call Groq for one resume and return validated candidate JSON."""
    resume_text = _extract_resume_text(resume_path)

    if not resume_text:
        raise ValueError(f"Resume appears empty: {resume_path.name}")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": _get_system_prompt(),
            },
            {
                "role": "user",
                "content": _build_user_prompt(job_description, resume_text, resume_path.name),
            },
        ],
        temperature=0.2,
    )

    response_text = ((response.choices[0].message.content) or "").strip()

    if not response_text.strip():
        raise ValueError(f"Empty model response for {resume_path.name}")

    try:
        candidate = json.loads(response_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Model returned invalid JSON for {resume_path.name}: {exc}") from exc

    fallback_name = resume_path.stem.replace("_", " ").replace("-", " ").strip() or "Unknown"
    return _validate_candidate_schema(candidate, fallback_name=fallback_name)


def run_screening(
    resumes_dir="data/resumes",
    jd_path="data/jd.txt",
    model="llama-3.3-70b-versatile",
):
    """Screen all resumes in a directory and return sorted candidate results plus errors."""
    # Always load the backend .env file regardless of current working directory.
    load_dotenv(BACKEND_DIR / ".env")

    model = os.getenv("GROQ_MODEL", model).strip() or model

    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key or api_key == "your_key_here":
        raise RuntimeError(
            "GROQ_API_KEY is missing or placeholder in backend/.env. "
            "Please set a valid API key."
        )

    client = Groq(api_key=api_key)

    jd_file = Path(jd_path)
    if not jd_file.is_absolute():
        jd_file = BACKEND_DIR / jd_file
    if not jd_file.exists():
        raise FileNotFoundError(f"Job description file not found: {jd_file}")

    job_description = jd_file.read_text(encoding="utf-8").strip()
    if not job_description:
        raise ValueError("Job description file is empty. Please update backend/data/jd.txt.")

    resumes_path = Path(resumes_dir)
    if not resumes_path.is_absolute():
        resumes_path = BACKEND_DIR / resumes_path
    if not resumes_path.exists() or not resumes_path.is_dir():
        raise FileNotFoundError(f"Resumes folder not found: {resumes_path}")

    supported_files = sorted(
        [p for p in resumes_path.iterdir() if p.is_file() and p.suffix.lower() in {".pdf", ".txt"}]
    )

    if not supported_files:
        raise ValueError("No supported resume files found in backend/data/resumes (expected .pdf or .txt).")

    results = []
    errors = []

    for resume_file in supported_files:
        try:
            candidate = _screen_single_resume(
                client=client,
                model=model,
                job_description=job_description,
                resume_path=resume_file,
            )
            results.append(candidate)
        except Exception as exc:
            # Continue processing remaining files while recording the failure.
            errors.append({"file": resume_file.name, "error": str(exc)})

    sorted_results = sorted(results, key=lambda item: item.get("match_score", 0), reverse=True)
    return sorted_results, errors
