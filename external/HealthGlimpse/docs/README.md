# HealthGlimpse+ - Offline Health Assistant

![HealthGlimpse+ Logo](https://img.shields.io/badge/HealthGlimpse+-Offline%20Health%20Assistant-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Flask](https://img.shields.io/badge/Flask-2.3+-red)
![Status](https://img.shields.io/badge/Status-Proof%20of%20Concept-yellow)

## Overview

HealthGlimpse+ is a **privacy-first, offline health assistant** designed for vulnerable populations including the unhoused, rural communities, disaster survivors, and refugees. It provides AI-powered symptom analysis, emergency navigation, and autonomous distress detection - all without requiring an internet connection.

### Key Features

- 🩺 **AI Symptom Analysis** - Multimodal health assessment using text, voice, and images
- 🗺️ **Offline Emergency Navigation** - Find nearby hospitals, clinics, and shelters
- 🎤 **Distress Monitoring** - Passive audio monitoring for emergency situations
- 🔒 **Privacy-First** - All data remains on device, no cloud connectivity required
- 🌐 **Offline-First** - Works in areas with no internet connectivity
- ♿ **Accessibility** - Designed for users with various accessibility needs

## Project Structure

```
healthglimpse_plus/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── static/              # CSS, JS, images
├── templates/           # HTML templates
│   ├── index.html       # Main dashboard
│   ├── symptom_check.html
│   ├── emergency_nav.html
│   └── distress_monitor.html
├── data/               # Offline databases
│   ├── symptoms.json   # Medical knowledge base
│   └── locations.json  # Emergency locations
├── models/            # AI simulation
│   └── gemma_simulator.py
├── utils/             # Core functionality
│   ├── symptom_analyzer.py
│   ├── navigation.py
│   └── audio_monitor.py
└── docs/              # Additional documentation
    └── API.md
```

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Modern web browser
- Microphone access (for distress monitoring)

### Installation

1. **Clone or download the project files**
   ```bash
   # If using git
   git clone <repository-url>
   cd healthglimpse_plus
   
   # Or extract downloaded files
   unzip healthglimpse_plus.zip
   cd healthglimpse_plus
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create required directories**
   ```bash
   mkdir -p data uploads static/css static/js static/images
   ```

5. **Setup data files**
   ```bash
   # Copy the provided JSON files to the data directory
   cp symptoms.json data/
   cp locations.json data/
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   Open your browser and navigate to: `http://localhost:5000`

## Detailed Setup Guide

### Step-by-Step Installation

#### 1. Environment Setup

Create a new directory for the project:
```bash
mkdir healthglimpse_plus
cd healthglimpse_plus
```

#### 2. Python Dependencies

Install required packages:
```bash
pip install Flask==2.3.3
pip install numpy==1.24.3
pip install pandas==1.5.3
pip install requests==2.31.0
pip install Pillow==10.0.1
pip install python-dotenv==1.0.0
```

**Note**: Audio processing libraries (pyaudio, speechrecognition) are optional for POC and may require additional system dependencies.

#### 3. File Structure Creation

Create the necessary directories and files:
```bash
# Main application files
touch app.py config.py requirements.txt

# Create directory structure
mkdir -p static/{css,js,images}
mkdir -p templates
mkdir -p data
mkdir -p models
mkdir -p utils
mkdir -p docs
mkdir uploads
```

#### 4. Data Files Setup

Ensure the JSON data files are in the correct location:
- `data/symptoms.json` - Medical knowledge base
- `data/locations.json` - Emergency facilities database

#### 5. Testing the Installation

Run the application:
```bash
python app.py
```

You should see output similar to:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

## Core Components

### 1. Symptom Analyzer (`utils/symptom_analyzer.py`)

**Purpose**: Analyzes user-reported symptoms and provides medical guidance.

**Features**:
- Text-based symptom analysis
- Image-based symptom detection (simulated)
- Emergency condition detection
- Triage recommendations

**Key Functions**:
- `analyze_text_symptoms(symptom_text)` - Process text descriptions
- `analyze_image_symptoms(image_data)` - Analyze symptom photos
- `get_triage_priority(analysis_result)` - Determine urgency level

### 2. Emergency Navigation (`utils/navigation.py`)

**Purpose**: Helps users find nearby emergency facilities and services.

**Features**:
- Offline location database
- Distance calculation
- Walking directions
- Facility filtering

**Key Functions**:
- `find_nearby(location, type, max_distance)` - Find nearby facilities
- `find_emergency_locations(location, emergency_type)` - Emergency-specific search
- `get_walking_directions(start, end)` - Basic navigation

### 3. Audio Monitor (`utils/audio_monitor.py`)

**Purpose**: Passive monitoring for distress calls and emergency situations.

**Features**:
- Keyword detection ("Help!", "Emergency!")
- Fall detection patterns
- Emergency broadcasting
- Configurable sensitivity

**Key Functions**:
- `start_monitoring()` - Begin audio monitoring
- `stop_monitoring()` - End monitoring
- `simulate_distress_event(event_type)` - Testing function

### 4. Gemma 3n Simulator (`models/gemma_simulator.py`)

**Purpose**: Simulates AI model capabilities for medical analysis.

**Features**:
- Multimodal analysis simulation
- Medical reasoning
- Confidence scoring
- Triage categorization

## Usage Guide

### Symptom Analysis

1. Navigate to "Symptom Check" page
2. Describe symptoms in text box or use quick buttons
3. Optionally upload a photo of visible symptoms
4. Click "Analyze Symptoms"
5. Review results and recommendations

### Emergency Navigation

1. Go to "Emergency Nav" page
2. Set your location (manually or via GPS)
3. Select facility type (hospital, clinic, etc.)
4. Click "Find Locations"
5. View results on map and list
6. Get directions to selected facility

### Distress Monitoring

1. Access "Distress Monitor" page
2. Grant microphone permission
3. Configure sensitivity and detection types
4. Click "Start Monitoring"
5. System will passively listen for emergency situations

## Configuration

### Application Settings

Edit `config.py` to modify application behavior:

```python
class Config:
    DEBUG = True                    # Enable debug mode
    OFFLINE_MODE = True            # Force offline operation
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB upload limit
    UPLOAD_FOLDER = 'uploads'      # File upload directory
    DATA_FOLDER = 'data'          # Database directory
```

### Data Configuration

#### Symptoms Database (`data/symptoms.json`)
- Add new medical conditions
- Update treatment recommendations
- Modify emergency keywords

#### Locations Database (`data/locations.json`)
- Add local emergency facilities
- Update contact information
- Modify service offerings

## Known Issues and Fixes

### Issue #1: Module Import Errors
**Problem**: ImportError when starting application
```
ImportError: No module named 'utils.symptom_analyzer'
```

**Solution**: 
1. Ensure all Python files are in correct directories
2. Add `__init__.py` files to make directories Python packages:
```bash
touch utils/__init__.py
touch models/__init__.py
```

**Fix Applied**: Added proper Python package structure

### Issue #2: Audio Permissions in Browser
**Problem**: Microphone access denied in some browsers

**Solution**:
1. Ensure HTTPS is used in production
2. For local development, use `localhost` (not `127.0.0.1`)
3. Check browser permissions settings

**Fix Applied**: Added permission request handling and fallback simulation

### Issue #3: Large File Upload Errors
**Problem**: Image uploads failing for large files

**Solution**: 
1. Increased `MAX_CONTENT_LENGTH` in config
2. Added client-side image compression
3. Implemented file size validation

**Fix Applied**: Updated configuration and added validation

### Issue #4: JSON Data Loading Failures
**Problem**: Application crashes if data files are missing

**Solution**:
1. Added fallback data creation
2. Implemented graceful error handling
3. Created default data when files missing

**Fix Applied**: Added robust error handling in data loading functions

### Issue #5: Cross-Browser Compatibility
**Problem**: Some features not working in older browsers

**Solution**:
1. Added polyfills for modern JavaScript features
2. Implemented progressive enhancement
3. Added feature detection

**Fix Applied**: Updated JavaScript to support broader browser compatibility

## API Documentation

### Health Check
```
GET /api/health-check
```
Returns system status and component health.

### Symptom Analysis
```
POST /api/analyze-symptoms
Content-Type: application/json

{
  "symptoms": "headache and fever",
  "image": "base64_encoded_image_data"
}
```

### Location Search
```
POST /api/find-emergency-locations
Content-Type: application/json

{
  "location": {"lat": 40.7589, "lng": -73.9851},
  "type": "hospital"
}
```

### Start Monitoring
```
POST /api/start-monitoring
Content-Type: application/json

{
  "sensitivity": "medium"
}
```

## Development Notes

### Gemma 3n Integration
Currently using a simulator for POC. For production integration:

1. Install Gemma 3n dependencies
2. Replace `GemmaSimulator` with actual model calls
3. Update model paths in configuration

### Offline Maps
For true offline capability:
1. Download OpenStreetMap tiles for coverage area
2. Store in `static/maps/` directory
3. Configure tile server in navigation component

### Audio Processing
For production audio monitoring:
1. Install `pyaudio` and system audio libraries
2. Implement WebRTC for browser audio capture
3. Add voice recognition models

## Security Considerations

### Data Privacy
- All data remains on device
- No telemetry or tracking
- Optional encrypted local storage

### File Uploads
- Image uploads are sanitized
- File type validation implemented
- Size limits enforced

### Audio Monitoring
- Microphone access requires explicit permission
- Audio data not stored permanently
- Processing happens locally only

## Testing

### Unit Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test module
python -m pytest tests/test_symptom_analyzer.py
```

### Manual Testing
1. Test symptom analysis with various inputs
2. Verify location search functionality
3. Test audio monitoring permissions
4. Check mobile responsiveness

### Test Data
Use the included test cases:
- Emergency scenarios
- Common symptoms
- Location searches
- Audio event simulation

## Deployment

### Local Deployment
For demo/POC use:
```bash
python app.py
```

### Production Deployment
For production deployment:
1. Use WSGI server (gunicorn)
2. Configure HTTPS
3. Set up proper logging
4. Configure system service

```bash
# Example production command
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Contributing

### Development Setup
1. Fork the repository
2. Create feature branch
3. Follow code style guidelines
4. Add tests for new features
5. Update documentation

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to all functions
- Comment complex logic

## Support

### Getting Help
- Check this README for common issues
- Review the logs for error messages
- Test with minimal configuration first

### Reporting Issues
When reporting issues, include:
1. Error message (full traceback)
2. Steps to reproduce
3. System information (OS, Python version)
4. Configuration details

## License

This project is a proof of concept for demonstration purposes.

## Acknowledgments

- Built with Flask web framework
- Uses Bootstrap for responsive design
- Inspired by the need for accessible healthcare technology
- Designed for vulnerable populations who need it most

---

**Note**: This is a proof of concept. For production use, additional security, testing, and medical validation would be required.