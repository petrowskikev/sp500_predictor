import yfinance as yf
import os


def fetch_sp500_data(start_date: str, end_date: str, save_path: str = r"..\data\sp500_data_raw.csv"):
    """
    Lädt historische S&P 500-Daten von Yahoo Finance und speichert sie lokal als CSV.
    """
    ticker_symbol = "^GSPC"

    print(f"Lade S&P 500-Daten von {start_date} bis {end_date}...")
    data = yf.download(ticker_symbol, start=start_date, end=end_date, interval="1d")
    print(f"Daten heruntergeladen.")

    print(f"Datan werden gespeichert bei dem path {save_path}")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    data.to_csv(save_path)
    print(f"Daten gespeichert unter: {save_path}")

    return data


if __name__ == "__main__":
    fetch_sp500_data(start_date="2015-01-01", end_date="2024-01-01")
