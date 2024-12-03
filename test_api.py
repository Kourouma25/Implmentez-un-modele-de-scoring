import pytest
import pandas as pd
from main import app

# Charger les données depuis le CSV
data = pd.read_csv('donnee_test/fichier_testeAPI.csv')

# Convertir la première ligne en dictionnaire
donne_predire = data.iloc[0, :].to_dict()

def test_accueil():
    """Test de la route de base"""
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"message": "Bienvenue sur l'API de prédiction bancaire"}

def test_predire():
    """Test de la route /predire en utilisant les données du CSV"""
    client = app.test_client()
    
    # Utiliser les données chargées depuis le CSV pour la prédiction
    response = client.post("/predire", json=donne_predire)
    
    # Vérifier que la réponse a un code de statut 200 et que la prédiction est présente
    assert response.status_code == 200
    assert "prediction" in response.json["resultats"]


