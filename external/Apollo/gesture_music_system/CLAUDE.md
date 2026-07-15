# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Gesture-to-Music System: Converts hand gestures captured via MPU6050 sensors on gloves into musical notes using machine learning. Hardware consists of Arduino Mega with 5 IMU sensors per glove; software uses Python with TensorFlow for LSTM/CNN gesture recognition and MIDI output.

## Development Commands

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Check system setup
python main.py  # Choose option 11
```

### Quick Testing (Without Hardware)
```bash
# Run end-to-end demo with simulated data (2-3 minutes)
python quick_demo.py

# Interactive interface for all operations
python main.py
```

### Data Collection Workflow
```bash
# 1. Generate simulated data (for testing)
python main.py  # Option 1

# 2. OR collect from real Arduino
python main.py  # Option 2
# Serial ports: /dev/ttyACM0 (Linux), /dev/cu.usbmodem* (Mac), COM3+ (Windows)

# 3. Visualize collected data
python main.py  # Option 3

# 4. View dataset statistics
python main.py  # Option 4
```

### Training Workflow
```bash
# 1. Preprocess data (windowing, normalization, train/val/test split)
python main.py  # Option 5

# 2. Train LSTM model (better temporal patterns, slower)
python main.py  # Option 6

# 3. OR train CNN model (faster inference, good local patterns)
python main.py  # Option 7

# 4. Evaluate trained model
python main.py  # Option 8
```

### Testing
```bash
# Test with simulated data (no hardware)
python main.py  # Option 9

# Test with real Arduino (requires hardware)
python main.py  # Option 10
```

### Standalone Module Testing
Each module has a `__main__` block and can be run independently:
```bash
python utils/data_simulator.py
python utils/data_processor.py
python models/gesture_model.py
```

## Architecture

### Data Flow Pipeline
```
Arduino Sensors → Serial (115200 baud) → data_collector.py → JSON (data/raw/)
                                                                      ↓
MIDI Output ← gesture_model.py ← Normalized Arrays ← data_processor.py
              (predict_gesture)   (data/processed/)   (windowing + scaling)
