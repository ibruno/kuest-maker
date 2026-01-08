# Kuest-Maker

A market making bot for Kuest prediction markets. This bot automates the process of providing liquidity to markets on Kuest by maintaining orders on both sides of the book with configurable parameters. A summary of my experience running this bot is available [here](https://x.com/defiance_cr/status/1906774862254800934)

## Overview

Kuest-Maker is a comprehensive solution for automated market making on Kuest. It includes:

- Real-time order book monitoring via WebSockets
- Position management with risk controls
- Customizable trade parameters fetched from Postgres
- Automated position merging functionality
- Sophisticated spread and price management

## Structure

The repository consists of several interconnected modules:

- `kuest_data`: Core data management and market making logic
- `kuest_merger`: Utility for merging positions (based on open-source Kuest code)
- `kuest_stats`: Account statistics tracking
- `kuest_utils`: Shared utility functions
- `data_updater`: Separate module for collecting market information

## Requirements

- Python 3.9.10 or higher
- Node.js (for kuest_merger)
- Postgres database
- Kuest account and API credentials

## Installation

This project uses UV for fast, reliable package management.

### Install UV

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

### Install Dependencies

```bash
# Install all dependencies
uv sync

# Install with development dependencies (black, pytest)
uv sync --extra dev
```

### Quick Start

```bash
# Run the market maker (recommended)
uv run python main.py

# Update market data
uv run python update_markets.py

# Update statistics
uv run python update_stats.py
```

### Setup Steps

#### 1. Clone the repository

```bash
git clone https://github.com/yourusername/kuest-maker.git
cd kuest-maker
```

#### 2. Install Python dependencies

```bash
uv sync
```

#### 3. Install Node.js dependencies for the merger

```bash
cd kuest_merger
npm install
cd ..
```

#### 4. Set up environment variables

```bash
cp .env.example .env
```

#### 5. Configure your credentials in `.env`

Edit the `.env` file with your credentials:
- `PK`: Your private key for Kuest
- `BROWSER_ADDRESS`: Your wallet address
- `DATABASE_URL`: Postgres connection string

**Important:** Make sure your wallet has done at least one trade through the UI so that the permissions are proper.

#### 6. Set up Postgres

Run the migration:

```bash
uv run python scripts/migrate.py
```

Add minimal config rows:

```sql
INSERT INTO maker_sheet_rows (sheet_name, row_data) VALUES
('Selected Markets', '{"question":"<market question>","param_type":"default"}'),
('Hyperparameters', '{"type":"default","param":"trade_size","value":100}'),
('Hyperparameters', '{"type":"default","param":"max_size","value":200}');
```

#### 7. Update market data

Run the market data updater to fetch all available markets:

```bash
uv run python update_markets.py
```

This should run continuously in the background (preferably on a different IP than your trading bot).

Update configuration by editing rows in `maker_sheet_rows`:
- `Selected Markets`: markets you want to trade
- `Hyperparameters`: config parameters by `type`

#### 8. Start the market making bot

```bash
uv run python main.py
```

## Configuration

The bot is configured via Postgres using the `maker_sheet_rows` table:

- **Selected Markets**: Markets you want to trade
- **All Markets**: Database of all markets on Kuest (written by `update_markets.py`)
- **Hyperparameters**: Configuration parameters for the trading logic


## Kuest Merger

The `kuest_merger` module is a particularly powerful utility that handles position merging on Kuest. It's built on open-source Kuest code and provides a smooth way to consolidate positions, reducing gas fees and improving capital efficiency.

## Important Notes

- This code interacts with real markets and can potentially lose real money
- Test thoroughly with small amounts before deploying with significant capital
- The `data_updater` is technically a separate repository but is included here for convenience

## License

MIT
