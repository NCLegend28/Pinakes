# AI Video Pipeline

Vision, audio, and video generation pipeline (see [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md) and [docs/SYSTEM_ARCHITECTURE.md](docs/SYSTEM_ARCHITECTURE.md)).

## Step 1: Vision Processing Pipeline (current)

- **Goal:** Input video → structured JSON (object labels, scene descriptions, key frames).
- **API:** `POST /v1/vision` with a video file.
- **Deliverable:** [docs/STEP1_DELIVERABLE.md](docs/STEP1_DELIVERABLE.md) — how to run, test with a 10-second video, and verify success.

### Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export VISION_PROVIDER=mock   # or openai + OPENAI_API_KEY
python run.py
# Then: curl -X POST http://127.0.0.1:8000/v1/vision -F "video=@tmp/test_10s.mp4"
```

Create a 10s test video: `./scripts/make_test_video.sh tmp/test_10s.mp4` (requires FFmpeg).

### Tests

```bash
PYTHONPATH=. python -m pytest tests/ -v
```
