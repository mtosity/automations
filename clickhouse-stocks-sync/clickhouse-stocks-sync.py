import os
import requests
import clickhouse_connect
from datetime import datetime
import logging
from dotenv import load_dotenv
import time
import csv

# Configuration
load_dotenv()

def load_symbols_from_csv(csv_file_path):
    """Load stock symbols from CSV file."""
    symbols = []
    try:
        with open(csv_file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:  # Skip empty rows
                    # Remove quotes and strip whitespace
                    symbol = row[0].strip().strip('"')
                    if symbol:  # Skip empty symbols
                        symbols.append(symbol)
        logging.info(f"Loaded {len(symbols)} symbols from {csv_file_path}")
        return symbols
    except FileNotFoundError:
        logging.error(f"CSV file not found: {csv_file_path}")
        return []
    except Exception as e:
        logging.error(f"Error reading CSV file: {str(e)}")
        return []

# Load symbols from CSV file
SYMBOLS = load_symbols_from_csv('../stocks.csv')
if not SYMBOLS:
    # Fallback to hardcoded symbols if CSV loading fails
    SYMBOLS = []
    logging.warning("Using fallback hardcoded symbols")

API_KEY = os.getenv('FMP_API_KEY')
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

# Configure logging
logging.basicConfig(
    filename='stock_ingest.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def fetch_stock_data(symbol):
    url = f'https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={API_KEY}'
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if not data:
                logging.warning(f"No data received for {symbol}")
                return None
            return data[0]
        except Exception as e:
            logging.error(f"Attempt {attempt+1} failed for {symbol}: {str(e)}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
    logging.error(f"All attempts failed for {symbol}")
    return None

def row_exists(client, symbol, date_str):
    """Check if a row with the same symbol and date already exists."""
    query = (
        "SELECT count() FROM stocks "
        "WHERE symbol = %(symbol)s AND date = %(date)s"
    )
    result = client.query(query, parameters={'symbol': symbol, 'date': date_str})
    return result.result_rows[0][0] > 0

def main():
    try:
        client = clickhouse_connect.get_client(
            host=os.getenv('CLICKHOUSE_HOST', 'localhost'),
            port=int(os.getenv('CLICKHOUSE_PORT', 8123)),
            username=os.getenv('CLICKHOUSE_USER', 'default'),
            password=os.getenv('CLICKHOUSE_PASSWORD', ''),
            database=os.getenv('CLICKHOUSE_DB', 'default')
        )

        today_str = datetime.now().strftime('%Y-%m-%d')
        today_date = datetime.now().date()  # Add date object for ClickHouse insert
        successful_inserts = 0

        for symbol in SYMBOLS:
            if row_exists(client, symbol, today_str):
                logging.info(f"Row for {symbol} on {today_str} already exists. Skipping insert.")
                continue

            raw_data = fetch_stock_data(symbol)
            if not raw_data:
                continue

            try:
                entry = {
                    'symbol': symbol,
                    'date': today_date,  # Use date object instead of string
                    'open': raw_data['open'],
                    'high': raw_data['dayHigh'],
                    'low': raw_data['dayLow'],
                    'close': raw_data['price'],
                    'volume': raw_data['volume'],
                    'change': raw_data['change'],
                    'changePercent': raw_data['changesPercentage'],
                    'vwap': raw_data['priceAvg50']
                }
            except KeyError as e:
                logging.error(f"Missing key {e} in response for {symbol}")
                continue

            try:
                client.insert(
                    table='stocks',
                    data=[[
                        entry['symbol'],
                        entry['date'],
                        entry['open'],
                        entry['high'],
                        entry['low'],
                        entry['close'],
                        entry['volume'],
                        entry['change'],
                        entry['changePercent'],
                        entry['vwap']
                    ]],
                    column_names=['symbol', 'date', 'open', 'high', 'low',
                                  'close', 'volume', 'change', 'changePercent', 'vwap']
                )
                successful_inserts += 1
                logging.info(f"Inserted data for {symbol} on {today_str}")
            except Exception as e:
                logging.error(f"Insert failed for {symbol}: {str(e)}")

        logging.info(f"Successfully inserted {successful_inserts}/{len(SYMBOLS)} symbols")

    except Exception as e:
        logging.critical(f"Fatal error: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()
