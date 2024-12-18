# **S&P 500 Predictor** 📈

Dieses Projekt zielt darauf ab, mithilfe von **Machine Learning (ML)** und **technischen Indikatoren** Kauf-, Verkaufs- oder Haltesignale für den **S&P 500 Index** vorherzusagen. Es nutzt historische Kursdaten, um Trends und Muster zu analysieren und daraus Handlungsempfehlungen abzuleiten.

---

## **Projektstruktur**

- **Datenbeschaffung**: Rohdaten des S&P 500 werden über die [Yahoo Finance API](https://finance.yahoo.com/) abgerufen.
- **Datenbereinigung**: Unnötige Spalten werden entfernt, und die Daten werden in eine saubere Struktur gebracht.
- **Feature Engineering**: Technische Indikatoren wie Moving Averages, RSI und Volatilität werden berechnet.
- **Modellentwicklung**: Ein Machine-Learning-Modell wird trainiert, um Signale (`Buy`, `Sell`, `Hold`) vorherzusagen.
- **Visualisierung**: Explorative Datenanalyse (EDA) und Ergebnisplots geben Einblicke in die Daten und Modellleistung.

---

## **Anforderungen**

- **Python >= 3.8**
- **Bibliotheken**:
   - `pandas`
   - `numpy`
   - `yfinance`
   - `matplotlib`
   - `seaborn`
   - `scikit-learn`
   - `pandas-ta`

Installiere die Abhängigkeiten mit folgendem Befehl:

```bash
pip install -r requirements.txt