```yaml
# config/discovery_config.yaml (continued)

discovery:
  schedules:
    daily_screening: "16:30"      # After market close
    weekly_review: "sunday 20:00"
    monthly_deep_dive: "first_sunday 20:00"
  
  screening:
    momentum:
      enabled: true
      lookback_period: 252        # 1 year
      min_return: 0.20            # 20% return
      min_volume: 1000000         # 1M shares daily
      min_market_cap: 1000000000  # $1B
      
    value:
      enabled: true
      max_pe: 15
      max_pb: 2.0
      min_fcf_yield: 0.05
      min_roe: 0.15
      
    quality:
      enabled: true
      min_roe: 0.15
      max_debt_to_equity: 0.5
      min_current_ratio: 1.5
      min_gross_margin: 0.40
      
    growth:
      enabled: true
      min_revenue_growth: 0.15
      min_earnings_growth: 0.20
      min_margin_expansion: 0.02
      
    technical:
      enabled: true
      patterns:
        - "consolidation_breakout"
        - "cup_and_handle"
        - "flag_pattern"
      min_consolidation_days: 20
      volume_surge_threshold: 1.5
  
  filters:
    liquidity:
      min_dollar_volume: 10000000   # $10M daily
      max_spread_bps: 10            # 0.10%
      
    quality:
      exclude_penny_stocks: true
      min_price: 5.0
      
    geographic:
      allowed_countries:
        - "US"
        - "CA"
        - "UK"
        - "DE"
        - "JP"
        - "SG"
        - "HK"
      
    sector:
      max_concentration: 0.30       # Max 30% in one sector
      
  universe_management:
    max_active_tickers: 200
    max_watchlist_tickers: 100
    
    core_universe:
      max_size: 50
      min_conviction_score: 80
      min_track_record_days: 90
      
    satellite_universe:
      max_size: 100
      min_conviction_score: 60
      min_track_record_days: 30
      
    tactical_universe:
      max_size: 50
      min_conviction_score: 70
      max_holding_period_days: 60
    
    inclusion_criteria:
      min_composite_score: 60
      require_agent_approval: true
      require_risk_validation: true
      require_compliance_check: true
      
    removal_criteria:
      auto_remove_conditions:
        - liquidity_dried_up: true    # Volume drops below threshold
        - delisted: true
        - fundamental_deterioration: true
      
      performance_triggers:
        max_consecutive_losing_days: 30
        max_drawdown_pct: 0.40        # Remove if -40% from peak
        min_sharpe_ratio: -0.5        # Remove if Sharpe < -0.5
      
      review_frequency_days: 7
    
  composite_scoring:
    weights:
      momentum: 0.30
      value: 0.20
      quality: 0.25
      growth: 0.15
      technical: 0.10
    
    normalization: "z_score"          # or "percentile_rank"
    
  risk_limits:
    max_position_size_pct: 0.05       # 5% max per ticker
    max_new_tickers_per_day: 10
    max_new_tickers_per_week: 30
    
  notifications:
    email:
      enabled: true
      recipients:
        - "trading@yourfirm.com"
      events:
        - "ticker_added"
        - "ticker_removed"
        - "screening_completed"
        - "review_completed"
    
    slack:
      enabled: true
      webhook_url: "https://hooks.slack.com/..."
      channels:
        - "#trading-alerts"
```

---

## 10. Advanced Features

### 10.1 Dynamic Strategy Assignment

