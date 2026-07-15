# PDF Tax Document OCR Integration - Technical Documentation

**Project:** Expense Tracker iOS App  
**Feature:** PDF Receipt/Invoice OCR Processing with CoreData Integration  
**Target:** Alex (AI Assistant for Xcode)  
**Date:** September 2025  
**Version:** 1.0  

## Overview

This document outlines the technical implementation for integrating PDF document OCR capabilities into an existing iOS expense tracker application. The system automatically extracts expense information from receipts, invoices, and financial statements using Apple's Vision framework, with full CoreData persistence and user review workflows.

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   PDF Import    │───▶│   OCR Engine     │───▶│  Review Queue   │
│  (UIDocument    │    │ (Vision/VisionKit│    │ (Manual Verify) │
│   Picker)       │    │   Framework)     │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                          │
┌─────────────────┐    ┌──────────────────┐              │
│  CoreData       │◀───│  Integration     │◀─────────────┘
│  Persistence    │    │     Layer        │
│                 │    │                  │
└─────────────────┘    └──────────────────┘
                              │
┌─────────────────┐          │
│   Expense       │◀─────────┘
│   Manager       │
│                 │
└─────────────────┘
```

## Core Components

### 1. PDFTaxReaderView.swift
**Purpose:** Main PDF document management and OCR processing  
**Key Features:**
- Document import via `UIDocumentPickerViewController`
- Multi-page PDF processing with progress tracking
- Vision Framework OCR with confidence scoring
- Smart expense extraction from different document types

**Dependencies:**
```swift
import SwiftUI
import PDFKit
import Vision
import VisionKit
import UniformTypeIdentifiers
```

### 2. ExpensePDFIntegration.swift
**Purpose:** Integration layer between PDF OCR and existing expense system  
**Key Features:**
- Automatic high-confidence expense processing
- Manual review queue management
- CoreData persistence coordination
- Batch approval/rejection workflows

**Dependencies:**
```swift
import SwiftUI
import Combine
// Requires: ExpenseManager, PDFReaderManager, CoreDataManager
```

### 3. CoreDataPDFExtensions.swift
**Purpose:** CoreData extensions for PDF-related data persistence  
**Key Features:**
- Tax document metadata storage
- Extracted expense audit trails
- Expense-to-PDF source linking
- Analytics and reporting queries

## CoreData Schema Updates

### New Entities

#### TaxDocumentEntity
```swift
@objc(TaxDocumentEntity)
public class TaxDocumentEntity: NSManagedObject {
    @NSManaged public var id: UUID
    @NSManaged public var filename: String
    @NSManaged public var documentType: String
    @NSManaged public var fileSize: Int64
    @NSManaged public var pdfData: Data
    @NSManaged public var extractedExpensesCount: Int32
    @NSManaged public var dateAdded: Date
    @NSManaged public var isProcessed: Bool
}
```

#### ExtractedExpenseEntity
```swift
@objc(ExtractedExpenseEntity)
public class ExtractedExpenseEntity: NSManagedObject {
    @NSManaged public var id: UUID
    @NSManaged public var amount: Double
    @NSManaged public var merchant: String
    @NSManaged public var expenseDescription: String
    @NSManaged public var category: String
    @NSManaged public var confidence: Float
    @NSManaged public var rawText: String
    @NSManaged public var sourceDocumentId: UUID
    @NSManaged public var isVerified: Bool
    @NSManaged public var dateExtracted: Date
    @NSManaged public var reviewStatus: String
    @NSManaged public var rejectionReason: String?
    @NSManaged public var dateReviewed: Date?
}
```

#### ExpenseEntity Updates
Add these fields to existing ExpenseEntity:
```swift
@NSManaged public var pdfSourceDocumentId: UUID?
@NSManaged public var extractedExpenseId: UUID?
@NSManaged public var wasEditedFromPDF: Bool
@NSManaged public var pdfImportDate: Date?
```

## Implementation Steps

### Phase 1: CoreData Model Updates
1. Open your `.xcdatamodeld` file in Xcode
2. Add `TaxDocumentEntity` with all specified attributes
3. Add `ExtractedExpenseEntity` with all specified attributes
4. Update `ExpenseEntity` with the new PDF-related optional fields
5. Create and run a Core Data migration if you have existing data

### Phase 2: File Integration
1. Add `PDFTaxReaderView.swift` to your project
2. Add `ExpensePDFIntegration.swift` to your project
3. Add `CoreDataPDFExtensions.swift` to your project
4. Ensure all dependencies are properly imported

### Phase 3: App Integration
Update your main `ContentView` or app coordinator:
```swift
struct ContentView: View {
    @StateObject private var coreDataManager = CoreDataManager()
    @StateObject private var expenseManager: ExpenseManager
    @StateObject private var pdfManager = PDFReaderManager()
    @StateObject private var integration: ExpensePDFIntegration
    
    init() {
        let coreDataManager = CoreDataManager()
        let expenseManager = ExpenseManager(coreDataManager: coreDataManager)
        let pdfManager = PDFReaderManager()
        
        _coreDataManager = StateObject(wrappedValue: coreDataManager)
        _expenseManager = StateObject(wrappedValue: expenseManager)
        _pdfManager = StateObject(wrappedValue: pdfManager)
        _integration = StateObject(wrappedValue: ExpensePDFIntegration(
            expenseManager: expenseManager,
            pdfManager: pdfManager,
            coreDataManager: coreDataManager
        ))
    }
    
