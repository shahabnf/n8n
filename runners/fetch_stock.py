import yfinance as yf
import json
import sys

def get_stocks(symbols):
    results = []
    # Initialize a session for all tickers to be efficient
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.fast_info
            results.append({
                "symbol": symbol,
                "price": round(info['last_price'], 2),
                "currency": info['currency'],
                "status": "success"
            })
        except Exception as e:
            results.append({
                "symbol": symbol,
                "status": "error",
                "message": str(e)
            })
    return results

if __name__ == "__main__":
    # Get symbols from command line arguments (space separated)
    # e.g. python fetch_stock.py MSFT.NE AMD.NE
    symbols_input = sys.argv[1:] if len(sys.argv) > 1 else ["AAPL"]
    data = get_stocks(symbols_input)
    print(json.dumps(data))