```

### Module Responsibilities

**config/config.py**
- Central configuration for hardware (sensor count, sample rate, baud rate)
- Gesture definitions and MIDI note mappings
- Model hyperparameters (LSTM units, dropout, learning rate)
- File paths and constants

**utils/data_collector.py** (ArduinoDataCollector)
- Serial interface to Arduino at 115200 baud
- Expects 30 comma-separated values: 5 sensors × (3 accel + 3 gyro)
- Saves structured JSON: `{gesture, timestamp, samples: [{timestamp, sensors: [{sensor_id, accel: {x,y,z}, gyro: {x,y,z}}]}]}`
- Methods: `connect()`, `read_sample()`, `collect_gesture()`, `collect_all_gestures()`

**utils/data_simulator.py** (GestureDataSimulator)
- Generates physics-based synthetic sensor data for testing without hardware
- Each gesture has characteristic frequency, acceleration/gyro ranges, and finger patterns
- Outputs same JSON format as data_collector
- Method: `generate_dataset(samples_per_gesture=50, duration_per_sample=2.0)`

**utils/data_processor.py** (GestureDataProcessor)
- Converts raw JSON → training-ready numpy arrays
- **Sliding windows**: Creates overlapping 1-second windows (100 samples at 100Hz, 50% overlap)
- **Feature extraction**: Flattens sensor data to (window_size=100, num_features=30)
- **Normalization**: StandardScaler fitted on training data, applied to train/val/test
- **Splitting**: 70% train, 15% val, 15% test with stratification
- Saves: `processed_dataset.npz` (arrays) + `metadata.pkl` (scaler, label mappings)
- Critical for real-time: `scaler` must be reused for inference normalization

**models/gesture_model.py** (GestureRecognitionModel)
- Two architectures:
  - **LSTM**: 2 layers (64→32 units), good for temporal dependencies, slower inference
  - **CNN**: 3 conv blocks (64→128→64 filters), faster, good for local patterns
- Input shape: `(window_size=100, num_features=30)`
- Output: Softmax over 6 gesture classes
- Callbacks: EarlyStopping (patience=10), ModelCheckpoint (best val_accuracy), ReduceLROnPlateau
- Saves: `best_model_{lstm|cnn}.keras` and `final_model_{lstm|cnn}.keras`
- Real-time method: `predict_gesture(sensor_window)` returns `(gesture_name, confidence)`

**utils/visualizer.py** (GestureVisualizer)
- Plots raw sensor data (30 time series per gesture)
- Compares multiple gestures side-by-side
- Shows dataset statistics and label distributions

**main.py**
- Interactive CLI menu for entire workflow
- Guides user through: simulate/collect → preprocess → train → evaluate → test

### Key Design Patterns

**Sliding Window Architecture**
- Raw recordings are variable length; model needs fixed input size
- 1-second windows (100 samples) with 50% overlap create multiple training samples per recording
- Critical: Real-time system must maintain rolling window buffer of last 100 samples

**Two-Stage Normalization**
- Stage 1 (training): Fit StandardScaler on training set 2D reshaped data `(num_samples*window_size, num_features)`
- Stage 2 (inference): Transform new windows with same scaler (saved in metadata.pkl)
- **Must preserve scaler** from training for real-time use

**Model Architecture Choice**
- LSTM: Use when gestures have long-term temporal dependencies (e.g., drawing patterns in air)
- CNN: Use when gestures have distinctive instantaneous patterns (e.g., static hand shapes)
- Both use dropout (0.3) and early stopping to prevent overfitting

**Gesture Definitions** (config/config.py GESTURES dict)
- 0: null (neutral hand)
- 1: fist (all fingers closed)
- 2: point (index extended)
- 3: peace (index + middle)
- 4: three (index + middle + ring)
- 5: open_hand (all fingers extended)
- Maps to MIDI notes via GESTURE_TO_MIDI_NOTE dict (trumpet chromatic scale: C=60, D=62, E=64, F=65, G=67)

### Hardware Integration

**Arduino Serial Format**
- Baud: 115200
- Format: 30 comma-separated floats per line
- Order: sensor0_ax,ay,az,gx,gy,gz, sensor1_ax,ay,az,gx,gy,gz, ... sensor4_ax,ay,az,gx,gy,gz
- Sample rate: 100Hz (10ms delay in Arduino loop)

**MPU6050 Sensor Layout**
- 5 sensors per glove (one per finger: thumb, index, middle, ring, pinky)
- I2C via multiplexer (TCA9548A or similar)
- Accel range: ±16g, Gyro range: ±2000°/s

### Real-Time Inference (Not Yet Implemented)
When implementing real-time mode (main.py option 10):
1. Load trained model + saved scaler from metadata.pkl
2. Connect to Arduino serial
3. Maintain rolling buffer of last 100 samples
4. On each new sample:
   - Add to buffer, remove oldest
   - Extract features, normalize with scaler
   - Run model.predict_gesture()
   - If confidence > CONFIDENCE_THRESHOLD (0.7), trigger MIDI note
5. Target latency: <50ms (currently: ~10ms serial + ~5ms preprocessing + ~10-30ms inference + ~5ms MIDI)

### Data Storage Structure
```
data/
├── raw/                          # JSON files from collection/simulation
│   └── {gesture}_{timestamp}.json
└── processed/                    # Training-ready data
    ├── processed_dataset.npz     # X_train, y_train, X_val, y_val, X_test, y_test
    └── metadata.pkl              # scaler, label_to_int, int_to_label

models/
├── best_model_lstm.keras         # Best validation accuracy during training
├── final_model_lstm.keras        # Final epoch model
├── best_model_cnn.keras
├── final_model_cnn.keras
└── training_history_*.json       # Loss/accuracy curves
```

## Configuration Tuning

**Increase Accuracy**
- Collect more data: Increase SAMPLES_PER_GESTURE in simulator or collection loop
- Longer training: Increase EPOCHS (default: 50)
- More model capacity: Increase LSTM_UNITS or CNN filters

**Reduce Latency (for Real-Time)**
- Shorter windows: Decrease WINDOW_SIZE_MS (trades accuracy for speed)
- Use CNN instead of LSTM
- Reduce BATCH_SIZE for single-sample inference

**Add New Gestures**
1. Add to GESTURES dict in config.py
2. Add MIDI mapping to GESTURE_TO_MIDI_NOTE
3. Collect/simulate data for new gesture
4. Retrain model (num_classes auto-adjusts from len(GESTURES))

## Common Development Tasks

**Debugging Poor Model Performance**
1. Visualize data: `python main.py` → Option 3 (check if gestures look distinct)
2. Check label distribution: Option 4 (ensure balanced dataset)
3. Review confusion matrix: Option 8 (identify which gestures are confused)
4. Try alternate architecture: Train both LSTM and CNN, compare

**Testing Changes Without Hardware**
1. Generate fresh simulated data: Option 1
2. Modify simulator patterns in `utils/data_simulator.py` → `gesture_patterns` dict
3. Full pipeline test: `python quick_demo.py`

**Adding New Sensor Features**
1. Update AXES_PER_SENSOR and TOTAL_FEATURES in config.py
2. Modify data_collector.py `read_sample()` to parse new format
3. Update data_simulator.py to generate new features
4. Retrain preprocessing pipeline (scaler dimensions auto-adjust)
