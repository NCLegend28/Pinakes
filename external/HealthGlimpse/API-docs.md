# HealthGlimpse+ API Documentation

## Overview

The HealthGlimpse+ API provides programmatic access to all core functionality of the offline health assistant. All endpoints work completely offline and do not require internet connectivity.

**Base URL**: `http://localhost:5000/api`

**Content-Type**: `application/json`

**Authentication**: None required (local application)

## API Endpoints

### System Health Check

Check the overall system status and component health.

```http
GET /api/health-check
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-07T12:00:00Z",
  "offline_mode": true,
  "components": {
    "symptom_analyzer": true,
    "emergency_nav": true,
    "audio_monitor": false,
    "gemma_sim": true
  }
}
```

**Status Codes:**
- `200 OK` - System is healthy
- `503 Service Unavailable` - System has issues

---

### Symptom Analysis

Analyze symptoms and provide medical recommendations.

```http
POST /api/analyze-symptoms
```

**Request Body:**
```json
{
  "symptoms": "I have a severe headache and feel nauseous",
  "image": "base64_encoded_image_data",
  "user_context": {
    "age": 35,
    "gender": "female",
    "medical_history": ["migraine", "hypertension"]
  }
}
```

**Parameters:**
- `symptoms` (string, required): Text description of symptoms
- `image` (string, optional): Base64 encoded image of visible symptoms
- `user_context` (object, optional): Additional user information

**Response:**
```json
{
  "condition": "Migraine Headache",
  "probability": 0.85,
  "severity": "Medium",
  "urgency_level": "Urgent",
  "recommendation": "Take prescribed migraine medication, rest in dark room",
  "seek_immediate_care": false,
  "emergency": false,
  "triage_category": "ESI-3",
  "follow_up_timeline": "Within 2-4 hours if symptoms persist",
  "all_recommendations": [
    "Take prescribed migraine medication",
    "Rest in a dark, quiet room",
    "Apply cold compress to forehead",
    "Stay hydrated",
    "Seek care if symptoms worsen"
  ],
  "likely_conditions": [
    {
      "condition": "Migraine Headache",
      "probability": 0.85,
      "severity": "medium"
    },
    {
      "condition": "Tension Headache", 
      "probability": 0.45,
      "severity": "low"
    }
  ],
  "confidence_level": "high",
  "processing_time": 0.234,
  "model_info": {
    "name": "Gemma 3n Simulator",
    "capabilities_used": ["text_analysis", "medical_reasoning", "triage_assessment"]
  }
}
```

**Status Codes:**
- `200 OK` - Analysis completed successfully
- `400 Bad Request` - Invalid request data
- `500 Internal Server Error` - Analysis failed

---

### Emergency Location Search

Find nearby emergency facilities and services.

```http
POST /api/find-emergency-locations
```

**Request Body:**
```json
{
  "location": {
    "lat": 40.7589,
    "lng": -73.9851
  },
  "type": "hospital",
  "max_distance": 5.0,
  "emergency": true
}
```

**Parameters:**
- `location` (object, required): User's current location
  - `lat` (number): Latitude
  - `lng` (number): Longitude
- `type` (string, optional): Facility type - `hospital`, `clinic`, `urgent_care`, `pharmacy`, `shelter`, `harm_reduction`
- `max_distance` (number, optional): Maximum search radius in miles (default: 5.0)
- `emergency` (boolean, optional): Prioritize emergency facilities

**Response:**
```json
[
  {
    "name": "Downtown General Hospital",
    "address": "123 Main Street, Downtown",
    "lat": 40.7589,
    "lng": -73.9851,
    "phone": "(555) 123-4567",
    "distance": 0.3,
    "walk_time": "6 minutes",
    "type": "hospital",
    "services": ["emergency", "trauma", "general", "surgery"],
    "hours": "24/7",
    "open_now": true,
    "accepts_uninsured": true,
    "languages": ["English", "Spanish"],
    "wheelchair_accessible": true,
    "trauma_level": "Level I",
    "emergency_room": true
  }
]
```

**Status Codes:**
- `200 OK` - Search completed successfully
- `400 Bad Request` - Invalid location or parameters
- `500 Internal Server Error` - Search failed

---

### Audio Monitoring Control

Start or stop distress monitoring.

```http
POST /api/start-monitoring
```

**Request Body:**
```json
{
  "sensitivity": "medium",
  "detection_types": ["keywords", "fall_detection", "medical_emergency"],
  "test_event": null
}
```

**Parameters:**
- `sensitivity` (string, optional): `low`, `medium`, `high` (default: `medium`)
- `detection_types` (array, optional): Types of events to detect
- `test_event` (string, optional): Simulate a test event for debugging

**Response:**
```json
{
  "status": "monitoring_started",
  "message": "Distress monitoring activated (medium sensitivity)",
  "config": {
    "sample_rate": 22050,
    "chunk_size": 1024,
    "threshold": 0.7,
    "continuous_monitoring": true,
    "keyword_detection": true,
    "pattern_analysis": true
  },
  "keywords": ["help", "emergency", "call 911", "i fell", "can't breathe"]
}
```

**Stop Monitoring:**
```http
POST /api/stop-monitoring
```

