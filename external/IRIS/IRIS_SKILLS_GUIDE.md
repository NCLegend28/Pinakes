# IRIS Skills Guide
## Building and Attaching New Capabilities to Your Vision AI Assistant

---

## Recommended Skills Roadmap

The skills below are organized in **priority order** — build them in sequence, as each one builds on the last.

| # | Skill | Description | Difficulty |
|---|-------|-------------|------------|
| 1 | **Photo Storage & Recall** | Capture, name, and retrieve images from local device storage | ⭐ Beginner |
| 2 | **Session Memory** | Remember what was discussed and shown across conversations | ⭐ Beginner |
| 3 | **Note Taking** | Transcribe voice notes and save them with optional image attachments | ⭐ Beginner |
| 4 | **Object Identification & Tagging** | Detect, label, and log objects seen by the camera | ⭐⭐ Intermediate |
| 5 | **Text Recognition (OCR)** | Read text in the real world — labels, documents, whiteboards, screens | ⭐⭐ Intermediate |
| 6 | **Hand & Pose Tracking** | Track hand landmarks and body pose via MediaPipe (foundation for the trumpet glove project) | ⭐⭐ Intermediate |
| 7 | **Spatial Awareness** | Estimate distances, dimensions, and relationships between objects in frame | ⭐⭐ Intermediate |
| 8 | **Web Search Integration** | Allow IRIS to look things up in real time and report back verbally | ⭐⭐ Intermediate |
| 9 | **Project Journal** | Auto-document what IRIS sees over time into a searchable, timestamped log | ⭐⭐ Intermediate |
| 10 | **Gesture Commands** | Trigger actions (capture, reset, recall) via hand gestures instead of voice | ⭐⭐⭐ Advanced |
| 11 | **Face Recognition** | Recognize and greet known people (stored locally, never in the cloud) | ⭐⭐⭐ Advanced |
| 12 | **Pattern Learning** | Record, label, and classify repeated visual patterns — foundation for trumpet position learning | ⭐⭐⭐ Advanced |
| 13 | **MIDI / Audio Output** | Map detected hand positions to musical notes or MIDI signals for the glove instrument | ⭐⭐⭐ Advanced |
| 14 | **Offline Mode** | Fall back to a local LLM (e.g. Ollama) when no internet is available | ⭐⭐⭐ Advanced |

---

## How Skills Are Structured

Every skill in IRIS follows the same pattern. Think of each skill as a **plug-in module** — a self-contained Python file that exposes a clean interface to the AI brain.

```
iris/
├── main.py
├── ai_brain.py
├── skills/
│   ├── __init__.py
│   ├── photo_storage.py     ← each skill lives here
│   ├── session_memory.py
│   ├── ocr.py
│   └── hand_tracking.py
```

---

## Step-by-Step: Building a New Skill

### Step 1 — Create the skill file

Every skill file follows this template:

```python
# skills/your_skill_name.py

class YourSkillName:
    """
    One-line description of what this skill does.
    """

    def __init__(self):
        # Any setup — load models, open files, connect to APIs, etc.
        self.ready = True

    def your_main_method(self, input_data):
        """
        The primary action this skill performs.
        Returns a result that ai_brain.py can use.
        """
        pass

    def cleanup(self):
        """
        Release any resources (cameras, file handles, models).
        Called on shutdown.
        """
        pass
```

### Step 2 — Register the skill in `ai_brain.py`

Open `ai_brain.py` and import your new skill at the top:

```python
from skills.photo_storage import PhotoStorage
from skills.session_memory import SessionMemory
# add yours here
```

Then instantiate it inside `__init__`:

```python
class AIBrain:
    def __init__(self):
        self.photo_storage = PhotoStorage()
        self.session_memory = SessionMemory()
        # add yours here
```

### Step 3 — Wire it into the `think()` method

The `think()` method is where IRIS decides what to do with each input. Add your skill's logic here:

