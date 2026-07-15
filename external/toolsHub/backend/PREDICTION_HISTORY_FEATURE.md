# Prediction History Feature

## Overview
Added comprehensive prediction history tracking and display to the Options & Predictions module.

## Backend Changes

### New API Endpoints

#### GET /api/options/history
Get recent prediction history across all tickers
- **Query Params**: `limit` (default: 20)
- **Returns**: Array of completed predictions with summary data

#### GET /api/options/history/{ticker}
Get historical predictions for a specific ticker
- **Path Param**: `ticker` - Stock ticker symbol
- **Query Params**: `limit` (default: 10)
- **Returns**: Array of predictions with full chart_data and sentiment_data

### Response Format
```json
{
  "ticker": "PATH",
  "count": 3,
  "history": [
    {
      "id": "job-id",
      "date": "2025-10-22T23:16:05.580460",
      "ticker": "PATH",
      "predicted_price": 5.72,
      "current_price": 16.28,
      "investment": 300,
      "expected_profit": 52.50,
      "expected_profit_pct": 17.5,
      "prediction_days": 60,
      "use_sentiment": true,
      "chart_data": [...],
      "sentiment_data": [...]
    }
  ]
}
```

## Frontend Changes

### New Component: PredictionHistory.jsx
A comprehensive history viewer with:
- **Table View**: Shows all predictions in a sortable table
- **Columns**: Date, Ticker, Current Price, Predicted Price, Investment, Expected Profit, Days
- **Detail Modal**: Click "View" to see full prediction details including charts
- **Color Coding**: Green for profitable predictions, red for losses
- **Responsive Design**: Works on desktop and mobile

### Features
- Automatically loads recent predictions
- Can filter by ticker or show all predictions
- **Interactive Charts**: Click "View" to see full price history with prediction
- Shows chart data and sentiment data in detail view
- Format currency and percentages properly
- Real-time updates when new predictions complete
- Visual indicators: Green for profits, Red for losses

### Integration
Added to OptionsModule.jsx below the recent jobs section:
```jsx
<PredictionHistory ticker={null} />
```

Pass a ticker to filter:
```jsx
<PredictionHistory ticker="PATH" />
```

## Data Persistence

All prediction data is automatically persisted in:
- `backend/results/jobs.json` - Stores all job history
- Survives server restarts
- Includes full prediction results with charts and metrics

## Usage

1. **Run a prediction** using the LSTM Analysis button
2. **Wait for completion** - Job will show progress
3. **View in history** - Automatically appears in the Prediction History table
4. **Click "View"** to see detailed analysis with:
   - Summary metrics (current price, predicted price, investment, profit)
   - **Interactive price chart** showing 90 days of historical data
   - Predicted price marked with a red dot
   - Sentiment analysis overlaid as green bars (if available)
   - Hoverable tooltips with detailed price and date information

## Benefits

- Track prediction accuracy over time
- Compare predictions across different tickers
- Review past analysis and charts
- Monitor expected vs actual returns
- Historical performance metrics

## Future Enhancements

- Add actual price tracking to compare with predictions
- Calculate prediction accuracy metrics
- Export history to CSV
- Filter by date range
- Sort by profitability
- Add visualizations for prediction accuracy trends
