from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.scorer import DODIAnalyzer

MAX_CHARS = 1_000_000  # ~200x a typical ToS; guards against abuse, not users

app = FastAPI(
    title="DODI",
    description="Digital Ownership Deception Index: score how hard a Terms of "
    "Service works to hide that 'Buy now' means 'revocable licence'.",
    version="1.1.0",
)
analyzer = DODIAnalyzer()
static_dir = Path(__file__).resolve().parent.parent / "static"


class ScoreRequest(BaseModel):
    text: str = Field(min_length=1, max_length=MAX_CHARS)


@app.post("/api/score")
def score(req: ScoreRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Document text is empty.")
    return analyzer.analyze(req.text)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(static_dir / "index.html")
