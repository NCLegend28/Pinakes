# Project IRIS: Interactive Real-time Intelligence System
### A Vision AI Conversational Assistant — Full Build Plan

---

## The Big Picture (System Analogy)

Think of this system like **your own nervous system**:

| Human Body        | Your System              | Technology                     |
|-------------------|--------------------------|--------------------------------|
| **Eyes**          | Camera Module            | USB/Pi Camera                  |
| **Ears**          | Microphone               | USB Mic / Array Mic            |
| **Brain**         | Multimodal LLM           | GPT-4o / Claude Vision API    |
| **Speech Center** | Text-to-Speech Engine    | OpenAI TTS / ElevenLabs       |
| **Spinal Cord**   | Orchestrator Script      | Python (your controller code) |
| **Mouth**         | Speaker                  | I2S Amp + 28mm Driver          |
| **Face**          | Touchscreen Display      | 3.5" DSI LCD (camera preview + status) |
| **Heart**         | Portable Power (UPS HAT) | Geekworm X1202 + 18650 cells  |

**Data Flow (the "reflex arc"):**
```
You speak → Mic captures audio → Whisper transcribes to text
                                          ↓
Camera captures frame → Image + Text → Multimodal LLM processes both
                                          ↓
                              LLM generates response text
                                    ↓              ↓
              TTS converts text → audio     Display shows status +
                    ↓                       camera preview
              Speaker plays it
```

Every component is modular — you can swap any piece without rebuilding the whole system. That's the engineering principle here: **loose coupling, high cohesion**.

---

## Architecture Decision: Edge + Cloud Hybrid (Portable)

**Why not fully local?**
Running a good multimodal model locally requires a GPU with 12+ GB VRAM (~$400+ just for the card). That eats your entire budget on one component and gives you worse results than cloud APIs. It also makes portability impossible — GPUs are power-hungry.

**Why not fully cloud?**
You want low-latency voice conversations. Sending raw audio to the cloud for every step adds lag.

**The hybrid approach (best of both worlds):**
- **Local**: Audio capture, wake word detection, camera capture, audio playback, battery management, touchscreen display
- **Cloud**: Speech-to-text, vision+language processing, text-to-speech
- **Power**: Geekworm X1202 UPS HAT with 4x 18650 cells (~5–8 hours portable runtime)
- **Connectivity**: WiFi (required for API calls) — use phone hotspot in the field
- **Result**: Snappy interaction, top-tier AI quality, fully portable, within budget

---

## Bill of Materials

### Option A: Raspberry Pi Build (Handheld Portable Device) — RECOMMENDED