**Response:**
```json
{
  "status": "monitoring_stopped",
  "message": "Distress monitoring deactivated"
}
```

**Status Codes:**
- `200 OK` - Monitoring status changed successfully
- `400 Bad Request` - Invalid parameters
- `500 Internal Server Error` - Failed to change monitoring status

---

### Monitoring Status

Get current monitoring status and recent activity.

```http
GET /api/monitoring-status
```

**Response:**
```json
{
  "is_monitoring": true,
  "sensitivity": "medium",
  "uptime": "00:15:32",
  "events_detected": 3,
  "alerts_triggered": 1,
  "recent_events": [
    {
      "timestamp": "2025-01-07T12:15:00Z",
      "type": "background_noise",
      "confidence": 0.2,
      "action_taken": "none"
    },
    {
      "timestamp": "2025-01-07T12:10:00Z", 
      "type": "help_call",
      "confidence": 0.9,
      "action_taken": "emergency_alert"
    }
  ],
  "system_status": {
    "microphone": "active",
    "processing": "normal",
    "storage": "available",
    "battery": "good"
  }
}
```

**Status Codes:**
- `200 OK` - Status retrieved successfully
- `500 Internal Server Error` - Failed to get status

---

## Error Handling

All API endpoints return consistent error responses:

```json
{
  "error": true,
  "error_code": "INVALID_REQUEST",
  "message": "Invalid request format",
  "details": "Missing required field: symptoms",
  "timestamp": "2025-01-07T12:00:00Z"
}
```

**Common Error Codes:**
- `INVALID_REQUEST` - Malformed request
- `MISSING_DATA` - Required data files not found
- `ANALYSIS_FAILED` - Symptom analysis failed
- `LOCATION_ERROR` - Location search failed
- `MONITORING_ERROR` - Audio monitoring error
- `SYSTEM_ERROR` - General system error

## Rate Limiting

- Default limit: 100 requests per minute per IP
- Monitoring endpoints: 10 requests per minute
- No authentication required for local use

## Data Privacy

- All data processing happens locally
- No data is sent to external servers
- Audio data is not permanently stored
- Image uploads are processed locally and can be automatically deleted

## SDK Examples

### Python Example

```python
import requests
import json

# Analyze symptoms
def analyze_symptoms(symptoms_text):
    url = "http://localhost:5000/api/analyze-symptoms"
    data = {"symptoms": symptoms_text}
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Find nearby hospitals
def find_hospitals(lat, lng):
    url = "http://localhost:5000/api/find-emergency-locations"
    data = {
        "location": {"lat": lat, "lng": lng},
        "type": "hospital"
    }
    
    response = requests.post(url, json=data)
    return response.json() if response.status_code == 200 else []

# Usage
result = analyze_symptoms("I have chest pain and shortness of breath")
hospitals = find_hospitals(40.7589, -73.9851)
```

### JavaScript Example

```javascript
// Analyze symptoms
async function analyzeSymptoms(symptomsText) {
    const response = await fetch('/api/analyze-symptoms', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            symptoms: symptomsText
        })
    });
    
    if (response.ok) {
        return await response.json();
    } else {
        throw new Error(`Analysis failed: ${response.status}`);
    }
}

// Start monitoring
async function startMonitoring(sensitivity = 'medium') {
    const response = await fetch('/api/start-monitoring', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            sensitivity: sensitivity
        })
    });
    
    return await response.json();
}

// Usage
analyzeSymptoms("headache and fever")
    .then(result => console.log(result))
    .catch(error => console.error(error));
```

### cURL Examples

```bash
# Health check
curl -X GET http://localhost:5000/api/health-check

# Analyze symptoms
curl -X POST http://localhost:5000/api/analyze-symptoms \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "severe headache and nausea"}'

# Find nearby clinics
curl -X POST http://localhost:5000/api/find-emergency-locations \
  -H "Content-Type: application/json" \
  -d '{
    "location": {"lat": 40.7589, "lng": -73.9851},
    "type": "clinic",
    "max_distance": 3.0
  }'

# Start monitoring
curl -X POST http://localhost:5000/api/start-monitoring \
  -H "Content-Type: application/json" \
  -d '{"sensitivity": "high"}'
```

## Webhooks (Future Feature)

For production deployments, webhook support may be added for real-time notifications:

```json
{
  "webhook_url": "http://localhost:8080/webhooks/emergency",
  "events": ["emergency_detected", "monitoring_started", "system_error"],
  "secret": "webhook_secret_key"
}
```

## Batch Processing

For processing multiple requests efficiently:

```http
POST /api/batch-analyze
```

```json
{
  "requests": [
    {"symptoms": "headache"},
    {"symptoms": "chest pain"},
    {"symptoms": "nausea"}
  ]
}
```

## API Versioning

Current API version: `v1`

Future versions will be accessible via:
- URL: `/api/v2/analyze-symptoms`
- Header: `API-Version: v2`

## Support

For API support and bug reports:
- Check application logs: `healthglimpse.log`
- Test with minimal requests first
- Verify all required data files are present
- Ensure proper JSON formatting

## Testing

Use the included test script to verify API functionality:

```bash
python test_system.py
```

This will test all API endpoints and verify responses.