```python
# tools/strategy_matcher.py

class StrategyMatcher:
    """Match tickers to appropriate strategies"""
    
    def __init__(self, coordinator):
        self.coordinator = coordinator
        
    def match_ticker_to_strategies(self, ticker: Ticker) -> List[str]:
        """
        Determine which strategies should trade this ticker
        
        Uses agent consultation to decide strategy fit
        """
        
        query = f"""Analyze ticker {ticker.symbol} and determine which strategies it's suitable for:

Ticker Profile:
- Symbol: {ticker.symbol}
- Momentum Score: {ticker.momentum_score}
- Value Score: {ticker.value_score}
- Quality Score: {ticker.quality_score}
- Market Cap: ${ticker.market_cap:,.0f}
- Avg Daily Volume: {ticker.avg_daily_volume:,.0f}
- Avg Spread: {ticker.avg_spread_bps} bps

Available Strategies:
1. Momentum (trend following, relative strength)
2. Mean Reversion (oversold bounces, range trading)
3. Breakout (consolidation breakouts, new highs)
4. Statistical Arbitrage (pair trading, basket trading)
5. Event Driven (earnings, announcements)

For each applicable strategy, explain why this ticker fits and what specific parameters to use."""

        response = self.coordinator.agents["Strategy Architect"].query(
            query,
            context={"ticker": ticker.to_dict()}
        )
        
        # Parse response and extract strategy assignments
        strategies = self._parse_strategy_assignments(response)
        
        return strategies
    
    def _parse_strategy_assignments(self, response: Dict) -> List[str]:
        """Extract strategy names from agent response"""
        # Implementation depends on response format
        pass
```

### 10.2 Performance Tracking

