import pandas as pd
import numpy as np

import pandas as pd
import numpy as np


def add_features_to_sp500_data(input_path: str,
                               output_path: str = "../data/sp500_data_cleaned_and_feature_engineered.csv"):
    df = pd.read_csv(input_path, parse_dates=["Date"], index_col="Date")
    print("Lade Daten erfolgreich.")

    # 1. Moving Averages: Kurzfristige (SMA_5) und langfristige (SMA_50)
    df["SMA_5"] = df["Close"].rolling(window=5).mean()  # 5-Tage-Durchschnitt
    print("Feature 'SMA_5' hinzugefügt: Der 5-Tage gleitende Durchschnitt des Schlusskurses zeigt kurzfristige Trends.")

    df["SMA_50"] = df["Close"].rolling(window=50).mean()  # 50-Tage-Durchschnitt
    print("Feature 'SMA_50' hinzugefügt: Der 50-Tage gleitende Durchschnitt zeigt langfristige Trends.")

    # 2. Bollinger Bands: Obere und untere Grenze
    df["STD_20"] = df["Close"].rolling(window=20).std()  # Standardabweichung über 20 Tage
    df["Bollinger_Upper"] = df["SMA_5"] + 2 * df["STD_20"]
    df["Bollinger_Lower"] = df["SMA_5"] - 2 * df["STD_20"]
    print(
        "Features 'Bollinger_Upper' und 'Bollinger_Lower' hinzugefügt: Zeigen die obere und untere Grenze basierend auf Volatilität.")

    # 3. Relative Strength Index (RSI)
    def calculate_rsi(series, period=14):
        delta = series.diff(1)
        gain = delta.where(delta > 0, 0)  # Gewinne
        loss = -delta.where(delta < 0, 0)  # Verluste

        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    df["RSI_14"] = calculate_rsi(df["Close"], period=14)
    print(
        "Feature 'RSI_14' hinzugefügt: Der Relative Strength Index zeigt überkaufte (>70) oder überverkaufte (<30) Situationen.")

    # 4. MACD (Moving Average Convergence Divergence)
    short_window = 12
    long_window = 26
    signal_window = 9

    df["EMA_12"] = df["Close"].ewm(span=short_window, min_periods=1).mean()  # Exponentieller 12-Tage-Durchschnitt
    df["EMA_26"] = df["Close"].ewm(span=long_window, min_periods=1).mean()  # Exponentieller 26-Tage-Durchschnitt
    df["MACD"] = df["EMA_12"] - df["EMA_26"]  # MACD-Linie
    df["MACD_Signal"] = df["MACD"].ewm(span=signal_window, min_periods=1).mean()  # Signal-Linie
    print(
        "Features 'MACD' und 'MACD_Signal' hinzugefügt: Zeigen Trendumkehrsignale basierend auf exponentiellen Durchschnitten.")

    # 5. Rate of Change (ROC)
    df["ROC_10"] = df["Close"].pct_change(periods=10) * 100  # Prozentuale Änderung über 10 Tage
    print("Feature 'ROC_10' hinzugefügt: Zeigt die prozentuale Änderung des Schlusskurses über 10 Tage.")

    # 6. Volatilität: Standardabweichung der täglichen Rendite
    df["Daily_Return"] = df["Close"].pct_change()  # Tägliche Rendite
    df["Volatility_10"] = df["Daily_Return"].rolling(window=10).std() * np.sqrt(252)  # Annualisierte Volatilität
    print("Feature 'Volatility_10' hinzugefügt: Annualisierte Volatilität der täglichen Rendite über 10 Tage.")

    # 7. Lag Features: Close-Preise der letzten Tage
    df["Close_Lag_1"] = df["Close"].shift(1)  # Gestern
    df["Close_Lag_2"] = df["Close"].shift(2)  # Vorgestern
    df["Close_Lag_3"] = df["Close"].shift(3)  # Vor 3 Tagen
    print("Features 'Close_Lag_1', 'Close_Lag_2' und 'Close_Lag_3' hinzugefügt: Schlusskurse der letzten 3 Tage.")

    df = df.dropna()
    print("NaN-Werte entfernt.")

    df.to_csv(output_path)
    print(f"Feature Engineering abgeschlossen. Ergebnisse gespeichert in: {output_path}")


if __name__ == "__main__":
    add_features_to_sp500_data(input_path="../data/sp500_data_cleaned.csv", )
