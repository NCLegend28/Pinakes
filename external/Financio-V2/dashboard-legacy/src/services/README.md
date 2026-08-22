# Stock Market Data Service

A TypeScript service for fetching real-time stock market data with multiple API providers, intelligent caching, and market status tracking.

## Features

- 🚀 **Real-time Stock Data** - Live price updates from multiple APIs
- 🔄 **Smart Caching** - 30-second cache to minimize API calls
- 🏪 **Market Status** - Real-time market open/closed detection
- 🔌 **Multiple API Support** - Alpha Vantage, Financial Modeling Prep, and mock data fallbacks
- 📊 **Comprehensive Data** - Price, volume, market cap, change percentages
- ⏰ **Auto-refresh** - Different refresh rates for market hours vs. after hours
- 🛡️ **Error Handling** - Graceful fallbacks and retry mechanisms
- 💾 **TypeScript Support** - Fully typed interfaces

## Quick Start

```typescript
import { stockMarketService } from '@/services/stockMarketService';

// Get single stock data
const appleStock = await stockMarketService.getStockData('AAPL');

// Get multiple stocks
const stocks = await stockMarketService.getMultipleStocksData(['AAPL', 'GOOGL', 'MSFT']);

// Check market status
const marketStatus = stockMarketService.getMarketStatus();
```

## Installation

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Set Up Environment Variables**
   ```bash
   cp .env.example .env
   ```

3. **Configure API Keys** (optional for demo mode)
   ```env
   VITE_ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
   VITE_FMP_API_KEY=your_fmp_key
   ```

## API Providers

### 1. Alpha Vantage (Primary)
- **Free Tier**: 25 requests/day, 5 requests/minute
- **Get API Key**: https://www.alphavantage.co/support/#api-key
- **Pros**: Reliable, comprehensive data
- **Cons**: Limited free tier

### 2. Financial Modeling Prep (Fallback)
- **Free Tier**: 250 requests/day
- **Get API Key**: https://financialmodelingprep.com/developer/docs
- **Pros**: Higher request limits
- **Cons**: Less reliable for some symbols

### 3. Mock Data (Development)
- **Always Available**: No API key required
- **Features**: Realistic price fluctuations, all stock symbols
- **Use Case**: Development, testing, API limit exceeded

## Data Structure

```typescript
interface StockData {
  symbol: string;          // Stock symbol (e.g., "AAPL")
  name: string;           // Company name (e.g., "Apple Inc.")
  price: number;          // Current price
  change: number;         // Price change ($)
  changePercent: number;  // Price change (%)
  volume: number;         // Trading volume
  marketCap?: number;     // Market capitalization
  lastUpdated: Date;      // Last update timestamp
}

interface MarketStatus {
  isOpen: boolean;        // Is market currently open
  status: string;         // Human readable status
  nextOpen?: string;      // When market opens next
}
```

## Usage Examples

### Basic Stock Data Fetching

```typescript
import { stockMarketService } from '@/services/stockMarketService';

// Single stock
const stock = await stockMarketService.getStockData('AAPL');
console.log(`${stock.symbol}: $${stock.price} (${stock.changePercent}%)`);

// Multiple stocks
const portfolio = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'NVDA'];
const stocks = await stockMarketService.getMultipleStocksData(portfolio);
stocks.forEach(stock => {
  console.log(`${stock.symbol}: $${stock.price} (${stock.changePercent}%)`);
});
```

### Market Status Monitoring

```typescript
const marketStatus = stockMarketService.getMarketStatus();

if (marketStatus.isOpen) {
  console.log('🟢 Market is open - Live trading active');
} else {
  console.log(`🔴 ${marketStatus.status}`);
  if (marketStatus.nextOpen) {
    console.log(`Next open: ${marketStatus.nextOpen}`);
  }
}
```

### React Component Integration

```tsx
import { useState, useEffect } from 'react';
import { stockMarketService, StockData } from '@/services/stockMarketService';

export const StockTicker = ({ symbol }: { symbol: string }) => {
  const [stock, setStock] = useState<StockData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStock = async () => {
      try {
        const data = await stockMarketService.getStockData(symbol);
        setStock(data);
      } finally {
        setLoading(false);
      }
    };

    fetchStock();
    
    // Refresh every 30 seconds during market hours
    const interval = setInterval(() => {
      const status = stockMarketService.getMarketStatus();
      if (status.isOpen) {
        fetchStock();
      }
    }, 30000);

    return () => clearInterval(interval);
  }, [symbol]);

  if (loading) return <div>Loading...</div>;
  if (!stock) return <div>Error loading stock data</div>;

  return (
    <div className={stock.change >= 0 ? 'text-green-500' : 'text-red-500'}>
      <span className="font-bold">{stock.symbol}</span>
      <span>${stock.price}</span>
      <span>({stock.changePercent}%)</span>
    </div>
  );
};
```

