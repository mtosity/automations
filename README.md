# ClickHouse Stocks Sync

A Python automation tool that fetches stock data and syncs it to ClickHouse database.

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

## GitHub Actions Automation

The project includes a GitHub Actions workflow that automatically runs the stock sync script daily at 8:00 PM UTC.

### Setting Up Automated Runs

1. **Push the workflow file to your GitHub repository:**

   ```bash
   git add .github/workflows/stocks-sync.yml
   git commit -m "Add daily stock sync workflow"
   git push
   ```

2. **Configure GitHub Secrets:**

   Go to your GitHub repository → Settings → Secrets and variables → Actions

   Add the following repository secrets:

   - `FMP_API_KEY`: Your Financial Modeling Prep API key
   - `CLICKHOUSE_HOST`: ClickHouse server host
   - `CLICKHOUSE_PORT`: ClickHouse server port (usually 8123)
   - `CLICKHOUSE_USER`: ClickHouse username
   - `CLICKHOUSE_PASSWORD`: ClickHouse password
   - `CLICKHOUSE_DB`: ClickHouse database name

3. **Manual Trigger:**

   You can manually trigger the workflow from:
   GitHub repository → Actions → "Daily Stock Data Sync" → "Run workflow"

### Workflow Features

- **Scheduled Runs**: Automatically runs daily at 8:00 PM UTC
- **Manual Trigger**: Can be run manually when needed
- **Dependency Caching**: Speeds up workflow execution
- **Error Handling**: Uploads logs if the sync fails
- **Artifact Retention**: Keeps error logs for 30 days

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

## Troubleshooting

**Virtual environment not activating?**

- Make sure you're in the correct directory (`automations/`)
- Try: `ls -la` to verify `venv/` folder exists

**Import errors?**

- Ensure virtual environment is activated (`(venv)` in prompt)
- Reinstall dependencies: `pip install -r requirements.txt`

**Permission issues?**

- Make sure the script is executable: `chmod +x clickhouse-stocks-sync/clickhouse-stocks-sync.py`

**GitHub Actions failing?**

- Check that all secrets are properly configured in GitHub repository settings
- Verify the ClickHouse server is accessible from GitHub Actions runners
- Check the workflow logs in the Actions tab for specific error messages
# automations
