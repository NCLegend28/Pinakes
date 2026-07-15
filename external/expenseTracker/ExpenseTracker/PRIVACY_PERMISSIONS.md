# Privacy Permissions Setup

To fix the camera and location crashes, you need to add these privacy permission descriptions to your Xcode project:

## How to Add Permissions in Xcode:

1. **Open Xcode Project**: Open `ExpenseTracker.xcodeproj`
2. **Select Target**: Click on "ExpenseTracker" target in the project navigator
3. **Go to Info Tab**: Click on the "Info" tab
4. **Add Custom iOS Target Properties**: Click the "+" button to add new entries

## Required Privacy Permissions:

Add these exact keys and descriptions:

### Camera Access
**Key**: `NSCameraUsageDescription`
**Value**: `ExpenseTracker needs camera access to scan receipts and extract expense information using OCR technology.`

### Photo Library Access
**Key**: `NSPhotoLibraryUsageDescription`
**Value**: `ExpenseTracker needs photo library access to import receipt images and PDF documents for expense processing.`

### Location When In Use
**Key**: `NSLocationWhenInUseUsageDescription`
**Value**: `ExpenseTracker needs location access to automatically track your business trips and calculate mileage for tax deductions.`

### Location Always (Optional - for background tracking)
**Key**: `NSLocationAlwaysAndWhenInUseUsageDescription`
**Value**: `ExpenseTracker needs location access to automatically track your business trips and calculate mileage for tax deductions, even when the app is in the background.`

### Document Access
**Key**: `NSDocumentPickerUsageDescription`
**Value**: `ExpenseTracker needs access to documents to import PDF receipts and tax documents for automated expense extraction.`

## Alternative Method - Raw Info.plist:

If you prefer to edit the Info.plist file directly, add these entries:

```xml
<key>NSCameraUsageDescription</key>
<string>ExpenseTracker needs camera access to scan receipts and extract expense information using OCR technology.</string>

<key>NSPhotoLibraryUsageDescription</key>
<string>ExpenseTracker needs photo library access to import receipt images and PDF documents for expense processing.</string>

<key>NSLocationWhenInUseUsageDescription</key>
<string>ExpenseTracker needs location access to automatically track your business trips and calculate mileage for tax deductions.</string>

<key>NSLocationAlwaysAndWhenInUseUsageDescription</key>
<string>ExpenseTracker needs location access to automatically track your business trips and calculate mileage for tax deductions, even when the app is in the background.</string>

<key>NSDocumentPickerUsageDescription</key>
<string>ExpenseTracker needs access to documents to import PDF receipts and tax documents for automated expense extraction.</string>
```

## After Adding Permissions:

1. **Clean Build**: Product → Clean Build Folder (Cmd+Shift+K)
2. **Rebuild**: Product → Build (Cmd+B)
3. **Install on Device**: Run on your physical device
4. **Test Permissions**: The first time you use camera/location features, iOS will show permission dialogs

## Troubleshooting:

- If the app still crashes, make sure all permission keys are spelled exactly as shown above
- Check that the target is set correctly in Xcode
- Verify your device is selected (not simulator) when testing
- If permissions don't appear, delete the app from your device and reinstall

Once you add these permissions, the camera OCR and mileage tracking should work properly on your device!