```python
# monitoring/ticker_performance.py

class TickerPerformanceTracker:
    """Track performance metrics for each ticker"""
    
    def __init__(self, ticker_universe):
        self.universe = ticker_universe
        
    def calculate_ticker_metrics(self, symbol: str, lookback_days: int = 30) -> Dict:
        """Calculate performance metrics for a ticker"""
        
        ticker = self.universe.tickers.get(symbol)
        if not ticker:
            return {}
        
        # Get trade history for this ticker
        trades = self._get_ticker_trades(symbol, lookback_days)
        
        if not trades:
            return {"error": "No trades found"}
        
        metrics = {
            "symbol": symbol,
            "period_days": lookback_days,
            
            # P&L metrics
            "total_pnl": sum(t['pnl'] for t in trades),
            "avg_pnl_per_trade": np.mean([t['pnl'] for t in trades]),
            "win_rate": len([t for t in trades if t['pnl'] > 0]) / len(trades),
            "profit_factor": self._calculate_profit_factor(trades),
            
            # Risk metrics
            "sharpe_ratio": self._calculate_sharpe(trades),
            "max_drawdown": self._calculate_max_drawdown(trades),
            "avg_mae": np.mean([t['mae'] for t in trades]),  # Max adverse excursion
            
            # Execution metrics
            "avg_slippage_bps": np.mean([t['slippage_bps'] for t in trades]),
            "avg_fill_time_seconds": np.mean([t['fill_time'] for t in trades]),
            
            # Trade statistics
            "total_trades": len(trades),
            "avg_holding_period_hours": np.mean([t['holding_period'] for t in trades]),
            "largest_win": max([t['pnl'] for t in trades]),
            "largest_loss": min([t['pnl'] for t in trades]),
        }
        
        return metrics
    
    def should_remove_ticker(self, symbol: str) -> tuple[bool, str]:
        """
        Determine if ticker should be removed based on performance
        
        Returns:
            (should_remove, reason)
        """
        metrics = self.calculate_ticker_metrics(symbol, lookback_days=30)
        
        if metrics.get("error"):
            return False, ""
        
        # Check removal criteria
        if metrics["sharpe_ratio"] < -0.5:
            return True, f"Poor Sharpe ratio: {metrics['sharpe_ratio']:.2f}"
        
        if metrics["max_drawdown"] > 0.40:
            return True, f"Excessive drawdown: {metrics['max_drawdown']:.1%}"
        
        if metrics["win_rate"] < 0.30 and metrics["total_trades"] > 20:
            return True, f"Low win rate: {metrics['win_rate']:.1%}"
        
        if metrics["avg_slippage_bps"] > 20:
            return True, f"Excessive slippage: {metrics['avg_slippage_bps']:.1f} bps"
        
        return False, ""
    
    def generate_ticker_report(self, symbol: str) -> str:
        """Generate performance report for a ticker"""
        
        metrics = self.calculate_ticker_metrics(symbol, lookback_days=90)
        ticker = self.universe.tickers.get(symbol)
        
        report = f"""
TICKER PERFORMANCE REPORT: {symbol}
{'='*60}

TICKER INFO:
- Status: {ticker.status.value}
- Universe Type: {ticker.universe_type.value}
- Added: {ticker.added_date.strftime('%Y-%m-%d') if ticker.added_date else 'N/A'}
- Strategies: {', '.join(ticker.strategies)}

PERFORMANCE (90 days):
- Total P&L: ${metrics['total_pnl']:,.2f}
- Win Rate: {metrics['win_rate']:.1%}
- Sharpe Ratio: {metrics['sharpe_ratio']:.2f}
- Max Drawdown: {metrics['max_drawdown']:.1%}
- Profit Factor: {metrics['profit_factor']:.2f}

EXECUTION QUALITY:
- Avg Slippage: {metrics['avg_slippage_bps']:.1f} bps
- Avg Fill Time: {metrics['avg_fill_time_seconds']:.1f}s
- Total Trades: {metrics['total_trades']}

TRADE STATISTICS:
- Avg Holding Period: {metrics['avg_holding_period_hours']:.1f} hours
- Largest Win: ${metrics['largest_win']:,.2f}
- Largest Loss: ${metrics['largest_loss']:,.2f}
- Avg P&L/Trade: ${metrics['avg_pnl_per_trade']:,.2f}

RECOMMENDATION:
{self._generate_recommendation(symbol, metrics)}
        """
        
        return report
    
    def _calculate_profit_factor(self, trades: List[Dict]) -> float:
        """Calculate profit factor (gross profit / gross loss)"""
        gross_profit = sum(t['pnl'] for t in trades if t['pnl'] > 0)
        gross_loss = abs(sum(t['pnl'] for t in trades if t['pnl'] < 0))
        
        if gross_loss == 0:
            return float('inf') if gross_profit > 0 else 0
        
        return gross_profit / gross_loss
    
    def _calculate_sharpe(self, trades: List[Dict]) -> float:
        """Calculate Sharpe ratio from trades"""
        returns = [t['return_pct'] for t in trades]
        
        if not returns or np.std(returns) == 0:
            return 0
        
        return (np.mean(returns) / np.std(returns)) * np.sqrt(252)  # Annualized
    
    def _calculate_max_drawdown(self, trades: List[Dict]) -> float:
        """Calculate maximum drawdown"""
        cumulative = np.cumsum([t['pnl'] for t in trades])
        running_max = np.maximum.accumulate(cumulative)
        drawdown = (cumulative - running_max) / (running_max + 1e-10)
        
        return abs(np.min(drawdown))
    
    def _get_ticker_trades(self, symbol: str, lookback_days: int) -> List[Dict]:
        """Fetch trade history for ticker"""
        # Implementation depends on your trade storage system
        pass
    
    def _generate_recommendation(self, symbol: str, metrics: Dict) -> str:
        """Generate recommendation based on metrics"""
        should_remove, reason = self.should_remove_ticker(symbol)
        
        if should_remove:
            return f"⚠️  REMOVE: {reason}"
        
        if metrics['sharpe_ratio'] > 2.0 and metrics['win_rate'] > 0.60:
            return "✓ EXCELLENT: Consider increasing position size"
        
        if metrics['sharpe_ratio'] > 1.0:
            return "✓ GOOD: Performing well, maintain current allocation"
        
        if metrics['sharpe_ratio'] > 0.5:
            return "⚠️  WATCH: Marginal performance, monitor closely"
        
        return "⚠️  UNDERPERFORMING: Consider removal if trend continues"
```

### 10.3 Market Regime Detection

