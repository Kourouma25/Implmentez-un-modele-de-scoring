from flask import Flask, jsonify, request
import joblib
import pandas as pd

app = Flask(__name__)

# Charger le modèle
model_enregistre = joblib.load('lgbm_model1.pkl')

# Définir le seuil de probabilité
SEUIL_PROBA = 0.5  

# Route de base
@app.route("/", methods=["GET"])
def accueil():
    return jsonify({"message": "Bienvenue sur l'API de prédiction de scoring crédit"})

# Route de prédiction
@app.route("/predire", methods=["POST"])
def predire():
    """Prédire avec les données envoyées dans le POST."""
    if not request.json:
        return jsonify({"erreur": "Aucun JSON fourni"}), 400

    try:
        # Récupérer les données envoyées dans la requête
        donnees = request.json

        # Convertir en DataFrame
        donnees_df = pd.DataFrame([donnees])

        # Prédiction avec le modèle
        predictions = model_enregistre.predict(donnees_df)

        # Retourner les résultats
        prediction_proba = model_enregistre.predict_proba(donnees_df)

        # Convertir le tableau ndarray en une liste normale Python
        resultats = {}
        prob_defaut = prediction_proba[0][1]  # Probabilité de défaut (classe 1)

        # Appliquer le seuil pour la prédiction
        if prob_defaut >= SEUIL_PROBA:
            resultats['prediction'] = 1  # Non accordé
        else:
            resultats['prediction'] = 0  # Accordé

        resultats['score'] = prob_defaut  # Probabilité de défaut

        return jsonify({"resultats": resultats})

    except Exception as e:
        return jsonify({"erreur": str(e)}), 400


# Lancer l'application
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)






