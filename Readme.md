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