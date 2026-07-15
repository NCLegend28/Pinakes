# ExpenseTracker Unit Tests

This directory holds the unit tests added in the A/B audit-pass refactor.
The tests are NOT yet wired into a test target because adding a Unit Testing
Bundle target requires changes to the Xcode project structure that are far
safer to make through Xcode's UI than through hand-edited pbxproj diffs.

## To enable the test target

1. Open `ExpenseTracker.xcodeproj` in Xcode.
2. File → New → Target → **Unit Testing Bundle**.
3. Name it `ExpenseTrackerTests`. Make sure "Target to be Tested" is set to
   `ExpenseTracker`.
4. Xcode will create a new empty `ExpenseTrackerTests/` folder containing
   `ExpenseTrackerTests.swift`. Delete the auto-generated file.
5. Drag `ExpenseTrackerTests.swift` from this folder into the newly created
   `ExpenseTrackerTests` group in Xcode, checking "Copy items if needed"
   and "Add to target: ExpenseTrackerTests".
6. ⌘U to run.

## What's covered

- `OCRProcessorTests` — receipt-text parsing helpers
  (amount/merchant/date/confidence)
- `MerchantCatalogTests` — known-merchant matching and category suggestions
- `ExpenseStoreTests` — SwiftData add/update/delete + monthly totals
- `MileageStoreTests` — round-trip persistence + derived isBusinessTrip
- `IRSMileageRateTests` — rate lookup for each TripPurpose

All `Store` tests use `PersistenceContainer.ephemeral()` to avoid touching
the user's real on-device data.