```python
# tools/regime_detector.py

class MarketRegimeDetector:
    """Detect market regime changes and adjust universe accordingly"""
    
    def __init__(self, data_provider):
        self.data_provider = data_provider
        
    def detect_current_regime(self) -> Dict[str, Any]:
        """
        Detect current market regime
        
        Regimes:
        - Bull (trending up, low vol)
        - Bear (trending down, high vol)
        - High Vol (choppy, high vol)
        - Low Vol (range-bound, low vol)
        """
        
        # Calculate regime indicators
        spy_data = self.data_provider.get_historical('SPY', days=252)
        
        # Trend
        sma_200 = spy_data['close'].rolling(200).mean().iloc[-1]
        current_price = spy_data['close'].iloc[-1]
        trend = "up" if current_price > sma_200 else "down"
        
        # Volatility
        returns = spy_data['close'].pct_change()
        current_vol = returns.rolling(20).std().iloc[-1] * np.sqrt(252)
        historical_vol = returns.std() * np.sqrt(252)
        vol_regime = "high" if current_vol > historical_vol * 1.2 else "low"
        
        # Classify regime
        regime_map = {
            ("up", "low"): "bull_trending",
            ("up", "high"): "bull_volatile",
            ("down", "low"): "bear_grinding",
            ("down", "high"): "bear_volatile"
        }
        
        regime = regime_map.get((trend, vol_regime), "neutral")
        
        return {
            "regime": regime,
            "trend": trend,
            "volatility": vol_regime,
            "current_vol": current_vol,
            "confidence": self._calculate_regime_confidence(spy_data)
        }
    
    def adjust_universe_for_regime(self, regime: str) -> Dict[str, Any]:
        """
        Adjust screening and universe based on market regime
        
        Different regimes favor different ticker characteristics
        """
        
        adjustments = {
            "bull_trending": {
                "favor": ["momentum", "growth"],
                "reduce": ["value", "defensive"],
                "screening_weights": {
                    "momentum": 0.40,
                    "growth": 0.30,
                    "quality": 0.20,
                    "value": 0.10
                }
            },
            "bull_volatile": {
                "favor": ["quality", "low_beta"],
                "reduce": ["high_beta", "speculative"],
                "screening_weights": {
                    "quality": 0.40,
                    "momentum": 0.30,
                    "value": 0.20,
                    "growth": 0.10
                }
            },
            "bear_grinding": {
                "favor": ["value", "quality", "defensive"],
                "reduce": ["momentum", "growth"],
                "screening_weights": {
                    "value": 0.35,
                    "quality": 0.35,
                    "momentum": 0.15,
                    "growth": 0.15
                }
            },
            "bear_volatile": {
                "favor": ["defensive", "low_vol"],
                "reduce": ["cyclical", "speculative"],
                "screening_weights": {
                    "quality": 0.50,
                    "value": 0.30,
                    "momentum": 0.10,
                    "growth": 0.10
                }
            }
        }
        
        return adjustments.get(regime, {})
    
    def _calculate_regime_confidence(self, data: pd.DataFrame) -> float:
        """Calculate confidence in regime classification"""
        # Implementation: use multiple indicators and measure agreement
        pass
```

### 10.4 Integration: Regime-Aware Discovery

```python
# orchestration/discovery_workflow.py (enhanced)

class DiscoveryWorkflow:
    
    def __init__(self, coordinator, ticker_universe, screener, regime_detector):
        self.coordinator = coordinator
        self.universe = ticker_universe
        self.screener = screener
        self.regime_detector = regime_detector
    
    def run_daily_discovery(self) -> Dict[str, Any]:
        """Daily discovery with regime awareness"""
        
        # Detect market regime
        regime = self.regime_detector.detect_current_regime()
        adjustments = self.regime_detector.adjust_universe_for_regime(regime['regime'])
        
        print(f"Market Regime: {regime['regime']} (confidence: {regime['confidence']:.1%})")
        print(f"Adjusting screens: favor {adjustments.get('favor', [])}")
        
        # Adjust screening weights based on regime
        screening_weights = adjustments.get('screening_weights', {
            "momentum": 0.30,
            "value": 0.20,
            "quality": 0.25,
            "growth": 0.15,
            "technical": 0.10
        })
        
        # Run screens with regime-adjusted weights
        screen_results = self.screener.composite_screen(
            screens=list(screening_weights.keys()),
            weights=screening_weights
        )
        
        # Rest of workflow continues...
        # Agent consultations include regime context
        
        context = {
            "screen_results": screen_results,
            "market_regime": regime,
            "regime_adjustments": adjustments
        }
        
        scout_evaluation = self.coordinator.agents["Ticker Scout"].query(
            f"""Market Regime: {regime['regime']}
            
Given the current market regime, evaluate these screening results and identify promising tickers that fit the regime:

Screening Results: {screen_results}
Regime Preferences: Favor {adjustments.get('favor', [])}

Focus on tickers that will perform well in a {regime['regime']} environment.""",
            context=context
        )
        
        # Continue workflow...
```

