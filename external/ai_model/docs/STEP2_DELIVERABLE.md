# Step 2 Deliverable: Audio Intelligence Layer

**Goal:** Extract speech → Generate speech.

**Success metric:** Transcription WER < 10%; TTS sounds human-like.

---

## What Was Delivered

1. **STT (Speech-to-Text)**
   - Adapters: Deepgram Nova-2 (real) and mock (no API key).
   - `POST /v1/audio/transcribe`: upload audio file → JSON with `text`, optional `wer` if `reference` query param is provided.

2. **TTS (Text-to-Speech)**
   - Adapters: ElevenLabs (real) and mock (silent WAV).
   - `POST /v1/audio/synthesize`: JSON body `{"text": "..."}` → response body is audio (mp3 or wav).

3. **WER (Word Error Rate)**
   - `audio/wer.py`: `word_error_rate(reference, hypothesis)` for Step 2 success metric (WER < 0.10).
   - Transcribe endpoint accepts optional query param `reference`; response then includes `wer`.

4. **Project layout (Step 2)**
   - `audio/` — `schema.py`, `wer.py`, `adapters/` (stt_base, stt_mock, stt_deepgram, tts_base, tts_mock, tts_elevenlabs).
   - Config: `STT_PROVIDER`, `TTS_PROVIDER`, `DEEPGRAM_API_KEY`, `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID` (optional).

---

## How to Run

### Prerequisites

- Python 3.10+, same venv as Step 1.
- For real APIs: Deepgram API key, ElevenLabs API key.

### Install (includes Step 2 deps)

```bash
pip install -r requirements.txt
```

### Env (optional)

```bash
# Mock both (no keys)
export STT_PROVIDER=mock
export TTS_PROVIDER=mock

# Or real APIs
export STT_PROVIDER=deepgram
export TTS_PROVIDER=elevenlabs
export DEEPGRAM_API_KEY=...
export ELEVENLABS_API_KEY=...
```

Start server: `python run.py`

---

## How to Test (Step 2 success metrics)

### 1. Transcribe (30 seconds of speech)

**With mock:**

```bash
# Create 30s silent audio (or use any short audio file)
ffmpeg -y -f lavfi -i anullsrc=r=44100:cl=stereo -t 30 -acodec libmp3lame tmp/30s.mp3

curl -X POST "http://127.0.0.1:8000/v1/audio/transcribe" \
  -F "audio=@tmp/30s.mp3"
```

**With reference (for WER):**  
Record yourself saying a known script (e.g. 30 seconds), save as `my_30s.mp3`. Then:

```bash
curl -X POST "http://127.0.0.1:8000/v1/audio/transcribe?reference=Your+exact+script+here" \
  -F "audio=@my_30s.mp3"
```

Response includes `wer`. **Success:** `wer < 0.10` (i.e. < 10%).

### 2. Synthesize (TTS)

```bash
curl -X POST "http://127.0.0.1:8000/v1/audio/synthesize" \
  -H "Content-Type: application/json" \
  -d '{"text": "The quick brown fox jumps over the lazy dog."}' \
  --output tmp/tts_out.mp3
```

Play `tmp/tts_out.mp3`. **Success:** TTS sounds human-like (with ElevenLabs; mock is silent WAV).

### 3. Full Step 2 workflow (transcribe → synthesize)

1. Record ~30 seconds of speech → save as `recorded.mp3`.
2. Transcribe: `POST /v1/audio/transcribe` with `audio=@recorded.mp3` → get `text`.
3. Synthesize: `POST /v1/audio/synthesize` with `{"text": "<paste transcript>"}` → save response as `regenerated.mp3`.
4. Compare: listen to original vs regenerated; verify transcription accuracy and that TTS sounds natural.

---

## Files Touched (Step 2)

| Path | Purpose |
|------|--------|
| `core/config.py` | `stt_provider`, `tts_provider`, API keys, `elevenlabs_voice_id` |
| `audio/schema.py` | `TranscribeResult`, `SynthesizeRequest`, `SynthesizeResult` |
| `audio/wer.py` | `word_error_rate`, `normalize_for_wer` |
| `audio/adapters/stt_base.py` | STT protocol |
| `audio/adapters/stt_mock.py` | Mock STT |
| `audio/adapters/stt_deepgram.py` | Deepgram Nova-2 |
| `audio/adapters/tts_base.py` | TTS protocol |
| `audio/adapters/tts_mock.py` | Mock TTS (silent WAV) |
| `audio/adapters/tts_elevenlabs.py` | ElevenLabs TTS |
| `app/main.py` | `POST /v1/audio/transcribe`, `POST /v1/audio/synthesize` |
| `requirements.txt` | `deepgram-sdk`, `elevenlabs` |
| `tests/test_audio_step2.py` | Schema, mock adapters, WER |
| `docs/STEP2_DELIVERABLE.md` | This deliverable |

Step 2 is complete when transcribe returns text (and WER < 10% when reference is provided) and synthesize returns playable, human-like audio with real providers.
