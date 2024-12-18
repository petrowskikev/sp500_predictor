from flask import Flask, jsonify, render_template
from sp500_predictor_ml import tomorrow_date, y_pred_proba, decision

# Flask-Anwendung initialisieren
print("Initialisiere Flask-Anwendung...")
app = Flask(__name__)


@app.route('/')
def home():
    # Homepage mit der Vorhersage
    print("Homepage-Aufruf: Anzeige der Vorhersage für den nächsten Tag.")
    return render_template('index.html',
                           date=tomorrow_date.strftime('%Y-%m-%d'),
                           probability=f"{y_pred_proba:.2f}",
                           decision=decision)


@app.route('/api/predict', methods=['GET'])
def predict_api():
    # API-Endpunkt, um die Vorhersagen als JSON bereitzustellen
    print("API-Endpunkt aufgerufen: /api/predict")
    result = {
        "date": tomorrow_date.strftime('%Y-%m-%d'),
        "probability": round(y_pred_proba, 2),
        "decision": decision
    }
    return jsonify(result)


if __name__ == '__main__':
    print("Starte Flask-Anwendung...")
    print("Die Website ist erreichbar unter: http://127.0.0.1:5000/")
    app.run(debug=True)
