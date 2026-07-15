# Gesture-to-Music System 🎵

Turn hand gestures into musical instruments using AI! This system uses MPU6050 sensors on gloves to capture hand movements and translates them into musical notes in real-time.

## 🎯 Project Overview

**Hardware:**
- Arduino Mega
- 5× MPU6050 IMU sensors per glove (one per finger)
- Multiplexer for I2C communication
- Latex gloves

**Software:**
- Python-based data collection and ML pipeline
- LSTM/CNN models for gesture recognition
- MIDI output for instrument control
- Real-time inference

**Current Goal:**
First iteration maps 5 hand gestures to trumpet notes (chromatic scale).

## 📁 Project Structure

```
gesture_music_system/
├── config/
│   └── config.py              # System configuration
├── data/
│   ├── raw/                   # Raw sensor data (JSON)
│   └── processed/             # Preprocessed arrays
├── models/
│   └── gesture_model.py       # ML model architecture
├── utils/
│   ├── data_collector.py      # Arduino interface
│   ├── data_simulator.py      # Testing without hardware
│   ├── data_processor.py      # Data preprocessing
│   └── visualizer.py          # Data visualization
├── main.py                    # Main interface (start here!)
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Test Without Hardware (Recommended First Step)

```bash
python main.py
```

Choose option 1 to generate simulated data, then follow the pipeline:
- Option 1: Generate simulated dataset (50 samples per gesture)
- Option 5: Preprocess data
- Option 6: Train LSTM model
- Option 9: Test with simulated data

### 3. With Real Hardware

**Arduino Setup:**
1. Connect MPU6050 sensors through multiplexer
2. Upload Arduino code that sends sensor data via serial
3. Data format: `sensor1_ax,ay,az,gx,gy,gz,sensor2_ax,...` (30 values total)
4. Baud rate: 115200

**Data Collection:**
```bash
python main.py
# Choose option 2: Collect data from Arduino
# Follow prompts to record gestures
```

## 📊 Workflow

### Phase 1: Data Collection
1. **Generate simulated data** (for testing) OR **collect real data** from Arduino
2. Record 50-100 samples per gesture
3. Vary speed, angle, intensity for robustness

### Phase 2: Training
1. **Preprocess data**: Creates windowed samples, normalizes, splits train/val/test
2. **Train model**: Choose LSTM (better temporal) or CNN (faster)
3. **Evaluate**: Check accuracy, confusion matrix

### Phase 3: Real-Time Use
1. Load trained model
2. Stream sensor data
3. Predict gestures in real-time
4. Map to MIDI notes/actions

## 🎮 Gesture Definitions

| Gesture | Description | Trumpet Note |
|---------|-------------|--------------|
| Null | Neutral hand | (silence) |
| Fist | All fingers closed | C (60) |
| Point | Index extended | D (62) |
| Peace | Index + middle | E (64) |
| Three | Index + middle + ring | F (65) |
| Open | All fingers extended | G (67) |

## 🔧 Configuration

Edit `config/config.py` to customize:
- Sensor settings (sample rate, window size)
- Model hyperparameters (LSTM units, dropout)
- Gesture definitions and MIDI mappings
- Training parameters (epochs, batch size)

## 📈 Model Performance

**Target Metrics:**
- Accuracy: >90% on validation set
- Latency: <50ms (real-time requirement)
- Confidence threshold: >0.7 to trigger action

## 🎹 Musical Mapping Examples

### Trumpet (Current Implementation)
- Left hand: Note selection (5 gestures = 5 notes)
- Right hand: TBD (articulation, volume, effects)

### Future Instruments

**Piano:**
- 10 fingers = 10 piano keys
- Continuous hand height = velocity

**Drums:**
- Different gestures = different drums
- Strike speed = velocity

**Synth:**
- Continuous hand movements = filter/oscillator control
- Multi-dimensional gesture control

## 🛠️ Arduino Code Template

```cpp
#include <Wire.h>
#include <MPU6050.h>

MPU6050 sensors[5];  // One per finger

void setup() {
  Serial.begin(115200);
  Wire.begin();
  
  // Initialize sensors on multiplexer channels
  for(int i = 0; i < 5; i++) {
    selectMuxChannel(i);
    sensors[i].initialize();
  }
}

