# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is an iOS expense tracking application built with SwiftUI that features OCR receipt scanning, expense categorization, and data visualization. The project includes both working Swift files and a technical specification document for PDF tax document integration.

## Development Commands

### Building and Running
- Open `ExpenseTracker/ExpenseTracker.xcodeproj` in Xcode
- Use Cmd+R to build and run on simulator or device
- Project requires iOS 15+ for Vision framework support

### Testing OCR Features
- Use the "Test OCR Camera" button in Settings tab
- Test with receipt images from photo library
- Verify OCR confidence scores and extracted data accuracy

## Architecture Overview

### Core Data Models
The app uses Core Data for persistence with the following entity:
- **ExpenseEntity**: Main expense storage with attributes for amount, merchant, category, date, receipt image data, OCR confidence, and metadata

### Key Classes and Components

#### Data Layer
- `ExpenseManager`: Observable object managing expense CRUD operations and calculations
- `PersistenceController`: Core Data stack management
- `CoreDataManager.swift`: Contains Core Data extensions and helper methods

#### OCR Processing
- `OCRProcessor`: Handles Vision framework integration for receipt text recognition
- Uses regex patterns for extracting amounts, merchants, and dates
- Automatic categorization based on merchant names
- Confidence scoring system for validation

#### UI Components
- `ExpenseDashboardView`: Main dashboard with monthly overview, stats, and category breakdown
- `ReceiptCameraView`: OCR camera interface using VNDocumentCameraViewController
- `ExpenseFormView`: Manual expense entry and editing form
- `ExpenseListView`: Full list view with search and filtering

### File Structure
- `ContentView.swift`: Main app file containing all SwiftUI views and logic
- `CoreDataManager.swift`: Core Data persistence layer
- `ExpenseModel.xcdatamodeld`: Core Data model definition
- Standalone files (`expense-*.swift`): Alternative implementations for reference

## Key Features

### Receipt Scanning (OCR)
- Document camera integration using Vision framework
- Automatic extraction of amount, merchant, date from receipt text
- Confidence scoring (0.0-1.0) based on successful extractions
- Smart categorization based on merchant keywords

### Expense Categories
Predefined categories with icons and colors:
- Meals & Entertainment (orange, fork.knife)
- Transportation (blue, car.fill)
- Office Supplies (green, paperclip)
- Software/Subscriptions (purple, laptopcomputer)
- Travel/Lodging (pink, bed.double.fill)
- Professional Services (indigo, briefcase.fill)
- Marketing (red, megaphone.fill)
- Other (gray, folder.fill)

### Data Visualization
- Monthly spending overview with navigation
- Category breakdown charts
- Weekly and daily average calculations
- Reimbursable expense tracking

## Development Notes

### PDF Tax Document Integration
The app now includes comprehensive PDF document processing with:
- Multi-page PDF import and OCR processing
- Smart expense extraction with confidence scoring
- Auto-processing pipeline with configurable thresholds
- Manual review queue for uncertain extractions
- Full Core Data integration with tax document entities

### Core Data Integration
Enhanced Core Data model includes:
- `TaxDocumentEntity`: PDF storage and metadata
- `ExtractedExpenseEntity`: OCR results with review status
- Extended `ExpenseEntity`: PDF source linking
- Analytics and reporting queries

### OCR Processing Pipeline
1. Image capture via VNDocumentCameraViewController
2. Text recognition using VNRecognizeTextRequest
3. Pattern matching with regex for data extraction
4. Confidence calculation based on successful extractions
5. Automatic expense creation with extracted data

### Testing Strategy
- Use Settings tab for manual testing of OCR functionality
- Verify expense calculations (monthly totals, category breakdowns)
- Test Core Data persistence if enabled
- Validate OCR accuracy with various receipt types

## Future Enhancements
The `alex-tech-doc.md` file contains detailed specifications for PDF tax document integration, including:
- Multi-page PDF processing
- Enhanced OCR with tax-specific patterns
- Review queue for uncertain extractions
- Advanced CoreData schema for document tracking

## Code Style Notes
- Uses SwiftUI with iOS 15+ features
- ObservableObject pattern for data management
- Async/await for OCR processing
- Environment objects for dependency injection
- Proper error handling with Core Data operations