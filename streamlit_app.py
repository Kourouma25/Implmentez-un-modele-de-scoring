import streamlit as st
import pandas as pd
import requests

# URL de l'API Flask déployée
API_URL = "https://projet-7-modele-de-scoring.ew.r.appspot.com/predire"

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
    st.write("Téléchargez un fichier CSV contenant les données des clients pour obtenir une prédiction et une probabilité.")

    # Téléchargement de fichier par l'utilisateur
    fichier = st.file_uploader("Choisissez un fichier CSV", type=["csv"])

    if fichier is not None:
        try:
            # Lecture du fichier CSV
            donnees = pd.read_csv(fichier)
            st.subheader("Aperçu des données chargées :")
            st.write(donnees.head())

            # Vérifier si le fichier contient des données
            if donnees.empty:
                st.warning("Le fichier téléchargé est vide. Veuillez charger un fichier valide.")
                return

            # Lorsque l'utilisateur appuie sur le bouton "Lancer la prédiction"
            if st.button("Lancer la prédiction"):
                st.write("Envoi des données à l'API pour prédiction...")

                # Sélectionner la première ligne et convertir en dictionnaire
                donnees_a_predire = donnees.iloc[3].to_dict()
                resultats = envoyer_pour_prediction(donnees_a_predire)

                # Si nous avons des résultats, on les affiche
                if resultats:
                    st.subheader("Résultats de la prédiction :")
                    prediction = resultats["resultats"]["prediction"]
                    probabilites = resultats["resultats"]["score"]

                    st.write(f"Prédiction : {prediction}")
                    st.write(f"Probabilités : {probabilites}")
                else:
                    st.error("Aucun résultat n'a été obtenu.")
        except Exception as e:
            st.error(f"Erreur lors de la lecture ou du traitement du fichier : {str(e)}")

if __name__ == "__main__":
    main()







