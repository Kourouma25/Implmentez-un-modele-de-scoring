import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import plotly.express as px
import joblib
import shap
import matplotlib.pyplot as plt

# Charger le modèle
model = joblib.load('lgbm_model1.pkl')

# URL de l'API Flask déployée
API_URL = "http://192.168.1.10:5000/predire"

# Fonction pour envoyer les données à l'API
def envoyer_pour_prediction(donnees):
    try:
        response = requests.post(API_URL, json=donnees)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur API : {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Erreur lors de l'appel à l'API : {str(e)}")
        return None

# Fonction pour afficher la jauge avec un message explicatif
def afficher_gauge(prediction, prob):
    color = "green" if prediction == 0 else "red"

    if prediction == 0:
        st.markdown('<p style="color:green; font-size:20px;">Le prêt est <b>accordé</b>.</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:red; font-size:20px;">Le prêt est <b>non accordé</b>.</p>', unsafe_allow_html=True)

    prob_defaut = prob * 100

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob_defaut,
        title={'text': "Score de Crédit"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 50], 'color': "lightgreen"},
                {'range': [50, 100], 'color': "lightcoral"}
            ]
        },
    ))

    return fig, prob_defaut

# Fonction pour afficher l'importance spécifique des caractéristiques avec SHAP
def afficher_importance_specifique(donnees_client, model):
    donnees_client_df = pd.DataFrame([donnees_client])
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(donnees_client_df)

    shap_values_df = pd.DataFrame(shap_values[1], columns=donnees_client_df.columns) if isinstance(shap_values, list) else pd.DataFrame(shap_values, columns=donnees_client_df.columns)
    
    impact_positif = shap_values_df[shap_values_df > 0].dropna(axis=1, how='all')
    impact_negatif = shap_values_df[shap_values_df < 0].dropna(axis=1, how='all')

    impact_positif = impact_positif.T.sort_values(by=0, ascending=False).head(10)
    impact_negatif = impact_negatif.T.sort_values(by=0, ascending=True).head(10)

    fig_pos = px.bar(impact_positif, x=0, y=impact_positif.index, orientation='h', title="Impact Positif",
                     labels={0: 'Impact', 'index': 'Caractéristique'}, color=0, color_continuous_scale="reds")
    fig_neg = px.bar(impact_negatif, x=0, y=impact_negatif.index, orientation='h', title="Impact Négatif",
                     labels={0: 'Impact', 'index': 'Caractéristique'}, color=0, color_continuous_scale="blues")
    return fig_pos, fig_neg

# Fonction pour calculer l'importance globale des caractéristiques
def afficher_importance_globale(donnees, model):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(donnees)

    # Importance moyenne des caractéristiques
    shap_mean = pd.DataFrame({
        'Caractéristique': donnees.columns,
        'Importance Moyenne': abs(shap_values[1] if isinstance(shap_values, list) else shap_values).mean(axis=0)
    }).sort_values(by='Importance Moyenne', ascending=False).head(10)

    # Graphique
    fig_importance_globale = px.bar(shap_mean, x='Importance Moyenne', y='Caractéristique',
                                    orientation='h', title="Importance Globale des Caractéristiques",
                                    color='Importance Moyenne', color_continuous_scale="viridis")
    return fig_importance_globale

# Fonction pour afficher la comparaison des caractéristiques du client
def afficher_analyse_client(donnees_client, donnees_globales):
    moyenne_globale = donnees_globales.mean()

    comparaison_df = pd.DataFrame({
        "Caractéristiques": donnees_client.index,
        "Client": donnees_client.values,
        "Moyenne Globale": moyenne_globale.values
    }).fillna(0)

    comparaison_df["Client"] = pd.to_numeric(comparaison_df["Client"], errors='coerce')
    comparaison_df["Moyenne Globale"] = pd.to_numeric(comparaison_df["Moyenne Globale"], errors='coerce')

    fig_comparaison = px.bar(comparaison_df, x="Caractéristiques", y=["Client", "Moyenne Globale"],
                             barmode="group", title="Comparaison Client vs Moyenne Globale")
    return fig_comparaison

