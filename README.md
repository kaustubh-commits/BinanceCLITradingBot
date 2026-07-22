<div align="center">
  <h1>Binance Futures Trading Bot</h1>
  <p>
    <strong>A command-line trading bot for Binance USDT-M Futures</strong>
  </p>
  <p>
    <a href="#features">Features</a> •
    <a href="#architecture">Architecture</a> •
    <a href="#installation">Installation</a> •
    <a href="#configuration">Configuration</a> •
    <a href="#usage">Usage</a> •
    <a href="#testing-status">Testing</a> •
    <a href="#security">Security</a>
  </p>
  <p>
    <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python 3.8+">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License">
    <img src="https://img.shields.io/badge/status-release--candidate-yellow.svg" alt="Release Candidate">
  </p>
</div>

---

## Overview

**Binance Futures Trading Bot** is a CLI-driven trading tool for Binance USDT-M Futures. It supports market orders, limit orders, OCO (take-profit + stop-loss) pairs, TWAP execution, and grid trading strategies.

This project was built to demonstrate clean Python architecture for automated trading — modular design, input validation, structured logging, testnet support, and comprehensive error handling.

It was originally developed and tested against the Binance Futures Testnet. The current release focuses on repository quality, documentation, architecture, validation, and maintainability.

---

## Features

| Category | Feature | Description |
|----------|---------|-------------|
| **Core** | Market Orders | Execute buy/sell orders at current market price |
| | Limit Orders | Place orders at a specified price with configurable time-in-force (GTC, IOC, FOK) |
| **Advanced** | OCO Orders | Take-profit limit order + stop-market order pair for position management |
| | TWAP | Split a large order into smaller chunks executed at regular intervals |
| | Grid Trading | Create multiple buy and sell orders at evenly spaced price levels |
| **Tooling** | Input Validation | Symbol format, quantity, price, side, and time-in-force validation |
| | Structured Logging | Timestamped logs with function names, line numbers, and severity levels |
| | API Diagnostics | Built-in script to troubleshoot Binance API connectivity and authentication |
| | Testnet Support | Default testnet configuration prevents accidental live trading |

---

## Architecture

```
User (CLI)
     │
     ▼
┌─────────────┐
│   CLI       │  Click command groups (market, limit, advanced)
│  (cli.py)   │  Parses arguments, delegates to order managers
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Order     │  Validate inputs, build order parameters,
│  Managers   │  call Binance client, return result dicts
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Validator  │  Symbol format, quantity > 0, price > 0,
│ (validator) │  side (BUY/SELL), time-in-force (GTC/IOC/FOK)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Binance   │  python-binance Client
│   Client    │  Manages API authentication and requests
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  Binance Futures    │  REST API
│  API (fapi.binance  │  testnet.binancefuture.com (default)
│  .com)              │  fapi.binance.com (live)
└─────────────────────┘
```

---

## Project Structure

```
binance-futures-bot/
│
├── src/                        # Source code package
│   ├── __init__.py
│   ├── cli.py                  # CLI entry point (Click)
│   ├── config.py               # Environment configuration loader
│   ├── bot_logger.py           # Structured logging setup
│   ├── validator.py            # Input validation utilities
│   ├── market_orders.py        # Market order management
│   ├── limit_orders.py         # Limit order management
│   ├── diagnose_api.py         # API connectivity diagnostics
│   └── advanced/               # Advanced order types
│       ├── __init__.py
│       ├── oco.py              # OCO (take-profit + stop-loss) orders
│       ├── twap.py             # Time-weighted average price execution
│       └── grid.py             # Grid trading strategy
│
├── logs/                       # Runtime log files (auto-generated, gitignored)
├── .env.example                # Configuration template
├── .gitignore
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Installation

### Prerequisites

- Python 3.8 or later
- A Binance account (testnet for testing, or live for production)
- Binance API key with Futures permissions

### Setup

```bash
# Clone the repository
git clone https://github.com/your-username/binance-futures-bot.git
cd binance-futures-bot

