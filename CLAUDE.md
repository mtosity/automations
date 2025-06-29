# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an automation scripts repository focused on financial data synchronization. The primary component is a ClickHouse stock data sync system that fetches stock quotes from Financial Modeling Prep API and stores them in a ClickHouse database.

## Architecture

- **Single Python script**: `clickhouse-stocks-sync/clickhouse-stocks-sync.py` handles all data fetching, processing, and database insertion
- **CSV-driven configuration**: Stock symbols are loaded from `stocks.csv` (500+ S&P 500 symbols)
- **Environment-based configuration**: Database connection and API credentials via `.env` file
- **Automated execution**: GitHub Actions workflow runs daily at 8:00 PM UTC
- **Logging**: All operations logged to `stock_ingest.log` with retry logic and error handling

## Development Setup

Before working with the code, set up the Python virtual environment:

```bash
# Create virtual environment (first time only)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Create `.env` file in `clickhouse-stocks-sync/` directory:
```env
FMP_API_KEY=your_financial_modeling_prep_api_key
CLICKHOUSE_HOST=localhost
CLICKHOUSE_PORT=8123
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=
CLICKHOUSE_DB=default
```

## Common Commands

**Run the stock sync script:**
```bash
python clickhouse-stocks-sync/clickhouse-stocks-sync.py
```

**Check logs:**
```bash
tail -f clickhouse-stocks-sync/stock_ingest.log
```

**Deactivate virtual environment:**
```bash
deactivate
```

## Key Dependencies

- `clickhouse-connect`: ClickHouse database connector
- `requests`: HTTP client for Financial Modeling Prep API
- `python-dotenv`: Environment variable management

## Data Flow

1. Load stock symbols from `stocks.csv`
2. For each symbol, fetch today's quote data from FMP API
3. Check if data already exists for today (prevents duplicates)
4. Insert new records into ClickHouse `stocks` table
5. Log all operations with retry logic for failed API calls

## GitHub Actions

The workflow `stocks-sync.yml` runs the synchronization daily with:
- 6-hour job timeout
- 5-hour sync step timeout
- Automatic log artifact upload on failure
- All secrets configured in GitHub repository settings