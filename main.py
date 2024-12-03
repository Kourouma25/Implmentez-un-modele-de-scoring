from flask import Flask, jsonify, request
import joblib
import pandas as pd

app = Flask(__name__)

# Charger le modèle
model_enregistre = joblib.load('lgbm_model.pkl')

# Route de base
@app.route("/", methods=["GET"])
def accueil():
    return jsonify({"message": "Bienvenue sur l'API de prédiction bancaire"})

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
        resultats = donnees  # Données envoyées
        resultats['prediction'] = int(predictions[0])  # Ajouter la prédiction
        
        return jsonify({"resultats": resultats})
    
    except Exception as e:
        return jsonify({"erreur": str(e)}), 400


# Lancer l'application
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)