> **Size Target:** No larger than a Nintendo Switch (~240mm × 102mm × 14mm)
> **Pi 5 board alone:** 85mm × 56mm (3.3" × 2.2")
> **3.5" DSI display board:** 86mm × 56mm (matches Pi footprint almost exactly)
> **Realistic assembled size:** ~95mm × 70mm × 40mm (3.7" × 2.8" × 1.6")
> **Architecture: "Screen Sandwich"** — Pi 5 mounts directly to the back of the display board with copper standoffs. DSI ribbon connects internally. Screen becomes the front face of the device. Think thick smartphone in a rugged case.
>
> **Honest note on thickness:** The Switch is 14mm thin because Nintendo custom-designed a thinline battery and SoC on a single board. Our device stacks 4 layers (UPS + Pi + heatsink + display) so ~40mm thick is the realistic floor. Think walkie-talkie, not smartphone. Still very much handheld — just not pocket-slim.

| # | Component | Specific Model | Size | Est. Cost | Purpose |
|---|-----------|---------------|------|-----------|---------|
| 1 | Raspberry Pi 5 (8GB) | Official Pi 5 8GB | 85 × 56mm | $80 | Main compute / orchestrator |
| 2 | MicroSD Card | Samsung EVO Select 128GB | — | $14 | OS + software storage |
| 3 | **Portable Power: UPS HAT** | **Geekworm X1202 (4-cell 18650)** | **~85 × 86mm (slightly wider than Pi)** | **$35** | **5.1V 5A output, smart power management** |
| 4 | **18650 Battery Cells (x4)** | **Samsung INR18650-35E (3500mAh, flat-top)** | **65 × 18mm each (inside X1202)** | **$20** | **~5–8 hrs runtime at full AI load** |
| 5 | Low-profile heatsink | Pimoroni Pi 5 heatsink or GeeekPi low-profile copper | ~85 × 56 × 5mm | $8 | Passive cooling — no fan height, saves ~10mm vs active cooler |
| 6 | **Display** | **Waveshare 3.5" DSI LCD (H) — 480×800, IPS, capacitive touch** | **86 × 56mm (matches Pi footprint!)** | **$10–15** | **Live camera preview, status, touch UI — connects via DSI ribbon, zero GPIO conflict** |
| 7 | Camera | Raspberry Pi Camera Module 3 (Wide) | 25 × 24 × 12mm (tiny!) | $35 | Vision — connects via ribbon cable, mount flush to case edge |
| 8 | **Microphone** | **INMP441 I2S MEMS Mic Breakout** | **14 × 10 × 2mm (thumbnail-sized!)** | **$3** | **Digital mic via I2S GPIO — no USB port needed** |
| 9 | **Amplifier** | **MAX98357A I2S Class-D Amp** | **20 × 18 × 3mm (stamp-sized!)** | **$6** | **3W amp, I2S input, drives speaker directly** |
| 10 | **Speaker Driver** | **28mm 4Ω 3W thin speaker** | **28mm diameter × 5mm** | **$2** | **Mounts inside case lid** |
| 11 | Camera ribbon cable | Pi 5 CSI 22-pin FPC (15cm) | Flat ribbon | $3 | Route camera to case edge window |
| 12 | Hookup wire + solder | 22AWG silicone wire kit | — | $5 | Connect INMP441 + MAX98357A to GPIO |
| 13 | Custom case | **3D-printed enclosure** (see design notes) | ~95 × 70 × 40mm | $10–15 | Houses entire Pi + UPS + display + audio + camera as one unit |

**Hardware Subtotal: ~$226–231**

> **What changed from the desktop version and why:**
>
> | Desktop Version | Handheld Version | Why |
> |----------------|-----------------|-----|
> | JBL Go 3 speaker ($30) | MAX98357A amp + 28mm driver ($8) | JBL is 88×75×42mm — nearly as big as the Pi itself. The I2S amp is the size of a postage stamp, and the 28mm driver is thinner than a coin. |
> | ReSpeaker USB Mic Array ($35) | INMP441 MEMS I2S mic ($3) | ReSpeaker is a 70mm diameter circle — way too big for handheld. The INMP441 is 14mm (smaller than your thumbnail). Trade-off: no noise-cancellation array, but adequate for close-range voice. |
> | Waveshare 7" display ($55) | Waveshare 3.5" DSI LCD (H) ($10–15) | 7 inches is larger than the whole device. The 3.5" DSI model matches the Pi's footprint and connects via ribbon cable — no GPIO conflict with I2S audio. |
> | USB-C Hub ($15) | Not needed | Camera uses CSI ribbon, mic and speaker use I2S on GPIO, display uses DSI ribbon. No USB peripherals left! |
> | Gooseneck camera mount ($10) | Flush mount in case wall | Camera ribbon routes to a window cut in the case shell. |
> | Argon case ($20) | 3D-printed custom case ($10–15) | No off-the-shelf case fits Pi + UPS + display + speaker + camera as a handheld unit. |
>
> **Net savings: ~$75 cheaper than the original desktop build, and fits in your hand — now with a screen.**

> **Soldering required:** The I2S approach requires soldering 5 wires for the mic (3.3V, GND, CLK, WS, DATA) and 5 for the amp (VIN, GND, BCLK, LRC, DIN) to the Pi's GPIO header. If you've never soldered before, this is a great beginner project — all through-hole connections, no surface mount work. A $15 soldering iron kit from Amazon covers it.

### I2S Wiring Map (GPIO Pin Reference)

```
Raspberry Pi 5 GPIO Header
─────────────────────────────────
INMP441 Microphone:        MAX98357A Amplifier:
  VCC  → Pin 1 (3.3V)       VIN  → Pin 2 (5V)
  GND  → Pin 6 (GND)        GND  → Pin 9 (GND)
  SCK  → Pin 12 (GPIO18)    BCLK → Pin 12 (GPIO18)  ← shared clock!
  WS   → Pin 35 (GPIO19)    LRC  → Pin 35 (GPIO19)  ← shared word select!
  SD   → Pin 38 (GPIO20)    DIN  → Pin 40 (GPIO21)

Camera:  22-pin CSI ribbon → Pi 5 CAM port (no GPIO used)
Display: 15-pin DSI ribbon → Pi 5 DSI port (no GPIO used, zero conflict!)
UPS:     Pogo pins on bottom (no GPIO used, I2C on GPIO2/3 for battery monitor)
```

> **Note:** The mic and amp *share* the clock (BCLK) and word select (LRC) lines. This is how I2S works — it's a bus, like a shared highway with lane markers. The mic puts data *onto* the bus (SD/GPIO20), and the amp reads data *from* the bus (DIN/GPIO21). One road, two directions.

### API & Software Costs (from remaining budget)

| Service | Purpose | Est. Monthly Cost | Notes |
|---------|---------|-------------------|-------|
| OpenAI API — GPT-4o | Vision + Language (the "brain") | $15–30/mo | ~$0.005/image + $0.01/1K tokens |
| OpenAI API — Whisper | Speech-to-Text | $3–5/mo | $0.006/minute of audio |
| OpenAI API — TTS | Text-to-Speech | $5–10/mo | $15/1M characters |
| **OR** Anthropic API — Claude | Vision + Language alternative | $15–30/mo | Better reasoning, comparable vision |
| **OR** ElevenLabs TTS | Premium voice quality | $5–22/mo | More natural voices |

**API Budget: ~$25–45/month → $269 covers 6–11 months of usage**

### Total Budget Breakdown

| Category | Cost |
|----------|------|
| Hardware (handheld build) | $226–231 |
| Soldering iron kit (if you don't have one) | ~$15 |
| API Credits (~8 months) | ~$259 |
| **Total** | **~$500** |

> The compact 2-cell build saves ~$75 in hardware vs. the original desktop plan, even with the display added. That extra budget goes straight to API credits — **the fuel that actually powers the AI brain.** You get a smaller device with a screen AND months of runtime. Win-win.

### Portable Runtime Estimates

| Workload | Est. Current Draw | Runtime (2x 3500mAh cells) |
|----------|-------------------|---------------------------|
| Idle (Pi 5 + WiFi only) | ~0.6A | ~8–9 hours |
| Light use (camera + display + occasional AI queries) | ~1.2A | ~4–5 hours |
| **Full Vision AI (camera + display + I2S mic + I2S speaker + continuous queries)** | **~1.7–2.0A** | **~2–3.5 hours** |

> **4-cell runtime (X1202):** The X1202 with 4x 3500mAh cells gives roughly double the runtime of the 2-cell X1200 — expect 5–8 hours under full Vision AI load. The trade-off is width (~30mm wider than the Pi footprint), but you get all-day field use without carrying spare cells.
>
> **Mitigation:** Carry a spare pair of 18650 cells (~$10). Pop them in when the first set dies — takes 10 seconds. Two sets = 5–8 hours of continuous Vision AI use, which covers a solid day of project work.
>
> **Why I2S helps battery life:** The INMP441 mic draws ~1.4mA and the MAX98357A amp draws ~2.4mA at idle. Compare that to the USB mic array (~200mA) and Bluetooth speaker (~150mA). Less parasitic draw = more juice for the brain.

### Option B: Laptop-Based Build (If you want to prototype first before going handheld)

If you already have a laptop with a webcam, you can build and test all the software first, then port to the Pi handheld. You only need:

| Component | Cost | Purpose |
|-----------|------|---------|
| USB Microphone (any small one) | $10–20 | Audio capture for prototyping |
| API Credits | ~$180 (6 months) | Same cloud AI services |
| **Total** | **~$190–200** | Software-identical to the Pi build, just not portable |

> This is a great approach if you want to learn the code first before committing to hardware. The Python code is identical on laptop vs. Pi — you just swap `picamera2` for OpenCV webcam capture.

---

## Step-by-Step Build Plan

### PHASE 1: Foundation (Days 1–3)
**Goal: Get the Pi running on portable power and talking to the internet**

#### Step 1.0 — Assemble the UPS HAT (Do This First!)
```
Assembly order (think of it like stacking LEGO):

1. Insert 4x 18650 cells into the X1202 board
   - CHECK POLARITY — the + and - are marked on the board
   - Use flat-top, unprotected cells (max length 65.3mm, diameter 18.5mm)
   - The X1202 has 2 pairs of cells in parallel for extended runtime

2. Mount the Pi 5 on top of the X1202
   - The X1202 stacks onto the Pi's 40-pin GPIO header
   - Align pin 1 carefully before pressing down — no force needed if aligned correctly
   - Secure with the included standoffs/screws
   
3. Attach the low-profile heatsink to the Pi 5's CPU (thermal pad included)
   
4. The 3D-printed case comes later (Phase 7) — for now, work with the bare stack

IMPORTANT: Do NOT plug power into the Pi's own USB-C port.
Instead, plug your USB-C charging cable into the X1202's USB-C port.
The UPS HAT manages all power delivery to the Pi.
```

#### Step 1.1 — Flash the OS
```bash
# On your main computer, download Raspberry Pi Imager
# Flash "Raspberry Pi OS (64-bit)" onto your microSD card
# Enable SSH, set WiFi credentials, set username/password in Imager settings
```

#### Step 1.2 — Initial Pi Setup
```bash
# Insert microSD into Pi, press the power button on the X1202 to boot
# Connect keyboard, monitor (or SSH in)
sudo apt update && sudo apt upgrade -y

# Install Python 3.11+ and essential tools
# python3-picamera2 and python3-libcamera must come from apt — pip alone won't work
sudo apt install -y python3-pip python3-venv git portaudio19-dev \
    libsndfile1 ffmpeg libatlas-base-dev i2c-tools \
    python3-picamera2 python3-libcamera python3-kms++

# Create project directory and virtual environment
# --system-site-packages makes apt-installed libs (picamera2, libcamera) visible in the venv
mkdir ~/vision-ai && cd ~/vision-ai
python3 -m venv --system-site-packages venv
source venv/bin/activate
```

#### Step 1.2b — Configure UPS Power Management
```bash
# Enable I2C (needed for battery level monitoring)
sudo raspi-config nonint do_i2c 0

# Verify the UPS HAT is detected (should show address 0x36)
sudo i2cdetect -y 1

# Enable full USB current (good practice even though I2S uses GPIO, not USB)
echo "usb_max_current_enable=1" | sudo tee -a /boot/firmware/config.txt

# Install smbus2 for battery monitoring
pip install smbus2

# Reboot to apply config changes
sudo reboot
```

#### Step 1.3 — Install Core Python Libraries
```bash
# picamera2 was installed via apt in Step 1.2 and is already accessible
# (because we created the venv with --system-site-packages)
pip install openai           # GPT-4o, Whisper, TTS APIs
pip install anthropic        # Claude API (alternative brain)
pip install sounddevice      # Audio I/O (works with I2S ALSA devices)
pip install numpy            # Audio processing
pip install Pillow           # Image processing
pip install opencv-python-headless  # Image processing for skills (NOT camera capture)
pip install python-dotenv    # Secure API key management
pip install pvporcupine      # Wake word detection (optional)
pip install smbus2           # I2C communication (UPS battery monitoring)
```

#### Step 1.4 — Configure I2S Audio (Mic + Speaker)
```bash
# The INMP441 mic and MAX98357A amp both use I2S over GPIO.
# This requires a device tree overlay to enable the I2S peripheral.

# Pi 5 uses a new audio subsystem (RP1 chip). Use these overlays:
# For MAX98357A output:  dtoverlay=hifiberry-dac
# For INMP441 input:     dtoverlay=i2s-mems-mic,gpiopin=20
# Add both to /boot/firmware/config.txt:
echo "dtoverlay=hifiberry-dac" | sudo tee -a /boot/firmware/config.txt
echo "dtoverlay=i2s-mems-mic,gpiopin=20" | sudo tee -a /boot/firmware/config.txt

# NOTE: If you're on Pi 4 or earlier, use this single overlay instead:
# echo "dtoverlay=googlevoicehat-soundcard" | sudo tee -a /boot/firmware/config.txt

# Reboot to load the I2S driver
sudo reboot

# After reboot, verify I2S devices are detected:
arecord -l    # Should show an I2S capture device
aplay -l      # Should show an I2S playback device
```

#### Step 1.5 — Secure Your API Keys
```bash
# NEVER hardcode API keys in your scripts
echo "OPENAI_API_KEY=sk-your-key-here" >> ~/vision-ai/.env
echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" >> ~/vision-ai/.env
chmod 600 ~/vision-ai/.env
```

#### Step 1.6 — Test Battery Monitoring
```python
# test_battery.py — Verify UPS HAT communication
import smbus2
from gpiozero import DigitalInputDevice

bus = smbus2.SMBus(1)
UPS_ADDR = 0x36

# Read battery voltage
raw = bus.read_word_data(UPS_ADDR, 0x02)
voltage = ((raw & 0xFF) << 8 | (raw >> 8)) * 78.125 / 1_000_000
print(f"🔋 Battery voltage: {voltage:.2f}V")

# Read battery percentage
raw = bus.read_word_data(UPS_ADDR, 0x04)
percent = ((raw & 0xFF) << 8 | (raw >> 8)) / 256
print(f"🔋 Battery level: {percent:.1f}%")

# Read AC power state (GPIO6)
ac_detect = DigitalInputDevice(pin=6, pull_up=True)
ac_power = ac_detect.value
print(f"🔌 AC Power: {'Connected' if ac_power == 1 else 'On Battery'}")

**Checkpoint:** Pi boots from UPS, you can read battery level, and all peripherals get full power.

#### Step 1.7 — Attach the 3.5" DSI Display
```
Assembly (the "screen sandwich"):

1. Connect the 12cm DSI ribbon cable from the display board to the Pi 5's DSI1 port
   - Lift the latch on the Pi's DSI connector, insert ribbon (contacts facing the board), push latch down
   - Same technique as the camera ribbon — gentle, no force needed

2. Mount the Pi 5 onto the back of the display board using the included copper standoffs
   - The display board has matching screw holes for Pi mounting
   - The Pi's GPIO header remains fully accessible on the back for I2S wiring later

3. The display also provides 5V power + I2C touch via a 4-pin connector to the Pi
   - Follow Waveshare's instructions for the specific (H) model wiring
```

```bash
# The DSI display should work out of the box on Raspberry Pi OS (Bookworm or later)
# Verify it's detected:
ls /dev/dri/
# Should show card0, card1, etc.

# If the display orientation is portrait (default for the H model), rotate to landscape:
# Edit /boot/firmware/config.txt and add:
# display_lcd_rotate=1
# Then reboot

# Test touch input:
sudo apt install -y libinput-tools
sudo libinput debug-events
# Touch the screen — you should see event output
```

**Checkpoint:** DSI display shows the desktop, touch input works, and the GPIO header is still free for I2S audio.

---

### PHASE 2: The Ears — Speech Input (Days 4–6)
**Goal: Capture your voice and convert it to text**

**Analogy:** This is like building a court stenographer — it listens and transcribes in real-time.

#### Step 2.1 — Test Microphone (I2S INMP441)
```python
# test_mic.py — Verify your I2S MEMS microphone works
import sounddevice as sd
import numpy as np

def test_recording(duration=3, sample_rate=16000):
    # List audio devices to find the I2S mic
    print(sd.query_devices())
    print("\nRecording for 3 seconds via I2S mic...")
    audio = sd.rec(int(duration * sample_rate),
                   samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    print(f"Captured {len(audio)} samples, max amplitude: {np.max(np.abs(audio))}")
    if np.max(np.abs(audio)) < 100:
        print("⚠️  Very low amplitude — check INMP441 wiring (especially SD → GPIO20)")
    else:
        print("✅ Microphone working!")
    return audio

test_recording()
```

#### Step 2.2 — Build the Audio Capture Module
```python
# audio_capture.py — Records until you stop speaking
import sounddevice as sd
import numpy as np
import wave
import io

class AudioCapture:
    def __init__(self, sample_rate=16000, channels=1, silence_threshold=500,
                 silence_duration=1.5):
        self.sample_rate = sample_rate
        self.channels = channels
        self.silence_threshold = silence_threshold  # Adjust based on your mic/environment
        self.silence_duration = silence_duration     # Seconds of silence = "done talking"

    def record_until_silence(self) -> bytes:
        """Record audio, stop when silence is detected. Returns WAV bytes."""
        print("🎤 Listening...")
        frames = []
        silent_frames = 0
        max_silent = int(self.silence_duration * self.sample_rate / 1024)

        def callback(indata, frame_count, time_info, status):
            nonlocal silent_frames
            frames.append(indata.copy())
            amplitude = np.max(np.abs(indata))
            if amplitude < self.silence_threshold:
                silent_frames += 1
            else:
                silent_frames = 0

        with sd.InputStream(samplerate=self.sample_rate, channels=self.channels,
                           dtype='int16', blocksize=1024, callback=callback):
            while silent_frames < max_silent:
                sd.sleep(100)

        # Convert to WAV bytes
        audio_data = np.concatenate(frames)
        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)  # 16-bit = 2 bytes
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_data.tobytes())
        return buffer.getvalue()
```

#### Step 2.3 — Build the Speech-to-Text Module
```python
# stt_engine.py — Sends audio to Whisper API
from openai import OpenAI
import io

class SpeechToText:
    def __init__(self):
        self.client = OpenAI()  # Reads OPENAI_API_KEY from environment

    def transcribe(self, audio_bytes: bytes) -> str:
        """Convert audio bytes to text using Whisper."""
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "audio.wav"  # Whisper needs a filename

        transcript = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
        print(f"📝 You said: {transcript}")
        return transcript
```

**Checkpoint:** You can speak, and see your words printed as text.

---

### PHASE 3: The Eyes — Vision Input (Days 7–9)
**Goal: Capture what the camera sees and prepare it for the AI**

**Analogy:** This is like building a photographer who takes a snapshot on command and hands it to the analyst.

#### Step 3.1 — Test Camera
```python
# test_camera.py
from picamera2 import Picamera2
import time

cam = Picamera2()
cam.configure(cam.create_still_configuration())
cam.start()

print("Camera opened. Warming up...")
time.sleep(2)

cam.capture_file("test_photo.jpg")
cam.stop()
print("Photo saved as test_photo.jpg")
```

#### Step 3.2 — Build the Vision Capture Module
```python
# vision_capture.py — Captures and encodes images via Pi Camera Module (picamera2)
import base64
import io
import time
import threading
import numpy as np
from PIL import Image
import cv2
from picamera2 import Picamera2

CAPTURE_FLASH_DURATION = 1.0

class VisionCapture:
    def __init__(self, resolution=(1280, 720)):
        self.camera = Picamera2()
        # Video config = continuous stream; still config adds shutter lag per capture
        config = self.camera.create_video_configuration(
            main={"size": resolution, "format": "RGB888"}
        )
        self.camera.configure(config)
        self.camera.start()

        self._lock = threading.Lock()
        self._latest_frame = None
        self._last_capture_time = 0.0
        self._running = True

        # Background thread reads frames continuously (~30 fps)
        self._thread = threading.Thread(target=self._reader, daemon=True)
        self._thread.start()

        for _ in range(40):
            if self._latest_frame is not None:
                break
            time.sleep(0.05)

    def _reader(self):
        while self._running:
            frame = self.camera.capture_array("main")  # RGB numpy array
            with self._lock:
                self._latest_frame = frame
            time.sleep(0.033)  # ~30 fps

    def capture_frame(self) -> str:
        """Grab latest frame, return as base64-encoded JPEG string."""
        with self._lock:
            if self._latest_frame is None:
                raise RuntimeError("No frame available.")
            frame = self._latest_frame.copy()

        self._last_capture_time = time.time()
        image = Image.fromarray(frame)  # picamera2 returns RGB — PIL uses it directly
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=85)
        print(f"Captured frame: {image.size[0]}x{image.size[1]}")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    def get_preview_frame(self) -> np.ndarray | None:
        """Return the latest frame as BGR (for cv2), with a flash if recently captured."""
        with self._lock:
            if self._latest_frame is None:
                return None
            frame = self._latest_frame.copy()

        # picamera2 returns RGB — convert to BGR for cv2
        frame_bgr = frame[:, :, ::-1].copy()

        if time.time() - self._last_capture_time < CAPTURE_FLASH_DURATION:
            h, w = frame_bgr.shape[:2]
            cv2.rectangle(frame_bgr, (0, 0), (w, h), (0, 220, 0), 8)
            cv2.putText(frame_bgr, "AI CAPTURING", (20, 52),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 220, 0), 3, cv2.LINE_AA)

        return frame_bgr

    def cleanup(self):
        self._running = False
        self._thread.join(timeout=2)
        self.camera.stop()