## Market Hours

The service automatically detects US market hours:

- **Market Open**: Monday-Friday, 9:30 AM - 4:00 PM EST
- **Pre-Market**: Before 9:30 AM EST
- **After Hours**: After 4:00 PM EST
- **Weekends**: Market closed

### Market Status Values

| Status | Description |
|--------|-------------|
| `"Market Open"` | Trading hours, live data updates |
| `"Pre-Market"` | Before market open |
| `"After Hours"` | After market close |
| `"Market Closed - Weekend"` | Weekend closure |

## Caching Strategy

- **Cache Duration**: 30 seconds
- **Cache Key**: Stock symbol
- **Benefits**: 
  - Reduces API calls
  - Improves performance
  - Avoids rate limits
  - Consistent data across components

## Error Handling

The service implements graceful error handling:

1. **API Failure**: Falls back to secondary API
2. **Rate Limits**: Uses cached data or mock data
3. **Network Issues**: Returns mock data with realistic values
4. **Invalid Symbols**: Generates placeholder data

## Performance Optimization

### Automatic Refresh Rates

- **Market Open**: Every 30 seconds
- **Market Closed**: Every 5 minutes
- **Manual Refresh**: Available via UI button

### Batch Requests

```typescript
// Efficient - Single batch request
const stocks = await stockMarketService.getMultipleStocksData(['AAPL', 'GOOGL', 'MSFT']);

// Inefficient - Multiple individual requests
const stocks = await Promise.all([
  stockMarketService.getStockData('AAPL'),
  stockMarketService.getStockData('GOOGL'),
  stockMarketService.getStockData('MSFT')
]);
```

## API Rate Limits

### Alpha Vantage
- **Free**: 25 requests/day, 5/minute
- **Paid**: Up to 1200 requests/minute
- **Recommendation**: Use for production with paid plan

### Financial Modeling Prep
- **Free**: 250 requests/day
- **Paid**: Up to 10,000 requests/day
- **Recommendation**: Good for development and small apps

## Development Mode

When no API keys are provided, the service automatically uses mock data:

```typescript
// Mock data features:
// ✅ Realistic price fluctuations
// ✅ Time-based variations
// ✅ All major stock symbols
// ✅ Proper market status simulation
// ✅ Volume and market cap data
```

## Troubleshooting

### Common Issues

**1. API Rate Limit Exceeded**
```
Error: API call frequency is too high
Solution: Service automatically falls back to mock data
```

**2. Invalid API Key**
```
Error: Invalid API key
Solution: Check .env file and verify API key
```

**3. Network Connection Issues**
```
Error: Failed to fetch
Solution: Service falls back to cached or mock data
```

### Debug Mode

Enable debug logging:

```typescript
// Add to your component
useEffect(() => {
  console.log('Market Status:', stockMarketService.getMarketStatus());
}, []);
```

## Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/new-api-provider`
3. **Add new API provider** in `stockMarketService.ts`
4. **Update this README** with new provider details
5. **Submit pull request**

### Adding New API Providers

```typescript
// Example: Adding Yahoo Finance API
async getStockDataYahoo(symbol: string): Promise<StockData> {
  try {
    const API_KEY = import.meta.env.VITE_YAHOO_API_KEY;
    const url = `https://yahoo-finance-api.com/quote/${symbol}`;
    
    const response = await fetch(url, {
      headers: { 'X-API-Key': API_KEY }
    });
    
    const data = await response.json();
    
    return {
      symbol: data.symbol,
      name: data.longName,
      price: data.regularMarketPrice,
      change: data.regularMarketChange,
      changePercent: data.regularMarketChangePercent,
      volume: data.regularMarketVolume,
      lastUpdated: new Date()
    };
  } catch (error) {
    return this.getMockStockData(symbol);
  }
}
```

## License

MIT License - See [LICENSE](../LICENSE) for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/NCLegend28/Financio-V2/issues)
- **Documentation**: This README
- **Examples**: See `src/components/MarketData.tsx`

---

## Related Files

- **Service Implementation**: `/src/services/stockMarketService.ts`
- **React Component**: `/src/components/MarketData.tsx`
- **Environment Config**: `/.env.example`
- **Type Definitions**: Included in service file
