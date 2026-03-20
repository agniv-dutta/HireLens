import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from screener import run_screening
from utils import save_results_to_csv, save_results_to_json


BACKEND_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BACKEND_DIR / "output"
RESULTS_JSON_PATH = OUTPUT_DIR / "results.json"
RESULTS_CSV_PATH = OUTPUT_DIR / "results.csv"


def _read_results():
    """Read results.json if present, otherwise return an empty list."""
    if not RESULTS_JSON_PATH.exists():
        return []

    try:
        return json.loads(RESULTS_JSON_PATH.read_text(encoding="utf-8"))
    except Exception:
        # Keep the API resilient if a partial write ever occurs.
        return []


def _run_and_persist_screening():
    """Run screening pipeline and persist latest artifacts."""
    results, errors = run_screening()
    save_results_to_json(results, RESULTS_JSON_PATH)
    save_results_to_csv(results, RESULTS_CSV_PATH)
    return results, errors


class HireLensHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload, status=HTTPStatus.OK):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/health":
            self._send_json({"status": "ok"})
            return

        if self.path == "/api/results":
            self._send_json(_read_results())
            return

        self._send_json({"error": "Not found"}, status=HTTPStatus.NOT_FOUND)

    def do_POST(self):
        if self.path != "/api/screen":
            self._send_json({"error": "Not found"}, status=HTTPStatus.NOT_FOUND)
            return

        try:
            results, errors = _run_and_persist_screening()
            self._send_json({"results": results, "errors": errors})
        except Exception as exc:
            self._send_json({"error": str(exc)}, status=HTTPStatus.INTERNAL_SERVER_ERROR)


def run_server(host="127.0.0.1", port=8000):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer((host, port), HireLensHandler)
    print(f"HireLens API server running on http://{host}:{port}")
    print("GET /api/results")
    print("POST /api/screen")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