```

**Checkpoint:** You can capture images and encode them as base64 strings.

---

### PHASE 4: The Brain — Multimodal Processing (Days 10–14)
**Goal: Send text + image to the LLM, get an intelligent response**

**Analogy:** This is the central nervous system — it takes in all sensory data and decides what to say. The system prompt is like your brain's "personality firmware."

#### Step 4.1 — Build the AI Brain Module (GPT-4o Version)
```python
# ai_brain.py — Multimodal conversation engine
from openai import OpenAI

class AIBrain:
    def __init__(self, system_prompt=None):
        self.client = OpenAI()
        self.conversation_history = []
        self.system_prompt = system_prompt or (
            "You are a helpful AI vision assistant. You can see what the user "
            "shows you through their camera and have natural conversations about "
            "real-world objects, project ideas, and technical concepts. "
            "Be concise but thorough. When you see objects, describe what you "
            "notice and offer insights. If the user is showing you a project or "
            "prototype, give constructive technical feedback."
        )

    def think(self, user_text: str, image_base64: str = None) -> str:
        """Process text + optional image, return response."""
        # Build the message content
        content = []

        if image_base64:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_base64}",
                    "detail": "high"  # Use "low" to save tokens/cost
                }
            })

        content.append({"type": "text", "text": user_text})

        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": content})

        # Build messages with system prompt
        messages = [
            {"role": "system", "content": self.system_prompt}
        ] + self.conversation_history[-10:]  # Keep last 10 turns (memory window)

        # Call the API
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )

        assistant_message = response.choices[0].message.content

        # Store in history (without image to save context space)
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        print(f"🧠 AI: {assistant_message}")
        return assistant_message

    def reset_conversation(self):
        """Clear conversation history."""
        self.conversation_history = []
        print("🔄 Conversation reset.")
