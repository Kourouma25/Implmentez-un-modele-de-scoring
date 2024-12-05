import streamlit as st
import pandas as pd
import requests

# URL de l'API Flask déployée (remplacez ceci par l'URL de votre propre API)
API_URL = "https://mon-projet7flask-225404997464.europe-west9.run.app/predire"

def envoyer_pour_prediction(donnees):
    """Envoie les données à l'API Flask et récupère les prédictions."""
    try:
        # Envoyer les données via une requête POST
        response = requests.post(API_URL, json=donnees)
        if response.status_code == 200:
            return response.json()  # Retourne les résultats en JSON
        else:
            st.error(f"Erreur API : {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Erreur lors de l'appel à l'API : {str(e)}")
        return None

def main():
    st.title("Application de Prédiction Bancaire")
    st.write("Téléchargez un fichier CSV contenant les données des clients pour obtenir des prédictions.")

    # Téléchargement de fichier par l'utilisateur
    fichier = st.file_uploader("Choisissez un fichier CSV", type=["csv"])

    if fichier is not None:
        try:
            # Lecture du fichier CSV
            donnees = pd.read_csv(fichier)
            st.subheader("Aperçu des données chargées :")
            st.write(donnees.head())  # Afficher un aperçu des données

            # Lorsque l'utilisateur appuie sur le bouton "Lancer la prédiction"
            if st.button("Lancer la prédiction"):
                st.write("Envoi des données à l'API pour prédiction...")  

                # Nous envoyons les données (en prenant la première ligne comme exemple)
                donnees_a_predire = donnees.iloc[0, :].to_dict()  # Conversion de la première ligne en dictionnaire
                resultats = envoyer_pour_prediction(donnees_a_predire)  # Appel à l'API Flask
                
                # Si nous avons des résultats, on les affiche
                if resultats:
                    st.subheader("Résultats de la prédiction :")
                    st.write(resultats["resultats"])  # Affichage des résultats retournés par l'API
        except Exception as e:
            st.error(f"Erreur lors de la lecture du fichier : {str(e)}")

if __name__ == "__main__":
    main()
