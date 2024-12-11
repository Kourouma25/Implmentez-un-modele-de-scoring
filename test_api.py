import pandas as pd
import requests
import pytest
import joblib

# Charger les données de test
data = pd.read_csv('donnee_test/fichier_testeAPI.csv')
donne_predire = data.iloc[0: 1,:]
# Charger le modèle
model_enregistre = joblib.load('model_entrainer/lgbm_model.pkl')


def test_predire():

    score = model_enregistre.predict_proba(donne_predire)[0]
    score = score[0]

    assert score >= 0 
    assert score <= 1
    """Test pour vérifier la route de prédiction"""
    
