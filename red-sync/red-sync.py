from openai import OpenAI
from supabase import create_client, Client
import requests
from urllib.parse import urlencode, urljoin
from datetime import datetime, timedelta
import json
import os
import sys
from dotenv import load_dotenv

load_dotenv()

AI_API_KEY = os.getenv('AI_API_KEY')
AI_BASE_URL = os.getenv('AI_BASE_URL', 'https://api.deepseek.com')
FMP_BASE_URL = os.getenv('FMP_BASE_URL', 'https://financialmodelingprep.com')
FMP_API_KEY = os.getenv('FMP_API_KEY')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

client = OpenAI(
    api_key=AI_API_KEY,
    base_url=AI_BASE_URL,
)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def build_url(base_url, path, params):
    params['apikey'] = FMP_API_KEY
    full_url = urljoin(base_url, path)
    if params:
        return f"{full_url}?{urlencode(params)}"
    return full_url

def call_api(url):
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"API call failed with status code {response.status_code}: {response.text}")
    return response.json()

def formatKeyToLabel(key):
    """Convert a snake_case or camelCase key to a human-readable label."""
    import re
    # Replace underscores with spaces
    key = key.replace('_', ' ')
    # Add space before capital letters (for camelCase)
    key = re.sub(r'(?<!^)(?=[A-Z])', ' ', key)
    # Capitalize each word
    return key.title()

def formatStockData(data):
    """Format stock data for display."""
    formatted_data = ""
    for item in data:
        for key, value in item.items():
            label = formatKeyToLabel(key)
            formatted_data += f"{label}: {value}\n"
        formatted_data += "\n"
    return formatted_data

def run(stock_symbol):
    data = ""
    data += "##Stock Quote\n" + formatStockData(call_api(build_url(FMP_BASE_URL, "/stable/quote", {"symbol": stock_symbol})))
    data += "##Company Profile Data\n" + formatStockData(call_api(build_url(FMP_BASE_URL, "/stable/profile", {"symbol": stock_symbol})))
    data += "##Company Notes\n" + formatStockData(call_api(build_url(FMP_BASE_URL, "/stable/company-notes", {"symbol": stock_symbol})))
    data += "##Income Statements\n" + formatStockData(call_api(build_url(FMP_BASE_URL, "/stable/income-statement", {"symbol": stock_symbol, "limit": 12, "period": "quarter"})))
    data += "##Balance Sheet Statement\n" + formatStockData(call_api(build_url(FMP_BASE_URL, "/stable/balance-sheet-statement", {"symbol": stock_symbol, "limit": 12, "period": "quarter"})))
    data += "##Cash Flow Statement\n" + formatStockData(call_api(build_url(FMP_BASE_URL, "/stable/cash-flow-statement", {"symbol": stock_symbol, "limit": 12, "period": "quarter"})))
    data += "##Financial Ratios\n" + formatStockData(call_api(build_url(FMP_BASE_URL, "/stable/ratios", {"symbol": stock_symbol, "limit": 4})))
    data += "##Key Metrics\n" + formatStockData(call_api(build_url(FMP_BASE_URL, "/stable/key-metrics", {"symbol": stock_symbol, "limit": 4})))
    data += "##Financial Scores\n" + formatStockData(call_api(build_url(FMP_BASE_URL, "/stable/financial-scores", {"symbol": stock_symbol})))
    data += "##Enterprise Values\n" + formatStockData(call_api(build_url(FMP_BASE_URL, "/stable/enterprise-values", {"symbol": stock_symbol})))
    data += "##Ratings snapshot\n" + formatStockData(call_api(build_url(FMP_BASE_URL, "/stable/ratings-snapshot", {"symbol": stock_symbol})))
    data += "##Grades Historical\n" + formatStockData(call_api(build_url(FMP_BASE_URL, "/stable/grades-historical", {"symbol": stock_symbol})))
    data += "##Grades News\n" + formatStockData(call_api(build_url(FMP_BASE_URL, "/stable/grades-news", {"symbol": stock_symbol, "limit": 16 })))
    data += "##News\n" + formatStockData(call_api(build_url(FMP_BASE_URL, "/stable/news/stock", {"symbol": stock_symbol})))
    from_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    data += "##Exponential Moving Average\n" + formatStockData(call_api(build_url(FMP_BASE_URL, "/stable/technical-indicators/ema", {"symbol": stock_symbol, "periodLength": "12", "timeframe": "1day", "from": from_date})))

    with open("red_system_prompt.txt", "r") as file:
        system_prompt = file.read()

    print(f"{stock_symbol} - Prompt created. Now generating recommendation...")
    completion = client.chat.completions.create(
        model="deepseek-reasoner",
        store=True,
        messages=[
            {"role": "system", "content": f"{system_prompt}"},
            {
                "role": "user",
                "content": f"Here is the quantitative data:\n\n\n {data}",
            },
        ],
    )
    output = completion.choices[0].message.content

    print(f"{stock_symbol} - Recommendation generated. Now extracting sector, market cap, and recommendation...")

    completion = client.chat.completions.create(
        model="deepseek-chat",
        store=True,
        messages=[
            {"role": "system", "content": """
    The user will provide an financial report of an stock in markdown format.
    Your task is to extract the sector (CONS DISC, CONS STPL, ENERGY, FINANCIALS, HEALTH, INDUSTRIALS, MATERIALS, REAL ESTATE, TECHNOLOGY, COMMUNICATION SVS, UTILITIES),
    market cap, recommendation (strong_buy, buy, hold, sell).

    EXAMPLE JSON OUTPUT:
    {
        "sector": "TECHNOLOGY",
        "market_cap": 2500000000,
        "recommendation": "strong_buy"
    }
    """},
            {
                "role": "user",
                "content": output,
            },
        ],
        response_format={
            'type': 'json_object'
        }
    )
    extracted_data = json.loads(completion.choices[0].message.content)
    print(f"{stock_symbol} - Extracted: {extracted_data['sector']}, {extracted_data['market_cap']}, {extracted_data['recommendation']}")

    response = (supabase.table("thestockie_post").upsert({
        "id": stock_symbol,
        "prompt": "[NOT PROVIDED]",
        "response": output,
        "created_by": "1a39b220-ec72-4bb0-bf01-32eff314d796",
        "recommendation": extracted_data['recommendation'],
        "market_cap": extracted_data['market_cap'],
        "sector": extracted_data['sector'],
    }).execute())
    print(f"{stock_symbol} - Data saved to Supabase")

def get_stock_symbols():
    """Get stock symbols from command line arguments or CSV file."""
    if len(sys.argv) > 1:
        # Use command line arguments - expect comma-separated symbols
        symbols_input = sys.argv[1]
        symbols = [symbol.strip().upper() for symbol in symbols_input.split(',') if symbol.strip()]
        print(f"Using {len(symbols)} symbols from command line: {symbols}")
        return symbols
    else:
        return []

if __name__ == "__main__":
    stock_symbols = get_stock_symbols()
    
    if not stock_symbols:
        print("No stock symbols to process. Exiting.")
        sys.exit(1)
    
    print(f"Processing {len(stock_symbols)} stock symbols...")
    print("Starting processing...")
    
    # Process each stock symbol
    from datetime import datetime, timedelta
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(run, stock_symbol): stock_symbol for stock_symbol in stock_symbols}
        for future in futures:
            try:
                future.result()  # Wait for the result
            except Exception as e:
                print(f"Error processing {futures[future]}: {e}")