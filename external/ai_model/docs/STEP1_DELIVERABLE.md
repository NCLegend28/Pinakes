# Step 1 Deliverable: Vision Processing Pipeline

**Goal:** Input video → Extract visual understanding.

**Success metric:** API returns structured JSON with detected objects/scenes (object labels with timestamps, scene descriptions, key frame extractions).

---

## What Was Delivered

1. **Vision pipeline**
   - Video ingest: upload or file path.
   - Key-frame extraction via FFmpeg (configurable interval, default 1 frame/sec).
   - Vision API adapter (OpenAI GPT-4o Vision or mock).
   - Structured JSON response: `object_labels`, `scene_descriptions`, `key_frames`, `duration_sec`.

2. **API**
   - `POST /v1/vision` — body: multipart form with `video` file (e.g. `.mp4`, `.webm`, `.mov`). Response: `VisionResult` JSON.

3. **Project layout (Step 1 only)**
   - `app/` — FastAPI app and `/v1/vision` route.
   - `core/` — Config (env-based: `VISION_PROVIDER`, `OPENAI_API_KEY`).
   - `vision/` — Schema, adapters (OpenAI + mock), pipeline.
   - `media/` — FFmpeg key-frame extraction and duration probe.
   - `scripts/make_test_video.sh` — Generates a 10-second test video.

---

## How to Run

### Prerequisites

- Python 3.10+
- FFmpeg on PATH (`brew install ffmpeg` or equivalent)
- For real Vision API: OpenAI API key. For testing without: use mock.

### Install and run

```bash
cd /path/to/ai_model
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Option A — Mock (no API key)**

```bash
export VISION_PROVIDER=mock
python run.py
```

**Option B — OpenAI Vision**

```bash
export VISION_PROVIDER=openai
export OPENAI_API_KEY=sk-...
python run.py
```

Server runs at `http://127.0.0.1:8000`. Docs: `http://127.0.0.1:8000/docs`.

---

## How to Test (Step 1 success metric)

### 1. Create a 10-second test video

```bash
chmod +x scripts/make_test_video.sh
./scripts/make_test_video.sh tmp/test_10s.mp4
```

### 2. Call the API

**With mock (no key):**

```bash
curl -X POST http://127.0.0.1:8000/v1/vision \
  -F "video=@tmp/test_10s.mp4"
```

**With OpenAI:** same curl; ensure `VISION_PROVIDER=openai` and `OPENAI_API_KEY` are set.

### 3. Verify response

You should get JSON like:

- `object_labels`: list of `{ "label": "...", "timestamp_sec": 0.0, "confidence": ... }`
- `scene_descriptions`: list of `{ "description": "...", "start_sec": 0.0, "end_sec": 10.0 }`
- `key_frames`: list of `{ "timestamp_sec": 0.0, "path": "frame_0000.png", "scene_summary": "..." }`
- `duration_sec`: e.g. `10.0`

**Success:** API returns structured JSON with detected objects/scenes (and key frame extractions). If any of these lists are empty with the real API, the pipeline still “works”; for the mock, they are always populated.

---

## Optional: run vision pipeline from CLI

For a quick check without the server (mock only):

```bash
export VISION_PROVIDER=mock
export PYTHONPATH=.
python -c "
from pathlib import Path
from vision.pipeline import run_vision_pipeline
from vision.adapters.mock_adapter import MockVisionAdapter
from media.ffmpeg import extract_key_frames, get_video_duration_sec

video = Path('tmp/test_10s.mp4')
if not video.exists():
    print('Create test video first: ./scripts/make_test_video.sh')
    exit(1)
frames_dir = Path('tmp/frames')
frames_dir.mkdir(parents=True, exist_ok=True)
result = run_vision_pipeline(video, frames_dir, MockVisionAdapter(), 1.0)
print(result.model_dump_json(indent=2))
"
```

---

## Files Touched (Step 1)

| Path | Purpose |
|------|--------|
| `requirements.txt` | Dependencies |
| `core/config.py` | Settings from env |
| `media/ffmpeg.py` | Key-frame extraction, duration |
| `vision/schema.py` | `VisionResult`, `ObjectLabel`, `SceneDescription`, `KeyFrameExtraction` |
| `vision/adapters/base.py` | Adapter protocol |
| `vision/adapters/mock_adapter.py` | Sample JSON without API |
| `vision/adapters/openai_adapter.py` | GPT-4o Vision |
| `vision/pipeline.py` | Ingest → frames → adapter → result |
| `app/main.py` | FastAPI and `POST /v1/vision` |
| `run.py` | Server entrypoint |
| `scripts/make_test_video.sh` | 10s test video |
| `docs/STEP1_DELIVERABLE.md` | This deliverable |

Step 1 is complete when the above test passes and the API returns structured JSON as described.
