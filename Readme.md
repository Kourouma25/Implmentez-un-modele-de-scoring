# Parcours Data Scientist - Projet 7 : Implémentez un modèle de scoring 

## Présentation du projet

Ce projet consiste à développer un modèle de scoring capable de prédire la probabilité de remboursement d’un crédit par un client. Le modèle s’appuie sur des données variées et vise à fournir une prédiction automatique tout en répondant à un besoin accru de transparence. Un dashboard interactif a également été conçu pour permettre aux gestionnaires de relation client de mieux expliquer les décisions prises par le modèle et d'améliorer la connaissance client.

## Source des données

Les données utilisées pour ce projet proviennent de la compétition Kaggle : Home Credit Default Risk.

## Contexte

Nous travaillons en tant que Data Scientist pour une société financière, "Prêt à dépenser", qui propose des crédits à la consommation à des clients ayant peu ou pas d’historique de crédit.

## Structure du projet

### Dossiers et fichiers principaux

* Notebook : Contient le code de préparation des données, l’analyse exploratoire et la modélisation.

* main.py:  Contient les fichiers relatifs au fonctionnement de l’API de prédiction

* .github/workflow: workflow GitHub Actions  pour automatiser le déploiement de application sur Google Cloud Platform (GCP), en particulier sur Google App Engine

* model_entrainer: le modele entrainer

* app.yaml: décrit la configuration nécessaire pour déployer l'application sur Google App Engine

* requirements.txt:  contient la liste des dépendances Python nécessaires au fonctionnement de notre application.

* test_api.py: contient des tests unitaires ou d'intégration pour vérifier le bon fonctionnement des routes et fonctionnalités de notre API Flask.

* donnee_test: fichier qui contient des client fictif pour le test

## Modèle de scoring

Le modèle repose sur un algorithme supervisé de type classification (LightGBM et dummyclassifier), entraîné sur les données disponibles.

## API de prédiction

Développée avec FastAPI et permet d’envoyer des données client sous format JSON et de recevoir une prédiction en retour.

## Déploiement

Environnement utilisé : Google cloud consosole.
Processus automatisé via un workflow CI/CD comprenant et tests unitaires avant déploiement.


## Guide de Développement et Déploiement d'une API Flask sur Google Cloud avec GitHub

Ce guide explique comment développer, versionner, tester, et déployer une API Flask sur Google Cloud, tout en utilisant GitHub pour le versionnement et les commits pertinents.

* Creation d'un projet (nom_du_projet) 
- mkdir nom_du_projet
- cd nom_du_projet

* creation d'un environnement virtuel (python -m env nom_environnement) + activation .\nom_environnement\Scripts\activate
* installer Google cloud sdk 
- gcloud config set project [PROJECT_ID]

* installer git bash + creation compte github 
- git init (nitialisez Git dans le répertoire)

**Création des fichiers essentiels**

* ajout fichier .github\workflows deploy.yml
- mkdir -p .github/workflows
* requirements.txt ou il ya les dependance necessaire
* ajout d'un fichier pour le test 
* ajout Readme
* Configurer les secrets GitHub 
- GCP_CREDENTIALS : fichier JSON d'authentification pour Google Cloud. on le trouve dans google cloud console IAM & Admin > Service Accounts
- GCP_PROJECT_ID : L'ID de du projet Google Cloud.
* construction de l'API (main.py)
- python main.py (nous donne le lien locale)

après chaque modification, on effectue des commits pertinents ci-dessous
git add  nom_ajouter
git commit -m "Description des modifications"
git push origin main