void loop() {
  // Read all sensors
  for(int i = 0; i < 5; i++) {
    selectMuxChannel(i);
    
    int16_t ax, ay, az, gx, gy, gz;
    sensors[i].getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
    
    Serial.print(ax); Serial.print(",");
    Serial.print(ay); Serial.print(",");
    Serial.print(az); Serial.print(",");
    Serial.print(gx); Serial.print(",");
    Serial.print(gy); Serial.print(",");
    Serial.print(gz);
    
    if(i < 4) Serial.print(",");
  }
  Serial.println();
  
  delay(10);  // 100Hz sampling
}
```

## 🐛 Troubleshooting

**"Serial port not found"**
- Check Arduino connection
- Linux: `/dev/ttyACM0` or `/dev/ttyUSB0`
- Windows: `COM3`, `COM4`, etc.
- Mac: `/dev/cu.usbmodem*`

**"No training data found"**
- Run data collection (option 1 or 2) first
- Check `data/raw/` directory has JSON files

**"Model accuracy too low"**
- Collect more training data (100+ samples per gesture)
- Ensure gesture execution is consistent
- Try different model architecture (LSTM vs CNN)
- Increase training epochs

**"Latency too high in real-time"**
- Reduce window size (faster but less accurate)
- Use CNN instead of LSTM
- Optimize data pipeline (reduce serial communication overhead)

## 📚 Key Concepts

**Time-Series Windows:**
Each gesture is a sequence of sensor readings. We use sliding windows (e.g., 1 second = 100 samples) to capture the temporal pattern.

**LSTM vs CNN:**
- **LSTM**: Remembers past inputs, better for sequences with long dependencies (like a melody)
- **CNN**: Detects local patterns, faster inference (like recognizing a chord shape)

**Normalization:**
Raw sensor values vary widely. StandardScaler normalizes them to have zero mean and unit variance, making training more stable.

**Confidence Threshold:**
Only trigger actions when model confidence >70% to avoid false positives.

## 🎓 Learning Path

1. **Start with simulation** - Test entire pipeline without hardware
2. **Collect small dataset** - 10 samples per gesture, verify pipeline works
3. **Scale up collection** - 50-100 samples per gesture for robust model
4. **Train and iterate** - Try both architectures, tune hyperparameters
5. **Real-time testing** - Start with one glove, then expand

## 🚧 Roadmap

- [x] Data collection infrastructure
- [x] Data simulation for testing
- [x] Preprocessing pipeline
- [x] ML model training (LSTM & CNN)
- [x] Visualization tools
- [ ] Real-time inference loop
- [ ] MIDI integration
- [ ] Second glove integration
- [ ] Multiple instrument mappings
- [ ] Continuous gesture control (not just discrete)
- [ ] Performance optimization (<30ms latency)
- [ ] Web-based visualizer

## 🤝 Contributing

This is a personal project, but ideas welcome! Key areas:
- Arduino optimization
- Better gesture definitions
- Novel musical mappings
- Real-time performance tuning

## 📝 Notes

**Sensor Data Format:**
Each sample: `[accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z]` × 5 fingers = 30 values

**Data Flow:**
```
Arduino → Serial → Python → Preprocessing → Model → Prediction → MIDI → Sound
```

**Critical Latency Points:**
1. Serial communication: ~10ms
2. Data preprocessing: ~5ms
3. Model inference: ~10-30ms (depends on architecture)
4. MIDI output: ~5ms
Total: 30-50ms (acceptable for real-time music)

## 🎵 Philosophy

Think of this like learning an instrument:
- **Data collection** = Practice sessions
- **Training** = Muscle memory development
- **Real-time use** = Performance

Start simple (5 gestures, 1 instrument) and gradually expand. The goal is to make gesture control feel natural and expressive!

---

**Questions?** Check the main menu (`python main.py`) for guided workflows.

**Hardware not ready?** No problem! Use simulation mode to build and test everything.

**This is important to you.** Take it step by step. You've got the hardware, now you've got the software infrastructure. Let's finish this! 🚀