```

#### Step 4.2 — Alternative: Claude Vision Brain
```python
# ai_brain_claude.py — Using Anthropic's Claude for vision
import anthropic

class AIBrainClaude:
    def __init__(self, system_prompt=None):
        self.client = anthropic.Anthropic()
        self.conversation_history = []
        self.system_prompt = system_prompt or (
            "You are a helpful AI vision assistant..."  # Same as above
        )

    def think(self, user_text: str, image_base64: str = None) -> str:
        content = []

        if image_base64:
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": image_base64
                }
            })

        content.append({"type": "text", "text": user_text})
        self.conversation_history.append({"role": "user", "content": content})

        response = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            system=self.system_prompt,
            messages=self.conversation_history[-10:]
        )

        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        return assistant_message
```

**Checkpoint:** You can send an image + text and get an intelligent response back.

---

### PHASE 5: The Voice — Speech Output (Days 15–17)
**Goal: Make the AI speak its responses through the I2S speaker**

**Analogy:** This is the vocal cords — turning thought into speech. The MAX98357A amp takes digital audio and pushes it through the 40mm speaker driver mounted in your case.

#### Step 5.1 — Test Speaker Output
```bash
# Verify the MAX98357A amp + speaker are working
# (Should hear white noise alternating left/right, or continuous for mono)
speaker-test -c2 -t wav