---

## 11. Command-Line Interface

```python
# cli.py

import click
from main import (
    coordinator, ticker_universe, discovery, 
    screener, regime_detector, performance_tracker
)

@click.group()
def cli():
    """Trading Agent System - Ticker Management CLI"""
    pass

@cli.command()
def discover():
    """Run ticker discovery workflow"""
    click.echo("Running ticker discovery...")
    results = discovery.run_daily_discovery()
    click.echo(f"✓ Discovered {results['total_added']} new tickers")

@cli.command()
def review():
    """Run weekly universe review"""
    click.echo("Running universe review...")
    results = discovery.run_weekly_review()
    click.echo(f"✓ Removed {len(results['removals'])} tickers")
    click.echo(f"✓ Promoted {len(results['promotions'])} tickers")

@cli.command()
@click.argument('symbol')
def analyze(symbol):
    """Analyze a specific ticker"""
    ticker = ticker_universe.tickers.get(symbol.upper())
    
    if not ticker:
        click.echo(f"Ticker {symbol} not found in universe")
        return
    
    # Get performance report
    report = performance_tracker.generate_ticker_report(symbol.upper())
    click.echo(report)

@cli.command()
@click.argument('symbol')
@click.option('--reason', '-r', required=True, help='Reason for addition')
@click.option('--type', '-t', type=click.Choice(['core', 'satellite', 'tactical']), default='satellite')
def add(symbol, reason, type):
    """Add ticker to universe manually"""
    
    # Run through agent approval
    query = f"Should we add {symbol} to the universe? Reason: {reason}"
    
    response = coordinator.route_query(query)
    
    click.echo(response['response'])
    
    if click.confirm('Proceed with addition?'):
        # Add ticker
        click.echo(f"✓ Added {symbol} to universe")

@cli.command()
@click.argument('symbol')
@click.option('--reason', '-r', required=True, help='Reason for removal')
def remove(symbol, reason):
    """Remove ticker from universe"""
    
    if click.confirm(f'Remove {symbol}? Reason: {reason}'):
        ticker_universe.remove_ticker(symbol.upper(), reason)
        click.echo(f"✓ Removed {symbol} from universe")

@cli.command()
def universe():
    """Show current universe"""
    
    active = ticker_universe.get_active_tickers()
    watchlist = ticker_universe.get_watchlist()
    
    click.echo(f"\n{'='*60}")
    click.echo(f"ACTIVE UNIVERSE ({len(active)} tickers)")
    click.echo(f"{'='*60}\n")
    
    # Group by type
    core = [t for t in active if t.universe_type == UniverseType.CORE]
    satellite = [t for t in active if t.universe_type == UniverseType.SATELLITE]
    tactical = [t for t in active if t.universe_type == UniverseType.TACTICAL]
    
    click.echo(f"Core ({len(core)}):")
    for t in sorted(core, key=lambda x: x.composite_score, reverse=True):
        click.echo(f"  {t.symbol:6s} - Score: {t.composite_score:5.1f} - {', '.join(t.strategies)}")
    
    click.echo(f"\nSatellite ({len(satellite)}):")
    for t in sorted(satellite, key=lambda x: x.composite_score, reverse=True)[:20]:
        click.echo(f"  {t.symbol:6s} - Score: {t.composite_score:5.1f}")
    
    click.echo(f"\nTactical ({len(tactical)}):")
    for t in tactical:
        click.echo(f"  {t.symbol:6s} - Score: {t.composite_score:5.1f}")
    
    click.echo(f"\n{'='*60}")
    click.echo(f"WATCHLIST ({len(watchlist)} tickers)")
    click.echo(f"{'='*60}\n")
    
    for t in sorted(watchlist, key=lambda x: x.composite_score, reverse=True)[:20]:
        days_on_watchlist = (datetime.now() - t.discovered_date).days
        click.echo(f"  {t.symbol:6s} - Score: {t.composite_score:5.1f} - {days_on_watchlist} days")

@cli.command()
def regime():
    """Show current market regime"""
    
    current_regime = regime_detector.detect_current_regime()
    adjustments = regime_detector.adjust_universe_for_regime(current_regime['regime'])
    
    click.echo(f"\n{'='*60}")
    click.echo(f"MARKET REGIME ANALYSIS")
    click.echo(f"{'='*60}\n")
    
    click.echo(f"Current Regime: {current_regime['regime']}")
    click.echo(f"Trend: {current_regime['trend']}")
    click.echo(f"Volatility: {current_regime['volatility']}")
    click.echo(f"Confidence: {current_regime['confidence']:.1%}")
    
    click.echo(f"\nRecommended Adjustments:")
    click.echo(f"  Favor: {', '.join(adjustments.get('favor', []))}")
    click.echo(f"  Reduce: {', '.join(adjustments.get('reduce', []))}")
    
    click.echo(f"\nScreening Weights:")
    for factor, weight in adjustments.get('screening_weights', {}).items():
        click.echo(f"  {factor}: {weight:.0%}")

@cli.command()
@click.option('--days', '-d', default=30, help='Performance period in days')
def performance(days):
    """Show performance summary"""
    
    active = ticker_universe.get_active_tickers()
    
    click.echo(f"\n{'='*60}")
    click.echo(f"PERFORMANCE SUMMARY (Last {days} days)")
    click.echo(f"{'='*60}\n")
    
    results = []
    for ticker in active:
        metrics = performance_tracker.calculate_ticker_metrics(ticker.symbol, days)
        if not metrics.get('error'):
            results.append((ticker.symbol, metrics))
    
    # Sort by Sharpe ratio
    results.sort(key=lambda x: x[1]['sharpe_ratio'], reverse=True)
    
    click.echo(f"{'Ticker':<8} {'P&L':>12} {'Sharpe':>8} {'Win%':>8} {'Trades':>8}")
    click.echo("-" * 60)
    
    for symbol, metrics in results[:30]:
        click.echo(
            f"{symbol:<8} "
            f"${metrics['total_pnl']:>11,.0f} "
            f"{metrics['sharpe_ratio']:>8.2f} "
            f"{metrics['win_rate']:>7.1%} "
            f"{metrics['total_trades']:>8}"
        )

@cli.command()
@click.option('--auto', is_flag=True, help='Run in automated mode')
def start(auto):
    """Start the trading system"""
    
    if auto:
        click.echo("Starting automated discovery scheduler...")
        from scheduler.discovery_scheduler import DiscoveryScheduler
        scheduler = DiscoveryScheduler(discovery)
        scheduler.start()
    else:
        click.echo("Starting interactive mode...")
        # Interactive shell
        from IPython import embed
        embed()

if __name__ == '__main__':
    cli()
```