    var body: some View {
        TabView {
            DashboardView()
                .tabItem { Label("Dashboard", systemImage: "chart.pie") }
            
            PDFTaxReaderView()
                .environmentObject(integration)
                .tabItem { Label("PDF Scanner", systemImage: "doc.viewfinder") }
        }
        .sheet(isPresented: $integration.showingReviewSheet) {
            if let document = integration.selectedDocument {
                ExpenseReviewSheet(integration: integration, document: document)
            }
        }
    }
}
```

## OCR Processing Pipeline

### 1. Document Import
- User selects PDF via `UIDocumentPickerViewController`
- File is read into memory and basic metadata extracted
- Document type auto-detected based on filename patterns

### 2. Page Processing
```swift
for pageIndex in 0..<pageCount {
    let page = pdfDocument.page(at: pageIndex)
    let image = page.thumbnail(of: pageRect.size, for: .mediaBox)
    
    // OCR processing with Vision Framework
    let extractedExpenses = await extractExpensesFromImage(image, documentType: document.documentType)
    allExtractedExpenses.append(contentsOf: extractedExpenses)
}
```

### 3. Text Pattern Recognition
The system recognizes different patterns based on document type:

**Receipt/Invoice Patterns:**
- Amount: `\$?(\d{1,6}(?:[,.]\d{2}))`
- Date: `(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})`
- Merchant extraction from surrounding context

**Bank Statement Patterns:**
- Transaction lines: `DATE MERCHANT AMOUNT`
- Component parsing with amount detection
- Merchant extraction from middle components

### 4. Confidence Scoring
- High Confidence (≥80%): Auto-approve eligible
- Medium Confidence (60-79%): Requires review
- Low Confidence (<60%): Flagged for manual verification

## User Workflows

### Automatic Processing Flow
1. User imports PDF document
2. OCR extracts potential expenses
3. High-confidence expenses (>80%) auto-added to expense tracker
4. Uncertain expenses queued for review
5. User receives notification if manual review needed

### Manual Review Flow
1. User opens review sheet from notification
2. Reviews each extracted expense with confidence indicators
3. Options for each expense:
   - **Approve:** Add to expense tracker as-is
   - **Edit:** Modify details then add
   - **Reject:** Discard extraction
4. Batch actions available: Approve All / Reject All

### Settings & Configuration
- Confidence threshold adjustment (50%-100%)
- Auto-processing toggle
- Manual review requirement override
- Cleanup policies for old data

## Error Handling & Edge Cases

### OCR Failures
- Graceful handling of unreadable documents
- Confidence scoring prevents bad data injection
- Manual review as fallback for uncertain extractions

### Data Validation
- Amount validation (positive numbers only)
- Date parsing with multiple format support
- Merchant name sanitization

### Performance Considerations
- Large PDF handling with progress indicators
- Memory management for PDF data storage
- Background processing for OCR operations

### Privacy & Security
- PDF data stored locally in CoreData
- No external API calls for OCR processing
- User control over data retention and cleanup

## Testing Strategy

### Unit Tests
- OCR text pattern recognition
- Confidence scoring algorithms
- Expense conversion logic
- CoreData integration methods

### Integration Tests
- End-to-end PDF processing workflow
- CoreData persistence verification
- Cross-component data flow

### User Acceptance Tests
- Receipt scanning accuracy
- Review interface usability
- Batch processing performance
- Data integrity verification

## Performance Metrics

### OCR Processing Targets
- Single page processing: <3 seconds
- Multi-page document: <10 seconds total
- Memory usage: <100MB for typical documents

### User Experience Targets
- App launch time: <2 seconds
- Review sheet load: <1 second
- Batch approval: <2 seconds for 10 items

## Configuration Options

### Integration Settings
```swift
// Auto-processing configuration
autoAddHighConfidence: Bool = true
minimumConfidenceThreshold: Float = 0.8
requireManualReview: Bool = false

// Reimbursable detection keywords
businessKeywords = ["business", "conference", "meeting", "client", "office", "supplies"]

// High-value threshold for mandatory review
highValueThreshold: Double = 500.0
```

### Data Retention
```swift
// Cleanup old rejected extractions
cleanupOldPDFData(olderThanDays: 30)

// Migration support for existing data
migrateExistingExpensesToIncludePDFFields()
```

## Troubleshooting Guide

### Common Issues
1. **OCR returns no results**
   - Check document image quality
   - Verify PDF is not password protected
   - Try re-processing with different confidence threshold

2. **App crashes on PDF import**
   - Check file size limits
   - Verify PDF format compatibility
   - Monitor memory usage

3. **CoreData migration fails**
   - Backup existing data
   - Run migration helper methods
   - Check entity relationship configurations

### Debug Tools
- OCR confidence logging
- Processing time measurement  
- CoreData query performance monitoring
- Memory usage tracking

## Future Enhancements

### Planned Features
- Machine learning model for better merchant/category recognition
- Cloud sync for PDF documents
- Export functionality for processed data
- Advanced analytics dashboard

### Performance Optimizations
- Background OCR processing
- Incremental PDF processing
- Caching for repeated document types
- Optimized CoreData queries

---

## Quick Start Checklist

For Alex (AI Assistant):

- [ ] Review existing `ExpenseManager` and `CoreDataManager` implementations
- [ ] Update CoreData model with new entities as specified
- [ ] Integrate the three main Swift files into the project
- [ ] Update app initialization to include PDF integration
- [ ] Test basic PDF import and OCR functionality
- [ ] Verify CoreData persistence is working correctly
- [ ] Test user review workflow
- [ ] Run performance verification on sample documents

**Expected Integration Time:** 2-4 hours for core implementation, additional time for testing and refinement.

**Dependencies:** iOS 15+, Xcode 13+, existing CoreData setup, Vision/VisionKit frameworks available.