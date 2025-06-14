[![Daily Stock Data Sync](https://github.com/mtosity/automations/actions/workflows/stocks-sync.yml/badge.svg)](https://github.com/mtosity/automations/actions/workflows/stocks-sync.yml)

# Automations

Automation scripts for boring tasks.

- Clickhouse Stocks Sync: Syncs stock data from FMP to Clickhouse.

## Environment Setup

This project uses a Python virtual environment to manage dependencies safely without affecting your system Python installation.

### First Time Setup

1. **Clone/Navigate to the project directory:**

   ```bash
   cd automations
   ```

2. **Create virtual environment** (if not already created):

   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**

   ```bash
   source venv/bin/activate
   ```

   You should see `(venv)` in your terminal prompt indicating the environment is active.

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Daily Usage

#### Switching to Virtual Environment

**Activate the environment:**

```bash
source venv/bin/activate
```

**Verify you're in the virtual environment:**

- Your terminal prompt should show `(venv)` at the beginning
- Check Python path: `which python` should show the venv path

#### Running the Stock Sync Script

```bash
python clickhouse-stocks-sync/clickhouse-stocks-sync.py
```

#### Switching Back to System Environment

**Deactivate the virtual environment:**

```bash
deactivate
```

The `(venv)` should disappear from your terminal prompt.

## Environment Variables

Create a `.env` file in the `clickhouse-stocks-sync/` directory with:

```env
FMP_API_KEY=your_financial_modeling_prep_api_key
CLICKHOUSE_HOST=localhost
CLICKHOUSE_PORT=8123
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=
CLICKHOUSE_DB=default
```

## Dependencies

- `clickhouse-connect`: ClickHouse database connector
- `python-dotenv`: Environment variable management
- `requests`: HTTP requests for API calls

## Project Structure

```
automations/
├── .github/
│   └── workflows/
│       └── stocks-sync.yml            # GitHub Actions workflow
├── venv/                              # Virtual environment
├── requirements.txt                   # Python dependencies
├── README.md                         # This file
└── clickhouse-stocks-sync/
    ├── clickhouse-stocks-sync.py     # Main script
    └── .env                          # Environment variables (create this)
```
