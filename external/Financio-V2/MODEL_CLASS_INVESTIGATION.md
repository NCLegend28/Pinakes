# Model Class Investigation Summary

## Issue
Model loading was reporting 2 classes but predictions were outputting 3-class probabilities.

## Investigation Findings

### 1. Model Configuration
All models in the system are **3-class models** (Sell/Hold/Buy):
- **Objective**: `multi:softprob` (multiclass softmax)
- **Num Classes**: 3
- **Classes**: 0=Sell, 1=Hold, 2=Buy

### 2. Root Cause
The `model_loader.py` was checking for `num_class` in the wrong location:

```python
# OLD CODE (WRONG)
num_class = booster.attributes().get("num_class")  # Returns None
```

**Why it failed:**
- XGBoost 3.x stores `num_class` in the model **CONFIG**, not **ATTRIBUTES**
- Attributes is a separate key-value store that must be explicitly set
- Since attributes were empty, it defaulted to `n_classes_ = 2`

### 3. Model Storage Locations
XGBoost models store `num_class` in multiple places:

| Location | Value | Accessible Via |
|----------|-------|----------------|
| **Config** | `"num_class": "3"` | `json.loads(booster.save_config())` |
| **Attributes** | Empty `{}` | `booster.attributes()` |
| **Feature Params** | `"num_class": 3` | `AAPL_feature_params.json` |

### 4. The Fix
Updated `_fix_model_classes_simple()` to read from config:

```python
# NEW CODE (CORRECT)
# Try attributes first (legacy compatibility)
num_class = booster.attributes().get("num_class")

if num_class is None:
    # Read from model config (XGBoost 3.x)
    config = json.loads(booster.save_config())
    learner_params = config.get("learner", {}).get("learner_model_param", {})
    num_class = learner_params.get("num_class")
    
model.n_classes_ = int(num_class)  # Now correctly = 3
```

## Migration History

### Phase 1: 2-Class Models (Legacy)
- **Purpose**: Web scraping / binary classification
- **Classes**: 0=Sell, 1=Buy
- **Use case**: Simple bullish/bearish signals

### Phase 2: 3-Class Models (Current)
- **Purpose**: Algorithmic trading with risk management
- **Classes**: 0=Sell, 1=Hold, 2=Buy
- **Use case**: More nuanced trading decisions
- **Added**: Hold signal to avoid overtrading

## Verification Results

All test models now correctly load as 3-class:

```
✅ AAPL: 3 classes, 61 features
✅ TSLA: 3 classes, 61 features
✅ NVDA: 3 classes, 61 features
```

**Sample prediction output:**
```
Shape: (1, 3) - [Sell_prob, Hold_prob, Buy_prob]
Example: [0.466, 0.322, 0.212] → SELL (highest probability)
```

## Files Modified

1. **requirements.txt**
   - Updated: `torch==2.2.2` → `torch>=2.3.0`
   - Reason: Compatibility with `stable-baselines3==2.6.0`

2. **financio_src/utils/model_loader.py**
   - Fixed: `_fix_model_classes_simple()` to read from config
   - Added: Proper 3-class detection logic

3. **tests/test_model_loading_fix.py**
   - Updated: Use proper `model_loader` utilities
   - Removed: Duplicate code that set read-only `classes_` attribute

## System Impact

**No breaking changes** - All existing code will continue to work because:
- Models are already 3-class (this was just a detection bug)
- Predictions already returned 3-class probabilities
- The fix simply corrects the `n_classes_` metadata

## Recommendations

1. **Future Training**: Consider explicitly setting booster attributes:
   ```python
   booster.set_attr(num_class="3")
   booster.set_attr(model_type="three_class")
   ```

2. **Validation**: Add CI/CD check to verify all models are 3-class

3. **Documentation**: Update training docs to clarify 3-class system

---
**Date**: 2025-12-31
**Status**: ✅ RESOLVED
