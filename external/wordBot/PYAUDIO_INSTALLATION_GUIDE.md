# PyAudio Installation Guide

This guide documents solutions for common PyAudio installation issues across different platforms.

## Common Error: Missing PortAudio Headers

**Error Message:**
```
fatal error: 'portaudio.h' file not found
```

**Cause:** PyAudio requires the PortAudio library and development headers to compile.

## Platform-Specific Solutions

### macOS (Homebrew)

**For Apple Silicon (M1/M2/M3) and Intel Macs:**

1. **Install PortAudio via Homebrew:**
   ```bash
   brew install portaudio
   ```

2. **Install PyAudio:**
   ```bash
   pip install pyaudio
   ```

**Alternative if above fails:**
```bash
# Set compiler flags manually
export CPPFLAGS="-I/opt/homebrew/include"
export LDFLAGS="-L/opt/homebrew/lib"
pip install pyaudio
```

### macOS (MacPorts)

```bash
sudo port install portaudio
pip install pyaudio
```

### Ubuntu/Debian Linux

```bash
# Install development packages
sudo apt-get update
sudo apt-get install portaudio19-dev python3-pyaudio

# Then install via pip
pip install pyaudio
```

### CentOS/RHEL/Fedora

```bash
# For newer versions (dnf)
sudo dnf install portaudio-devel
pip install pyaudio

# For older versions (yum)
sudo yum install portaudio-devel
pip install pyaudio
```

### Windows

**Option 1: Use pre-compiled wheels**
```bash
pip install pyaudio
```

**Option 2: If compilation needed**
- Install Microsoft Visual C++ Build Tools
- Install portaudio manually
- Set environment variables for include/lib paths

**Option 3: Use conda**
```bash
conda install pyaudio
```

## Alternative Solutions

### 1. Using Conda (Cross-platform)

```bash
# Create conda environment
conda create -n audio_env python=3.11
conda activate audio_env
conda install pyaudio
```

### 2. Using System Package Manager (Linux)

```bash
# Install system package instead of pip
sudo apt-get install python3-pyaudio  # Debian/Ubuntu
sudo dnf install python3-pyaudio      # Fedora
```

### 3. Alternative Audio Libraries

If PyAudio continues to cause issues, consider these alternatives:

**sounddevice** (easier to install):
```bash
pip install sounddevice
```

**pyalsaaudio** (Linux only):
```bash
pip install pyalsaaudio
```

## Troubleshooting Tips

### 1. Check Architecture Compatibility

For Apple Silicon Macs, ensure you're using the correct Python:
```bash
python -c "import platform; print(platform.machine())"
# Should show 'arm64' for Apple Silicon
```

### 2. Virtual Environment Issues

Sometimes the issue is with the virtual environment:
```bash
# Recreate venv
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
# Install dependencies again
```

### 3. Compiler Issues

Set compiler flags explicitly:
```bash
# macOS with Homebrew
export CPPFLAGS="-I$(brew --prefix)/include"
export LDFLAGS="-L$(brew --prefix)/lib"
pip install pyaudio
```

### 4. Permission Issues

On some systems:
```bash
# Use --user flag
pip install --user pyaudio

# Or fix permissions
sudo chown -R $(whoami) /path/to/venv
```

## Testing Installation

After successful installation, test with:

```python
import pyaudio
import numpy as np

def test_pyaudio():
    p = pyaudio.PyAudio()
    print(f"PyAudio version: {pyaudio.__version__}")
    print(f"Available audio devices: {p.get_device_count()}")

    # List input devices
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info['maxInputChannels'] > 0:
            print(f"Input device {i}: {info['name']}")

    p.terminate()
    print("✅ PyAudio working correctly!")

if __name__ == "__main__":
    test_pyaudio()
```

## Project-Specific Setup

For this voice cloning project, after installing PyAudio:

1. **Install all dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test voice recording:**
   ```bash
   python voice_cloner.py
   ```

3. **Verify microphone access:**
   - macOS: Grant microphone permissions when prompted
   - Linux: Check ALSA/PulseAudio configuration
   - Windows: Verify microphone drivers

## Error Reference

| Error | Platform | Solution |
|-------|----------|----------|
| `portaudio.h not found` | macOS | `brew install portaudio` |
| `portaudio.h not found` | Ubuntu | `sudo apt install portaudio19-dev` |
| `Microsoft Visual C++ required` | Windows | Install MSVC Build Tools |
| `Permission denied` | All | Use `--user` flag or fix venv permissions |
| `Architecture mismatch` | macOS M1/M2 | Use native ARM64 Python |

## Last Resort Solutions

1. **Use Docker:**
   ```dockerfile
   FROM python:3.11-slim
   RUN apt-get update && apt-get install -y portaudio19-dev
   RUN pip install pyaudio
   ```

2. **Use pre-built wheels from third parties:**
   ```bash
   pip install https://download.lfd.uci.edu/pythonlibs/archived/PyAudio-0.2.11-cp39-cp39-win_amd64.whl
   ```

3. **Switch to alternative libraries** (see alternatives section above)

---

*Last updated: 2024 - Tested on macOS 15.0 (ARM64), Ubuntu 22.04, Windows 11*