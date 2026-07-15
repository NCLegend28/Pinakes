# Tools Hub

Central dashboard for managing and running all project tools from one interface.

## Architecture

- **Frontend**: React + Vite
- **Backend**: FastAPI (Python)

## Modules

### 1. Book Pack Builder
- Build and manage book packs
- Configure packing parameters
- View packing results

### 2. Options & Predictions
- Run stock predictions with sentiment analysis
- Configure tickers and prediction parameters
- View prediction results and charts

### 3. Sentiment Tracking (Morgans)
- Monitor sentiment from Reddit, SEC filings, Twitter
- Track sentiment history for multiple tickers
- Configure sentiment sources

### 4. Crypto Trading (Redpill)
- View trading bot status
- Monitor positions and performance
- Configure trading strategies

## Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Running

1. Start backend: `cd backend && python main.py`
2. Start frontend: `cd frontend && npm run dev`
3. Open http://localhost:5173
