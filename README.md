# dodi-web: score a Terms of Service in your browser

**Paste a ToS, get its DODI score. Live at [dodi-web.onrender.com](https://dodi-web.onrender.com/).** The Digital Ownership Deception Index (0&ndash;100) measures how hard a document works to hide that "Buy now" means "revocable licence". Higher is more deceptive.

The free tier sleeps when idle, so the first request after a quiet spell takes about 30 seconds to wake the service.

This is the deployed companion to [dodi-analysis](https://github.com/Axwolf13/dodi-analysis), the study that scored ten platforms across a decade of ToS snapshots. Read the [write-up](https://axwolf13.github.io/writing/dodi/) for the findings and the validation against ToS;DR. The scorer here is byte-for-byte the same math: deterministic, no LLM, no API calls, nothing stored.

```
DODI = 0.25 x readability penalty + 0.50 x licence ratio + 0.25 x red-flag score
```

## Run it locally

```sh
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://localhost:8000. Interactive API docs at http://localhost:8000/docs.

## Or with Docker

```sh
docker build -t dodi-web .
docker run -p 8000:8000 dodi-web
```

The container respects `PORT`, so it deploys unchanged to Render, Fly.io or Hugging Face Spaces.

## API

One endpoint does the work:

```sh
curl -X POST http://localhost:8000/api/score \
  -H "Content-Type: application/json" \
  -d '{"text": "You are granted a limited, revocable license to access the service..."}'
```

Response: the total score, the three weighted components (licence ratio, readability, red flags) and the raw counts behind them. `GET /api/health` for monitoring.

## Tests

```sh
pytest
```

Covers the scorer (determinism, weighting, bounds, the zero-ownership edge case) and the API (validation, error paths). CI runs the suite on every push via GitHub Actions.

## Honest limitations

Same as the study: keyword counting has no sense of negation, the score is gameable by padding a document with ownership words and it measures language, not legal substance. Treat the number as a signal, not a verdict.

---

Akshay A · [axwolf13.github.io](https://axwolf13.github.io/)
