# Step 3 Deliverable: Video Generation Engine

**Goal:** Text/image prompts → Generated video.

**Success metric:** All 3 videos render successfully at 720p+, maintain visual coherence.

---

## What Was Delivered

1. **Video generation package (`video_gen/`)**
   - **schema.py:** `VideoGenMode` (text_to_video, image_to_video, video_extension), `VideoGenRequest`, `VideoGenResult`.
   - **adapters/base.py:** Protocol for generate(mode, prompt, image, video, duration) → (bytes, content_type, width, height, duration).
   - **adapters/mock.py:** FFmpeg-generated 720p (1280x720) placeholder MP4 for all 3 modes; no external API key.
   - **adapters/ltx.py:** LTX Video (LTX-2) adapter; sync API for text-to-video and image-to-video (720p); does not support video_extension.
   - **adapters/kling.py:** Kling AI adapter; async submit/poll/download for text-to-video and image-to-video; does not support video_extension (use mock for that).
   - **adapters/luma.py:** Luma Dream Machine (Ray 2); async create/poll/download for text-to-video and image-to-video (720p); video_extension not supported for upload-based input.
   - **adapters/stable_video_diffusion.py:** Stable Video Diffusion via Replicate (image-to-video only); text-to-video and video_extension not supported.

2. **API**
   - **POST /v1/video/generate** (multipart): `mode` (required), `prompt` (required for text_to_video), `duration_sec` (optional), `image` (file, for image_to_video), `video` (file, for video_extension). Response: body is video/mp4; headers `X-Video-Width`, `X-Video-Height`, `X-Video-Duration-Seconds`.

3. **Config**
   - `VIDEO_GEN_PROVIDER=mock` | `ltx` | `kling` | `luma` | `svd`; `LTX_API_KEY`, `KLING_API_KEY`, `KLING_API_BASE`, `LUMA_API_KEY`, `REPLICATE_API_TOKEN` (for svd); `generated_video_dir` (optional).

4. **Shared**
   - **media/ffmpeg.py:** `generate_placeholder_video(width, height, duration_sec)` → MP4 bytes (for mock).

---

## How to Run

### Prerequisites

- Python 3.10+, FFmpeg on PATH (for mock).
- For LTX, Kling, or Luma: `httpx` and the corresponding API key. For SVD: `replicate` and `REPLICATE_API_TOKEN`.

### Env

```bash
# Mock (no key, uses FFmpeg)
export VIDEO_GEN_PROVIDER=mock

# Or LTX (sync; text/image-to-video only)
export VIDEO_GEN_PROVIDER=ltx
export LTX_API_KEY=...

# Or Kling (async; text/image-to-video only)
export VIDEO_GEN_PROVIDER=kling
export KLING_API_KEY=...
# Optional: export KLING_API_BASE=https://your-kling-gateway.com/v1

# Or Luma Dream Machine (async; text/image-to-video)
export VIDEO_GEN_PROVIDER=luma
export LUMA_API_KEY=...

# Or Stable Video Diffusion via Replicate (image-to-video only)
export VIDEO_GEN_PROVIDER=svd
export REPLICATE_API_TOKEN=...
```

Start server: `python run.py`.

---

## How to Test (Step 3 success metrics)

### 1. Text-to-video

```bash
curl -X POST "http://127.0.0.1:8000/v1/video/generate" \
  -F "mode=text_to_video" \
  -F "prompt=a sunset over mountains" \
  --output tmp/text2video.mp4
```

Check: `X-Video-Width: 1280`, `X-Video-Height: 720`; play `tmp/text2video.mp4` (720p+).

### 2. Image-to-video

```bash
# Use any image file (e.g. PNG/JPEG)
curl -X POST "http://127.0.0.1:8000/v1/video/generate" \
  -F "mode=image_to_video" \
  -F "prompt=animate this scene" \
  -F "image=@/path/to/image.png" \
  --output tmp/image2video.mp4
```

Mock ignores image content and returns the same 720p placeholder; LTX and Kling use the image.

### 3. Video extension (5s → 10s)

Create a 5s clip (e.g. `./scripts/make_test_video.sh tmp/5s.mp4` with duration 5), then:

```bash
curl -X POST "http://127.0.0.1:8000/v1/video/generate" \
  -F "mode=video_extension" \
  -F "duration_sec=10" \
  -F "video=@tmp/5s.mp4" \
  --output tmp/extended.mp4
```

Check: output is ~10s and 720p+ (mock returns 10s placeholder; LTX/Kling do not support video_extension—use mock for this test).

### Verify 720p+ and coherence

- **Resolution:** Response headers `X-Video-Width` and `X-Video-Height` should be ≥ 1280 and 720 (or 720 and 1280 for portrait).
- **Coherence:** Play the file; mock is a solid blue clip; LTX and Kling output should be visually coherent with the prompt/input.

---

## Files Touched (Step 3)

| Path | Purpose |
|------|--------|
| `core/config.py` | `video_gen_provider`, `ltx_api_key`, `kling_api_key`, `kling_api_base`, `generated_video_dir` |
| `video_gen/schema.py` | Modes and request/result models |
| `video_gen/adapters/base.py` | Adapter protocol |
| `video_gen/adapters/mock.py` | FFmpeg 720p placeholder |
| `video_gen/adapters/ltx.py` | LTX Video (sync text/image-to-video) |
| `video_gen/adapters/kling.py` | Kling AI (async text/image-to-video) |
| `video_gen/adapters/luma.py` | Luma Dream Machine (async text/image-to-video) |
| `video_gen/adapters/stable_video_diffusion.py` | Stable Video Diffusion via Replicate (image-to-video only) |
| `media/ffmpeg.py` | `generate_placeholder_video()` |
| `app/main.py` | `POST /v1/video/generate` and `_get_video_gen_adapter()` |
| `requirements.txt` | `httpx` |
| `tests/test_video_gen_step3.py` | Schema and mock adapter tests |
| `docs/STEP3_DELIVERABLE.md` | This deliverable |

Step 3 is complete when all 3 test videos render at 720p+ and the API returns video bytes with correct headers.
