import pandas as pd
import os


def clean_sp500_data(input_path: str, output_path: str = "data/sp500_data_cleaned.csv"):
    """
    Bereinigt die S&P 500-Rohdaten und speichert sie in einer neuen Datei.
    """
    print("Lade Rohdaten zur Bereinigung...")
    df = pd.read_csv(input_path)

    print("Entferne Date und Ticker...")
    df = df[(df['Price'] != 'Ticker') & (df['Price'] != 'Date')]
    df.rename(columns={'Price': 'Date'}, inplace=True)
    df.set_index('Date', inplace=True)

    print("Entferne fehlende Werte...")
    df.dropna(inplace=True)

    df = df.loc[:, ['Open', 'Close', 'Adj Close', 'Low', 'High', 'Volume']]

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path)
    print(f"Bereinigte Daten gespeichert unter: {output_path}")

    return df


if __name__ == "__main__":
    clean_sp500_data(input_path="../data/sp500_data_raw.csv", output_path="../data/sp500_data_cleaned.csv")
