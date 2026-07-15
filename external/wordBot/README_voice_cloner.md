# 🎤 Voice Cloner

A powerful Python application that can clone voices from audio samples and generate speech with new text using state-of-the-art TTS models.

## Features

- **Quick Voice Cloning**: Clone any voice from a short audio sample (3-30 seconds)
- **Voice Profiles**: Create and reuse voice profiles for consistent results
- **Multiple Languages**: Support for 15+ languages including English, Spanish, French, German, etc.
- **Audio Processing**: Built-in audio enhancement and optimization
- **CLI Interface**: Easy-to-use command line interface with progress indicators
- **Interactive Mode**: Interactive session for experimenting with different voices

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install system audio tools (optional):**
   ```bash
   # macOS
   brew install sox

   # Ubuntu/Debian
   sudo apt install sox
   ```

## Quick Start

### 1. Quick Voice Cloning
Clone a voice and generate speech in one command:

```bash
python voice_cli.py quick \
  --audio reference_voice.wav \
  --text "Hello, this is a cloned voice!" \
  --output generated_speech.wav
```

### 2. Create Voice Profile
Create a reusable voice profile:

```bash
python voice_cli.py create-profile \
  --name "john" \
  --audio john_voice_sample.wav
```

### 3. Use Voice Profile
Generate speech using the saved profile:

```bash
python voice_cli.py clone \
  --profile "john" \
  --text "Any text you want to say" \
  --output output.wav
```

## Usage Examples

### Command Line Interface

```bash
# Get help
python voice_cli.py --help

# Quick cloning with language specification
python voice_cli.py quick -a voice.wav -t "Bonjour le monde" -o french.wav -l fr

# List all profiles
python voice_cli.py profiles

# Show system information
python voice_cli.py info

# Interactive mode
python voice_cli.py interactive
```

### Programmatic Usage

```python
from voice_cloner import VoiceCloner

# Initialize cloner
cloner = VoiceCloner()

# Quick clone
success = cloner.quick_clone(
    reference_audio="speaker.wav",
    text="Hello world!",
    output_path="output.wav"
)

# Create profile
cloner.create_voice_profile("alice", "alice_voice.wav")

# Use profile
cloner.clone_voice("New text here", "alice", "result.wav")
```

## Audio Requirements

### Optimal Audio Quality
- **Duration**: 10-30 seconds of clear speech
- **Format**: WAV, MP3, or FLAC
- **Content**: Single speaker, minimal background noise
- **Quality**: Clear pronunciation, natural pace

### Audio Preprocessing
The application automatically:
- Trims silence from beginning/end
- Normalizes volume levels
- Applies noise reduction
- Limits duration to 30 seconds

### Quality Validation
```bash
python audio_utils.py  # Analyze audio quality
```

## Supported Languages

English (en), Spanish (es), French (fr), German (de), Italian (it), Portuguese (pt), Polish (pl), Turkish (tr), Russian (ru), Dutch (nl), Czech (cs), Arabic (ar), Chinese (zh-cn), Japanese (ja), Hungarian (hu), Korean (ko)

## Configuration

### GPU Acceleration
The application automatically uses GPU if available:
- NVIDIA GPU with CUDA support
- Significantly faster processing times
- Automatic fallback to CPU

### Model Selection
Default model: `tts_models/multilingual/multi-dataset/xtts_v2`

To use a different model:
```python
cloner = VoiceCloner("tts_models/en/ljspeech/tacotron2-DDC")
```

## Performance Tips

1. **Use high-quality reference audio** (clear, noise-free)
2. **Keep reference clips short** (10-30 seconds optimal)
3. **Use GPU acceleration** when available
4. **Preprocess audio** for better results
5. **Create profiles** for frequently used voices

## Troubleshooting

### Common Issues

**"Model failed to load"**
- Install PyTorch with CUDA support
- Check internet connection for model download
- Verify disk space (models are ~1GB)

**"Poor voice quality"**
- Use higher quality reference audio
- Try longer reference samples (up to 30s)
- Ensure single speaker in reference
- Check audio format compatibility

**"CUDA out of memory"**
- Reduce batch size or switch to CPU
- Close other GPU applications
- Use shorter text inputs

### Audio Format Issues
```bash
# Convert audio format
ffmpeg -i input.mp3 -ar 22050 -ac 1 output.wav
```

## Examples Directory

Sample audio files and scripts:
- `examples/sample_voice.wav` - Example reference voice
- `examples/test_cloning.py` - Test script
- `examples/batch_process.py` - Batch processing script

## API Reference

### VoiceCloner Class

```python
class VoiceCloner:
    def __init__(self, model_name: str)
    def create_voice_profile(self, name: str, reference_audio: str) -> bool
    def clone_voice(self, text: str, profile_name: str, output_path: str) -> bool
    def quick_clone(self, reference_audio: str, text: str, output_path: str) -> bool
    def list_profiles(self) -> None
    def get_model_info(self) -> dict
```

### AudioProcessor Class

```python
class AudioProcessor:
    @staticmethod
    def get_audio_info(file_path: str) -> dict
    @staticmethod
    def create_optimized_reference(input_path: str) -> str
    @staticmethod
    def trim_silence(data: np.ndarray) -> np.ndarray
    @staticmethod
    def normalize_audio(data: np.ndarray) -> np.ndarray
```

## License

This project uses the Coqui TTS library. Please check their license terms for commercial usage.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with various audio samples
5. Submit a pull request

## Acknowledgments

- Built with [Coqui TTS](https://github.com/coqui-ai/TTS)
- Powered by [XTTS-v2](https://huggingface.co/coqui/XTTS-v2) model
- Audio processing with librosa and soundfile