# If no sound, check:
# 1. Wiring: VIN→5V, GND→GND, BCLK→GPIO18, LRC→GPIO19, DIN→GPIO21
# 2. Overlay loaded: check /boot/firmware/config.txt has dtoverlay line
# 3. Volume: alsamixer (use arrow keys to raise volume)
```

#### Step 5.2 — Build the Text-to-Speech Module
```python
# tts_engine.py — Converts AI response to spoken audio
from openai import OpenAI
import subprocess
import tempfile
import os

class TextToSpeech:
    def __init__(self, voice="nova"):
        """
        Available voices: alloy, echo, fable, onyx, nova, shimmer
        'nova' is warm and natural; 'onyx' is deeper;
        'shimmer' is clear and bright
        """
        self.client = OpenAI()
        self.voice = voice

    def speak(self, text: str):
        """Convert text to speech and play it."""
        response = self.client.audio.speech.create(
            model="tts-1",       # Use "tts-1-hd" for higher quality (2x cost)
            voice=self.voice,
            input=text,
            response_format="mp3"
        )

        # Save to temp file and play
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            f.write(response.content)
            temp_path = f.name

        # Play audio via ffplay (part of ffmpeg, installed in Step 1.2)
        # On Mac, use "afplay" instead of "ffplay"
        subprocess.run(
            ["ffplay", "-nodisp", "-autoexit", temp_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        os.unlink(temp_path)  # Clean up
```

**Checkpoint:** You can type a sentence and hear the AI speak it.

---

### PHASE 6: The Spinal Cord — Wire It All Together (Days 18–22)
**Goal: Unified system — speak, show, listen, repeat**

#### Step 6.1 — Battery Monitor Module
```python
# battery_monitor.py — Reads UPS HAT battery state via I2C
import smbus2
import threading
import time

class BatteryMonitor:
    def __init__(self, warn_percent=15, critical_percent=5):
        self.bus = smbus2.SMBus(1)
        self.address = 0x36
        self.warn_percent = warn_percent
        self.critical_percent = critical_percent
        self._running = False

    def get_voltage(self) -> float:
        """Read battery voltage in volts."""
        try:
            raw = self.bus.read_word_data(self.address, 0x02)
            return ((raw & 0xFF) << 8 | (raw >> 8)) * 78.125 / 1_000_000
        except Exception:
            return -1.0

    def get_percent(self) -> float:
        """Read battery percentage (0-100)."""
        try:
            raw = self.bus.read_word_data(self.address, 0x04)
            return ((raw & 0xFF) << 8 | (raw >> 8)) / 256
        except Exception:
            return -1.0

    def get_status(self) -> dict:
        """Get full battery status."""
        percent = self.get_percent()
        voltage = self.get_voltage()
        if percent <= self.critical_percent:
            level = "CRITICAL"
        elif percent <= self.warn_percent:
            level = "LOW"
        else:
            level = "OK"
        return {"percent": percent, "voltage": voltage, "level": level}

    def status_string(self) -> str:
        """Human-readable battery status."""
        s = self.get_status()
        icon = "🔋" if s["level"] == "OK" else "🪫" if s["level"] == "LOW" else "🚨"
        return f"{icon} Battery: {s['percent']:.0f}% ({s['voltage']:.2f}V)"
```

#### Step 6.2 — Main Orchestrator
```python
# main.py — The complete Portable Vision AI Assistant
from dotenv import load_dotenv
load_dotenv()  # Load API keys from .env

from audio_capture import AudioCapture
from stt_engine import SpeechToText
from vision_capture import VisionCapture
from ai_brain import AIBrain
from tts_engine import TextToSpeech
from battery_monitor import BatteryMonitor
import sys

class VisionAssistant:
    def __init__(self):
        print("🚀 Initializing Vision AI Assistant...")
        self.ears = AudioCapture()
        self.transcriber = SpeechToText()
        self.eyes = VisionCapture()
        self.brain = AIBrain()
        self.voice = TextToSpeech(voice="nova")
        self.battery = BatteryMonitor(warn_percent=15, critical_percent=5)
        print(f"✅ All systems online! {self.battery.status_string()}\n")

    def check_battery(self) -> bool:
        """Check battery and warn user if low. Returns False if critical."""
        status = self.battery.get_status()
        if status["level"] == "CRITICAL":
            self.voice.speak(
                f"Warning: battery critically low at {status['percent']:.0f} percent. "
                "Shutting down to protect your work. Please recharge."
            )
            return False
        elif status["level"] == "LOW":
            self.voice.speak(
                f"Heads up — battery is at {status['percent']:.0f} percent. "
                "Consider plugging in soon."
            )
        return True

    def run(self):
        """Main conversation loop."""
        print("=" * 50)
        print("  PROJECT IRIS — Portable Vision AI Assistant")
        print("  Speak naturally. Show me things.")
        print("  Say 'goodbye' to exit.")
        print("  Say 'reset' to clear conversation.")
        print("  Say 'look at this' to include camera.")
        print("  Say 'battery' to check power level.")
        print("=" * 50)

        turn_count = 0

        while True:
            try:
                # Check battery every 5 conversation turns
                turn_count += 1
                if turn_count % 5 == 0:
                    if not self.check_battery():
                        break  # Critical battery — safe shutdown

                # STEP 1: Listen
                audio_bytes = self.ears.record_until_silence()

                # STEP 2: Transcribe
                user_text = self.transcriber.transcribe(audio_bytes)

                if not user_text.strip():
                    continue

                # Check for commands
                lower_text = user_text.lower().strip()
                if any(word in lower_text for word in ["goodbye", "bye", "exit", "quit"]):
                    self.voice.speak("Goodbye! Great chatting with you.")
                    break

                if "reset" in lower_text:
                    self.brain.reset_conversation()
                    self.voice.speak("Conversation reset. Fresh start!")
                    continue

                if "battery" in lower_text:
                    status = self.battery.status_string()
                    print(status)
                    self.voice.speak(
                        f"Battery is at {self.battery.get_percent():.0f} percent."
                    )
                    continue

                # STEP 3: Decide whether to include vision
                include_vision = any(phrase in lower_text for phrase in [
                    "look", "see", "show", "what is this", "check this",
                    "camera", "watch", "observe", "this thing"
                ])

                image_b64 = None
                if include_vision:
                    image_b64 = self.eyes.capture_frame()

                # STEP 4: Think
                response = self.brain.think(user_text, image_b64)

                # STEP 5: Speak
                self.voice.speak(response)

            except KeyboardInterrupt:
                print("\n👋 Shutting down...")
                break
            except Exception as e:
                print(f"❗ Error: {e}")
                continue

        self.eyes.cleanup()
        print(f"Final {self.battery.status_string()}")

if __name__ == "__main__":
    assistant = VisionAssistant()
    assistant.run()
```

**Checkpoint:** Full working system — you talk, it listens, sees, thinks, and responds.

---

### PHASE 7: Polish & Enhance (Days 23–30)
**Goal: Make it production-quality and add power features**

#### 7.1 — Add Wake Word Detection (Hands-Free)
Instead of always listening, use Picovoice Porcupine for a wake word like "Hey Iris":
```bash
pip install pvporcupine
```
Free tier supports custom wake words. This means the mic only activates when you say the trigger phrase — huge UX improvement.

#### 7.2 — Add Always-On Vision Mode
For continuous observation (like showing a project build):
```python
# Add to VisionAssistant class
def continuous_vision_mode(self, interval=5):
    """Capture and analyze every N seconds."""
    import time
    print("👁️ Continuous vision mode. Speak to discuss what I see.")
    while True:
        image_b64 = self.eyes.capture_frame()
        audio = self.ears.record_until_silence()
        text = self.transcriber.transcribe(audio)
        response = self.brain.think(text, image_b64)
        self.voice.speak(response)
```

#### 7.3 — Add Conversation Logging
```python
import json
from datetime import datetime

class ConversationLogger:
    def __init__(self, log_dir="./logs"):
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = f"{log_dir}/session_{datetime.now():%Y%m%d_%H%M%S}.json"
        self.entries = []

    def log(self, role, text, had_image=False):
        self.entries.append({
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "text": text,
            "included_image": had_image
        })
        with open(self.log_file, 'w') as f:
            json.dump(self.entries, f, indent=2)
```

#### 7.4 — Cost Optimization Tips
| Technique | Savings |
|-----------|---------|
| Use `detail: "low"` for images when fine detail isn't needed | ~85% less per image |
| Cap `max_tokens` to 300 for casual chat, 800 for technical | ~40% token savings |
| Use `tts-1` instead of `tts-1-hd` | 50% TTS savings |
| Batch casual queries with `gpt-4o-mini` and reserve `gpt-4o` for vision | ~90% for text-only |
| Store and summarize old conversation history instead of keeping full context | Reduces context length |

---

## Project File Structure
```
~/vision-ai/
├── .env                    # API keys (NEVER commit this)
├── main.py                 # Orchestrator with battery awareness (Phase 6)
├── audio_capture.py        # Microphone input (Phase 2)
├── stt_engine.py           # Speech-to-Text (Phase 2)
├── vision_capture.py       # Camera input (Phase 3)
├── ai_brain.py             # GPT-4o multimodal (Phase 4)
├── ai_brain_claude.py      # Claude alternative (Phase 4)
├── tts_engine.py           # Text-to-Speech (Phase 5)
├── battery_monitor.py      # UPS HAT battery monitoring (Phase 6)
├── conversation_logger.py  # Logging (Phase 7)
├── test_mic.py             # Hardware test
├── test_camera.py          # Hardware test
├── test_battery.py         # UPS HAT test (Phase 1)
├── requirements.txt        # All pip dependencies
├── logs/                   # Conversation logs
└── README.md               # Your project notes
```

---

## Troubleshooting Quick Reference

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| Mic doesn't record | Wrong device index | Run `python -m sounddevice` to list devices, set `device=N` |
| Camera "already in use" | Previous process didn't release | `sudo pkill -f libcamera` then retry |
| Camera init fails / no frames | picamera2 config mismatch | Ensure venv was created with `--system-site-packages`; verify `python3 -c "from picamera2 import Picamera2"` works |
| API returns 401 | Bad API key | Check `.env` file, ensure no extra spaces |
| Audio playback choppy | I2S buffer underrun | Check `dtoverlay` in config.txt, try increasing ALSA buffer size |
| No sound from speaker | MAX98357A wiring or overlay | Verify BCLK→GPIO18, LRC→GPIO19, DIN→GPIO21; run `speaker-test -c2` |
| Mic records silence | INMP441 wiring issue | Check SD→GPIO20, verify `arecord -l` shows I2S device |
| AI doesn't "see" well | Low resolution / bad lighting | Increase resolution, add desk lamp |
| High API costs | Too many high-detail images | Switch to `detail: "low"`, use `gpt-4o-mini` for text-only |
| Silence detection too sensitive | Threshold too high | Lower `silence_threshold` in AudioCapture |
| **UPS shuts down after 3 sec** | **Pogo pins not making contact** | **Reseat Pi on UPS HAT, clean GPIO pads on Pi bottom** |
| **I2C address 0x36 not found** | **I2C not enabled or bad contact** | **Run `sudo raspi-config` → enable I2C, reseat pogo pins** |
| **Lightning bolt ⚡ icon on screen** | **Power supply insufficient** | **Check UPS is charged, verify USB-C cable supports 5A** |
| **Battery drains faster than expected** | **USB devices drawing too much** | **Disconnect display when not needed, use `detail: "low"` to reduce CPU** |
| **UPS won't charge after power reconnect** | **Known quirk on some firmware** | **Press S1 button on X1202 to restart charging** |
| **0x36 not found on i2cdetect** | **Cells discharged below fuel gauge minimum** | **Charge via X1202's USB-C port for 30–60 min, then retry `sudo i2cdetect -y 1`** |
| **Pi throttling (temp icon)** | **Passive heatsink insufficient for load** | **Ensure heatsink has good thermal pad contact; reduce CPU load or add small 5V fan** |
| **DSI display blank/white** | **Ribbon cable not seated properly** | **Reseat DSI ribbon — lift latch, reinsert firmly (contacts facing board), push latch down** |
| **Display shows portrait, not landscape** | **Default orientation for (H) model** | **Add `display_lcd_rotate=1` to `/boot/firmware/config.txt` and reboot** |
| **Touch not working on display** | **I2C touch driver not loaded** | **Check Waveshare wiki for driver install; verify I2C with `sudo i2cdetect -y 1`** |

---

## Upgrade Roadmap (After v1.0)

| Upgrade | Difficulty | Cost | Value |
|---------|-----------|------|-------|
| Add OpenAI Realtime API (true voice-to-voice) | Medium | Same API cost | Eliminates STT/TTS roundtrip, feels instant |
| Local Whisper (run STT on-device) | Medium | Free | No STT API costs, works offline for transcription |
| Second INMP441 (stereo array) | Easy | +$3 | Basic noise rejection via beamforming |
| Add on-screen GUI (Pygame/Qt) | Medium | Free | Live camera feed, conversation history, battery status on the 3.5" display |
| Add object memory (vector DB) | Hard | Free (local) | "Remember" objects between sessions |
| Stream video (not just snapshots) | Medium | Higher API cost | Real-time motion understanding |
| Solar charging panel | Easy | ~$25 | Charge UPS outdoors for extended field use |
| Spare 18650 cell set | Easy | ~$20 | Hot-swap batteries for all-day field sessions |
| Wrist/arm mount strap | Easy | ~$10 | Truly hands-free wearable AI assistant |
| Upgrade to Pi 5 16GB | Easy | +$40 | Run local small LLM as offline fallback |

---

## Shopping List (Quick Copy-Paste for Ordering)

### Core Components:
1. ☐ Raspberry Pi 5 8GB — **$80**
   - **Amazon:** https://www.amazon.com/Raspberry-Pi-8GB-SC1112-Quad-core/dp/B0CK2FCG1K
   - **Adafruit:** https://www.adafruit.com/product/5813
   - **CanaKit:** https://www.canakit.com/raspberry-pi-5-8gb.html
   - **PiShop.us:** https://www.pishop.us

2. ☐ Samsung EVO Select 128GB microSD — **$14**
   - **Amazon:** Search "Samsung EVO Select 128GB microSD" — widely available

3. ☐ **Geekworm X1200 2-Cell 18650 UPS HAT for Pi 5** — **$25**
   - **Amazon:** https://www.amazon.com/Geekworm-X1200-Raspberry-Shutdown-Detection/dp/B0CRYVC8C5
   - **Geekworm Direct:** https://geekworm.com/products/x1200

4. ☐ **Samsung INR18650-35E 3500mAh cells x2** (flat-top, unprotected) — **$10**
   - **Amazon:** Search "Samsung 35E 18650 flat top" — buy from reputable battery sellers only
   - **18650BatteryStore.com** — specialist retailer, verified authentic cells
   - **IMRbatteries.com** — another trusted 18650 vendor

5. ☐ Pimoroni Pi 5 heatsink (low-profile passive, no fan) — **$8**
   - **Pimoroni:** https://shop.pimoroni.com (search "Pi 5 heatsink")
   - **Amazon:** Search "Pimoroni Pi 5 heatsink" or "GeeekPi Pi 5 copper heatsink"

6. ☐ **Waveshare 3.5" DSI LCD (H) — 480×800, IPS, capacitive touch** — **$10–15**
   - **Waveshare Direct:** https://www.waveshare.com/3.5inch-dsi-lcd-h.htm
   - **Amazon:** Search "Waveshare 3.5inch DSI LCD H" — also listed on Amazon US via Waveshare storefront

7. ☐ Raspberry Pi Camera Module 3 Wide — **$35**
   - **Amazon:** https://www.amazon.com/Raspberry-Pi-Camera-Module/dp/B0BRY6MVXL (select "Wide" variant)
   - **Adafruit:** https://www.adafruit.com/product/5658
   - **PiShop.us:** https://www.pishop.us/product/raspberry-pi-camera-module-3/
   - **Pimoroni:** https://shop.pimoroni.com/en-us/products/raspberry-pi-camera-module-3

### I2S Audio:
8. ☐ INMP441 I2S MEMS Microphone Breakout — **$3**
   - **Amazon (single):** https://www.amazon.com/DAOKI-Omnidirectional-Microphone-Interface-Precision/dp/B0821521CV
   - **Amazon (3-pack ~$8):** https://www.amazon.com/AITRIPAITRIP-AITRIP-Omnidirectional-Microphone-Interface/dp/B0972XP1YS
   - **Amazon (5-pack ~$10):** https://www.amazon.com/EC-Buying-INMP441-Omnidirectional-Microphone/dp/B0C1C64R8S
   - _Tip: Multi-packs are great value — keep spares or add a second mic later for stereo._

9. ☐ Adafruit MAX98357A I2S 3W Class-D Amp Breakout — **$6**
   - **Adafruit (official, best docs):** https://www.adafruit.com/product/3006
   - **Amazon (Adafruit brand):** https://www.amazon.com/Adafruit-I2S-Class-Amplifier-Breakout/dp/B01K5GCFA6
   - **Micro Center:** https://www.microcenter.com/product/613583/adafruit-industries-max98357a-i2s-3w-class-d-amplifier-breakout
   - **Amazon (generic clones ~$3–4):** Search "MAX98357A I2S amplifier breakout" for budget alternatives

10. ☐ 28mm 4Ω 3W Thin Speaker Driver — **$2**
    - **Amazon:** Search "28mm 4 ohm 3W thin speaker" — many generic options available
    - **Adafruit (Gikfun 2-pack):** Search "Gikfun 4Ohm 3W speaker Arduino" on Amazon

11. ☐ Pi 5 CSI Camera Ribbon Cable (15cm, 22-pin to 15-pin) — **$3**
    - **Adafruit:** https://www.adafruit.com/product/5658 (one now included with Camera Module 3)
    - **Amazon:** Search "Raspberry Pi 5 camera cable 22 pin to 15 pin"

12. ☐ 22AWG Silicone Hookup Wire (assorted) — **$5**
    - **Amazon:** Search "22AWG silicone wire kit" — any multi-color kit works

### Enclosure:
13. ☐ 3D-printed custom case (or order via print service) — **$10–15**
    - **PCBWay 3D Printing:** https://www.pcbway.com/rapid-prototyping/3d-printing/
    - **JLCPCB 3D Printing:** https://jlc3dp.com
    - **Shapeways / Craftcloud** — alternative print-on-demand services
    - _Or print yourself if you have access to an FDM printer (PLA or PETG recommended)._

### Tools (if needed):
14. ☐ Soldering iron starter kit — **$15** *(skip if you already own one)*
    - **Amazon:** Search "soldering iron kit" — any beginner kit with temperature control works

### API Credits:
15. ☐ OpenAI API Credits — **$50–100 to start**
    - **OpenAI:** https://platform.openai.com
16. ☐ Anthropic API Credits (optional, for Claude brain) — **$25–50**
    - **Anthropic:** https://console.anthropic.com

> **⚠️ Battery safety note:** Only buy 18650 cells from reputable vendors (Samsung, LG, Panasonic/Sanyo, Sony/Murata). Avoid no-name cells that claim impossibly high capacities (anything over 3600mAh for an 18650 is fake). Flat-top, unprotected cells are what the X1202 requires — max length 65.3mm, max diameter 18.5mm. The X1202 holds 4 cells.

**Hardware Total: ~$226–231 | With tools: ~$246 | With 8 months API: ~$500**
