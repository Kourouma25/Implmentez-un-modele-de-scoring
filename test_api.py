import pandas as pd
import requests
import pytest

# Charger les données de test
data = pd.read_csv('donnee_test/fichier_testeAPI.csv')
donne_predire = data.iloc[0, :].to_dict()

# URL de l'API
url = "http://127.0.0.1:5000"

def test_accueil():
    """Test pour vérifier la route d'accueil"""
    response = requests.get(url + "/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue sur l'API de prédiction bancaire"}

def test_predire():
    """Test pour vérifier la route de prédiction"""
    response = requests.post(url + "/predire", json=donne_predire)
    assert response.status_code == 200
    assert "prediction" in response.json()["resultats"]



