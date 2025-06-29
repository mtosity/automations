[![Daily Stock Data Sync](https://github.com/mtosity/automations/actions/workflows/stocks-sync.yml/badge.svg)](https://github.com/mtosity/automations/actions/workflows/stocks-sync.yml)

# Automations

Automation scripts for boring tasks.

- Clickhouse Stocks Sync: Syncs stock data from FMP to Clickhouse.
- Red Sync: Generates AI-powered stock analysis reports with manual workflow trigger.

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

#### Running the Red Sync Script

```bash
python red-sync/red-sync.py "AAPL,GOOGL,MSFT"
```

Stock symbols should be comma-separated. The script will generate AI-powered analysis reports and save them to Supabase.

#### Switching Back to System Environment

**Deactivate the virtual environment:**

```bash
deactivate
```

The `(venv)` should disappear from your terminal prompt.

## Environment Variables

Create environment files:

**For ClickHouse Stocks Sync** - `.env` file in the `clickhouse-stocks-sync/` directory:

```env
FMP_API_KEY=your_financial_modeling_prep_api_key
CLICKHOUSE_HOST=localhost
CLICKHOUSE_PORT=8123
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=
CLICKHOUSE_DB=default
```

**For Red Sync** - `.env` file in the `red-sync/` directory:

```env
AI_API_KEY=your_ai_api_key
AI_BASE_URL=https://api.deepseek.com
FMP_API_KEY=your_financial_modeling_prep_api_key
FMP_BASE_URL=https://financialmodelingprep.com
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

## Dependencies

- `clickhouse-connect`: ClickHouse database connector
- `python-dotenv`: Environment variable management
- `requests`: HTTP requests for API calls
- `openai`: OpenAI API client (used for DeepSeek API)
- `supabase`: Supabase Python client

## Pricing Information

**Discount Period**: UTC 16:30-00:30 (EST 11:30-19:30)

| Token Type | Standard Rate | Discount Rate |
|------------|---------------|---------------|
| 1M Tokens Input (Cache Hit) | $0.070 | $0.035 (50% OFF) |
| 1M Tokens Input (Cache Miss) | $0.270 | $0.135 (50% OFF) |
| 1M Tokens Output | $1.100 | $0.550 (50% OFF) |

*Note: During discount hours, pricing is 50% off standard rates*

## Project Structure

```
automations/
├── .github/
│   └── workflows/
│       ├── stocks-sync.yml           # Daily ClickHouse sync workflow
│       └── red-sync.yml              # Manual stock analysis workflow
├── venv/                             # Virtual environment
├── requirements.txt                  # Python dependencies
├── README.md                         # This file
├── clickhouse-stocks-sync/
│   ├── clickhouse-stocks-sync.py     # ClickHouse sync script
│   └── .env                          # Environment variables (create this)
└── red-sync/
    ├── red-sync.py                   # Stock analysis script
    ├── red_system_prompt.txt         # AI system prompt
    └── .env                          # Environment variables (create this)
```

## GitHub Actions Workflows

### Manual Stock Analysis (red-sync.yml)

Trigger the Red Sync workflow manually from GitHub Actions:

1. Go to the Actions tab in your GitHub repository
2. Select "Generate stock analysis report"
3. Click "Run workflow"
4. Enter comma-separated stock symbols (e.g., "AAPL,GOOGL,MSFT")
5. Analysis reports will be uploaded as artifacts

The workflow:
- Fetches comprehensive financial data from Financial Modeling Prep API
- Generates AI-powered analysis using DeepSeek's reasoning model
- Extracts structured data (sector, market cap, recommendation)
- Stores results in Supabase database
- Uploads analysis report as GitHub artifact