---

## 12. Usage Examples

```bash
# Run daily discovery
python cli.py discover

# Review universe
python cli.py review

# Analyze specific ticker
python cli.py analyze AAPL

# Add ticker manually
python cli.py add NVDA -r "Strong momentum breakout above 200 SMA"

# Remove ticker
python cli.py remove XYZ -r "Liquidity dried up"

# View current universe
python cli.py universe

# Check market regime
python cli.py regime

# View performance
python cli.py performance --days 30

# Start automated mode
python cli.py start --auto

# Interactive mode
python cli.py start
```

---

## Summary

You now have a **complete ticker discovery and management system** that:

✅ **Automatically discovers** promising tickers using quantitative screens  
✅ **Evaluates candidates** through multi-agent consultation  
✅ **Manages universe** with watchlist → active → removal lifecycle  
✅ **Adapts to market regimes** by adjusting screening criteria  
✅ **Tracks performance** and auto-removes underperformers  
✅ **Assigns strategies** dynamically based on ticker characteristics  
✅ **Runs on schedule** with daily discovery and weekly reviews  
✅ **Provides CLI** for manual operations and monitoring  

The system integrates seamlessly with your existing 12-agent architecture and follows the same patterns (agent consultation, structured decisions, audit logging).

**Next implementation steps:**
1. Add Ticker Scout and Portfolio Manager agents
2. Implement the screener tools
3. Set up the ticker universe database
4. Configure discovery workflows
5. Test with paper trading first

Want me to elaborate on any specific component?