# Fonction pour analyser une caractéristique spécifique
def visualiser_feature_par_feature(donnees_client, donnees_globales):
    feature = st.selectbox("Choisissez une caractéristique", donnees_client.index)
    valeurs_globales = donnees_globales[feature]

    fig = px.histogram(valeurs_globales, nbins=30, title=f"Distribution de la caractéristique : {feature}",
                       labels={'value': feature, 'count': 'Nombre de clients'},
                       marginal="box")
    fig.add_vline(x=donnees_client[feature], line_color="red", line_dash="dash",
                  annotation_text="Client sélectionné", annotation_position="top left")
    return fig

# Fonction pour une analyse bi-variée
def visualiser_bivarie(donnees_globales):
    feature_x = st.selectbox("Choisissez la première caractéristique (axe X)", donnees_globales.columns, key="feature_x")
    feature_y = st.selectbox("Choisissez la deuxième caractéristique (axe Y)", donnees_globales.columns, key="feature_y")

    fig = px.scatter(donnees_globales, x=feature_x, y=feature_y,
                     title=f"Relation entre {feature_x} et {feature_y}",
                     labels={feature_x: feature_x, feature_y: feature_y},
                     color_discrete_sequence=["blue"])
    return fig

# Fonction principale
def main():
    st.set_page_config(layout="wide")
    st.title("Dashboard de Scoring de Crédit")

    # Menu latéral
    with st.sidebar:
        st.header("Charger un fichier CSV")
        fichier = st.file_uploader("Choisissez un fichier CSV", type=["csv"])

    if fichier is not None:
        donnees = pd.read_csv(fichier)
        st.sidebar.write("Aperçu des données :")
        st.sidebar.write(donnees.head())

        index = st.sidebar.selectbox("Sélectionnez un client", donnees.index)
        donnees_client = donnees.iloc[index]

        # Envoyer pour prédiction uniquement si le bouton est cliqué
        if st.sidebar.button("Envoyer pour prédiction"):
            donnees_client_dict = donnees_client.to_dict()
            resultats = envoyer_pour_prediction(donnees_client_dict)

            if resultats:
                st.session_state.prediction = resultats["resultats"]["prediction"]
                st.session_state.prob = resultats["resultats"]["score"]

        # Vérification si la prédiction est disponible
        if 'prediction' in st.session_state:
            prediction = st.session_state.prediction
            prob = st.session_state.prob

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Résultat de la Prédiction")
                fig_gauge, prob_defaut = afficher_gauge(prediction, prob)
                st.plotly_chart(fig_gauge)

                st.markdown(f"**Probabilité de non-remboursement (Défaut):** {prob*100:.2f}%")

            with col2:
                st.subheader("Importance des Caractéristiques")
                fig_pos, fig_neg = afficher_importance_specifique(donnees_client, model)
                st.plotly_chart(fig_pos)
                st.plotly_chart(fig_neg)

            st.markdown("---")
            st.subheader("Top 10 Caractéristiques les plus importantes")
            fig_importance_globale = afficher_importance_globale(donnees, model)
            st.plotly_chart(fig_importance_globale)

            st.markdown("---")
            st.subheader("Analyse du client")
            fig_comparaison = afficher_analyse_client(donnees_client, donnees)
            st.plotly_chart(fig_comparaison)

            st.markdown("---")
            st.subheader("Analyse par Caractéristique")
            fig_feature = visualiser_feature_par_feature(donnees_client, donnees)
            st.plotly_chart(fig_feature)

            st.markdown("---")
            st.subheader("Analyse Bi-Variée")
            fig_bivarie = visualiser_bivarie(donnees)
            st.plotly_chart(fig_bivarie)

if __name__ == "__main__":
    main()




