```python
def think(self, user_text: str, image_b64: str = None) -> str:

    # Example: auto-save image if user says "save this"
    if "save" in user_text.lower() and image_b64:
        label = self.extract_label(user_text)  # parse a name from speech
        self.photo_storage.save(image_b64, label=label)

    # Example: inject memory context into the prompt
    memory_context = self.session_memory.get_recent(n=5)

    # Then pass everything to Claude as usual
    response = self.client.messages.create(
        model="claude-opus-4-6",
        system=SYSTEM_PROMPT + memory_context,
        messages=self.conversation_history,
        ...
    )
```

### Step 4 — Add voice trigger phrases in `main.py`

Skills can be triggered by voice commands in the main loop:

```python
# In main.py, inside the while True loop:

if "save this" in lower_text and image_b64:
    result = self.brain.photo_storage.save(image_b64)
    self.voice.speak(f"Got it. Saved as {result['filename']}.")
    continue

if "show me" in lower_text:
    label = lower_text.replace("show me", "").strip()
    image = self.brain.photo_storage.recall(label)
    # display on screen
    continue
```

### Step 5 — Clean up on shutdown

In `main.py`, add your skill's cleanup call alongside the existing ones:

```python
# At the bottom of run(), after the while loop:
self.eyes.cleanup()
self.brain.photo_storage.cleanup()
self.brain.your_skill.cleanup()
```

---

## Worked Example: Photo Storage Skill

Here is a complete, ready-to-use implementation of Skill #1:

```python
# skills/photo_storage.py
import os
import base64
import json
from datetime import datetime
from pathlib import Path

class PhotoStorage:
    """
    Save, retrieve, and list photos captured by IRIS.
    Photos are stored locally with metadata for recall by label or date.
    """

    def __init__(self, storage_dir: str = "iris_photos"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.index_file = self.storage_dir / "index.json"
        self.index = self._load_index()

    def _load_index(self) -> dict:
        if self.index_file.exists():
            with open(self.index_file, "r") as f:
                return json.load(f)
        return {}

    def _save_index(self):
        with open(self.index_file, "w") as f:
            json.dump(self.index, f, indent=2)

    def save(self, image_b64: str, label: str = None) -> dict:
        """Save a base64 image to disk and record it in the index."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        label = label or f"photo_{timestamp}"
        filename = f"{label}_{timestamp}.jpg"
        filepath = self.storage_dir / filename

        with open(filepath, "wb") as f:
            f.write(base64.b64decode(image_b64))

        self.index[label] = {
            "filename": filename,
            "filepath": str(filepath),
            "timestamp": timestamp,
            "label": label
        }
        self._save_index()
        return self.index[label]

    def recall(self, label: str) -> str | None:
        """Retrieve a saved photo as base64 by label. Returns None if not found."""
        # Fuzzy match — find closest label
        match = next((v for k, v in self.index.items() if label.lower() in k.lower()), None)
        if not match:
            return None
        with open(match["filepath"], "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def list_photos(self) -> list:
        """Return a list of all saved photo labels and timestamps."""
        return [
            {"label": v["label"], "timestamp": v["timestamp"]}
            for v in self.index.values()
        ]

    def cleanup(self):
        pass  # Nothing to release
```

---

## Tips for Building Skills That Work Well With Voice

- **Return strings whenever possible.** The AI brain can speak any string directly.
- **Keep methods focused.** One method = one thing. `save()`, `recall()`, `list()` — not one giant `handle_photo()`.
- **Handle failures gracefully.** If a skill fails, it should return a string IRIS can speak: `"I couldn't find that photo."` rather than crashing.
- **Think in spoken English.** Before finalizing a skill, ask: *what would IRIS say when this runs?* Design the return values around that.
- **Log everything to a file**, not just the terminal. On a Pi with no monitor attached, file logs are your only visibility into what's happening.

---

## What's Next After Skills

Once you have 3–4 skills working, the next architectural step is building a **skill router** — a small function inside `ai_brain.py` that reads the user's intent and automatically dispatches to the right skill, rather than hardcoding trigger phrases everywhere. This is how voice assistants like Alexa work under the hood, and it scales much more cleanly as IRIS grows.