# (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `python-binance` | 1.0.19 | Binance REST API client |
| `python-dotenv` | 1.0.0 | Environment variable loading |
| `click` | 8.1.7 | CLI framework |
| `colorama` | 0.4.6 | Colored terminal output |

---

## Configuration

### Environment Variables

```bash
# Copy the environment template
cp .env.example .env
```

Edit `.env` with your credentials:

```
BINANCE_API_KEY=your_api_key_here
BINANCE_SECRET_KEY=your_secret_key_here
BINANCE_TESTNET=True
```

| Variable | Default | Description |
|----------|---------|-------------|
| `BINANCE_API_KEY` | — | Binance API key with Futures permissions |
| `BINANCE_SECRET_KEY` | — | Binance API secret key |
| `BINANCE_TESTNET` | `True` | Use testnet endpoint when `True`; use live endpoint when `False` |

**Important:** `BINANCE_TESTNET` defaults to `True`. You must explicitly set it to `False` to use live trading.

### Getting Testnet API Keys

1. Visit [Binance Futures Testnet](https://testnet.binancefuture.com/)
2. Create an account and navigate to API Management
3. Generate a new API key with Futures permissions
4. Copy the API Key and Secret Key into your `.env` file

---

## Usage

All commands are invoked via the CLI module:

```bash
python -m src.cli [command]
```

### Market Orders

Execute buy or sell orders immediately at the best available price.

```bash
# Buy
python -m src.cli market buy BTCUSDT 0.002

# Sell
python -m src.cli market sell ETHUSDT 0.1
```

### Limit Orders

Place orders at a specific price. Supports configurable time-in-force.

```bash
# Default time-in-force: GTC (Good-Til-Cancelled)
python -m src.cli limit buy BTCUSDT 0.002 55000.0

# With explicit time-in-force
python -m src.cli limit sell ETHUSDT 0.1 4000.0 --tif IOC
python -m src.cli limit buy BTCUSDT 0.002 52000.0 --tif FOK

# Cancel a pending limit order
python -m src.cli limit cancel BTCUSDT 12345
```

### OCO Orders (Take-Profit + Stop-Loss)

Place a take-profit limit order and a stop-market order simultaneously. When one order fills, the other remains open.

```bash
python -m src.cli advanced oco BTCUSDT BUY 0.002 70000.0 55000.0
```

**Note:** This implementation places two separate orders (take-profit limit + stop-market) rather than using Binance's native OCO endpoint, which has different symbol and parameter requirements on Futures. Both orders are tracked in memory for coordinated management.

### TWAP Orders (Time-Weighted Average Price)

Split a large order into smaller chunks executed at regular intervals to reduce market impact.

```bash
# Execute 0.01 BTC over 30 minutes with 60-second intervals
python -m src.cli advanced twap BTCUSDT BUY 0.01 30 --interval 60
```

TWAP runs in a background thread. Order state is maintained in memory and is lost on process restart.

### Grid Trading

Create a series of buy and sell limit orders at evenly spaced price levels within a defined range.

```bash
# Create a grid from 58000 to 62000 with 5 levels, 0.002 per level
python -m src.cli advanced grid BTCUSDT 58000 62000 5 0.002
```

---

## Order Types

| Order | Description |
|-------|-------------|
| **Market** | Executes immediately at the best available price. |
| **Limit** | Executes only at the specified price or better. Supports GTC (Good-Til-Cancelled), IOC (Immediate-Or-Cancel), and FOK (Fill-Or-Kill). |
| **OCO** | Places a take-profit limit order and a stop-market order as a coordinated pair. Orders are tracked in memory for cancellation. |
| **TWAP** | Splits a large order into smaller chunks at regular intervals to reduce market impact. Executes in a background thread. |
| **Grid** | Creates multiple buy and sell limit orders at evenly spaced price levels within a defined range. |

---

## Logging

Logs are written daily to `logs/bot_YYYYMMDD.log`.

| Level | Destination | Detail |
|-------|-------------|--------|
| DEBUG | File only | Detailed execution info, function names, line numbers |
| INFO | File + console | Order placements, status updates |
| WARNING | File + console | Recoverable issues |
| ERROR | File + console | Failures and exceptions |

---

## API Diagnostics

The repository includes a diagnostic script for troubleshooting Binance API connectivity:

```bash
python -m src.diagnose_api
```

This script checks:
- Environment file and variable presence
- System time synchronization
- API connectivity (with and without authentication)
- Futures API permissions

---

## Testing Status

The following verification was performed during this release:

| Area | Status |
|------|--------|
| Module organization and import structure | ✓ Verified |
| CLI command structure and argument parsing | ✓ Verified |
| Dependency installation and compatibility | ✓ Verified |
| Configuration loading from `.env` | ✓ Verified |
| Input validation layer (symbol, quantity, price, side, TIF) | ✓ Verified |
| Structured logging setup and output | ✓ Verified |
| Error handling in order managers | ✓ Verified |
| API connectivity and authentication flow | ✓ Verified via diagnostic script |

The project was originally developed and tested against the Binance Futures Testnet during its initial implementation. This release focuses on repository quality, documentation, architecture, validation, and maintainability.

**Actual order execution** requires users to configure their own Binance Futures Testnet API credentials. No new end-to-end integration tests were performed as part of this release.

---

## Limitations

- **USDT-M Futures only** — does not support COIN-M or spot trading
- **Order state is in-memory** — active OCO, TWAP, and grid tracking is lost on process restart
- **No WebSocket support** — uses REST API with polling for TWAP execution
- **Single-asset grid** — each grid operates on one trading pair
- **No portfolio management** — this is an order execution tool, not a portfolio manager or risk management system
- **No persistent order history** — order state is not persisted to disk

---

## Security

- **API keys are read from `.env` only** — never hardcoded in source code
- **Testnet is the default** — `BINANCE_TESTNET=True` prevents accidental live trading
- **Logs contain order metadata only** — no API keys or secrets are logged
- **`.env` is gitignored** — credentials stay local and are never committed
- **No secrets in version control** — the repository has been audited for unintentionally committed credentials
- **Recommended:** Enable IP address restrictions on your Binance API keys and use the minimum required permissions

---

## Future Improvements

Potential areas for future development:

- OCO refactoring to use Binance's native OCO endpoint when Futures support is stable
- WebSocket integration for real-time price feeds and order status updates
- Persistent order state (e.g., SQLite or file-based storage)
- Portfolio-level tracking and risk management
- Additional order types (trailing stop, iceberg)
- Unit and integration test suite
- Docker containerization
- CLI output formatting improvements (tables, JSON output flag)

---

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

---

## Disclaimer

**This software is for educational purposes only.** Cryptocurrency futures trading carries substantial financial risk. You may lose more than your initial investment. Always test thoroughly on testnet before considering live trading. The authors are not responsible for any financial losses incurred through the use of this software.

---

## Release Checklist

The following items have been confirmed for this release:

- [x] README complete and professionally formatted
- [x] LICENSE file present (MIT)
- [x] `.env.example` present with clear instructions
- [x] `.gitignore` complete (excludes `.env`, `logs/`, `__pycache__/`, `.venv/`, etc.)
- [x] No credentials or secrets committed to version control
- [x] No log files committed to version control
- [x] Repository structure organized and documented
- [x] Installation instructions verified against a clean environment
- [x] CLI usage documented with examples
- [x] All dependencies listed with versions
- [x] Architecture documented with diagram
- [x] Limitations honestly documented
- [x] Testing status transparently described
- [x] Security notes provided
- [x] Repository ready for GitHub publication