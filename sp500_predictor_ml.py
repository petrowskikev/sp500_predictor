import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from datetime import timedelta

# Daten laden
sp500 = yf.Ticker("^GSPC")
sp500 = sp500.history(period="max")

# Unnötige Spalten entfernen
del sp500["Dividends"]
del sp500["Stock Splits"]

# Zielspalte erstellen
sp500["Tomorrow"] = sp500["Close"].shift(-1)
sp500["Target"] = (sp500["Tomorrow"] > sp500["Close"]).astype(int)

# Filter für Daten ab 1990
sp500 = sp500.loc["1990-01-01":].copy()

# Zusätzliche technische Indikatoren berechnen
sp500["RSI"] = 100 - (100 / (1 + sp500["Close"].diff().clip(lower=0).rolling(14).mean() /
                             sp500["Close"].diff().clip(upper=0).abs().rolling(14).mean()))
sp500["SMA_20"] = sp500["Close"].rolling(20).mean()
sp500["Bollinger_Upper"] = sp500["SMA_20"] + 2 * sp500["Close"].rolling(20).std()
sp500["Bollinger_Lower"] = sp500["SMA_20"] - 2 * sp500["Close"].rolling(20).std()

# Merkmale erstellen
horizons = [2, 5, 60, 250]
new_predictors = []

for horizon in horizons:
    rolling_averages = sp500.rolling(horizon).mean()
    ratio_column = f"Close_Ratio{horizon}"
    sp500[ratio_column] = sp500["Close"] / rolling_averages["Close"]
    trend_column = f"Trend_{horizon}"
    sp500[trend_column] = sp500["Target"].shift(1).rolling(horizon).sum()
    new_predictors += [ratio_column, trend_column]

# Zusätzliche Merkmale hinzufügen
new_predictors += ["RSI", "Bollinger_Upper", "Bollinger_Lower"]

# Fehlende Werte entfernen
sp500 = sp500.dropna()

# Merkmale und Ziel trennen
X = sp500[new_predictors]
y = sp500["Target"]

# Daten skalieren
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Gesamte Daten verwenden, um das Modell zu trainieren
param_grid = {
    "n_estimators": [100, 200, 300],
    "min_samples_split": [10, 50, 100],
    "max_depth": [5, 10, None]
}

grid_search = GridSearchCV(RandomForestClassifier(random_state=1), param_grid, scoring="precision", cv=3)
grid_search.fit(X_scaled, y)
best_model = grid_search.best_estimator_

# Letzte Datenreihe als Input für die morgige Vorhersage
latest_data = X.iloc[-1:].copy()
latest_data_scaled = scaler.transform(latest_data)

# Datum des letzten Eintrags
last_date = sp500.index[-1]
tomorrow_date = last_date + timedelta(days=1)

# Vorhersage für morgen
y_pred_proba = best_model.predict_proba(latest_data_scaled)[0, 1]

# Entscheidung treffen
threshold_buy = 0.7  # Schwellenwert für Kaufen
threshold_sell = 0.3  # Schwellenwert für Verkaufen


def make_decision(proba):
    if proba >= threshold_buy:
        return "Kaufen"
    elif proba <= threshold_sell:
        return "Verkaufen"
    else:
        return "Halten"


decision = make_decision(y_pred_proba)

# Ergebnis ausgeben
print(f"Vorhersage für den {tomorrow_date.strftime('%Y-%m-%d')}:")
print(f"Wahrscheinlichkeit für steigenden Kurs: {y_pred_proba:.2f}")
print(f"Empfehlung: {decision}")
