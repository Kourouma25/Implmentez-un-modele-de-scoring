# Utiliser l'image officielle légère de Python
FROM python:3.9-slim

# Permettre l'affichage immédiat des instructions et messages de log dans les journaux
ENV PYTHONUNBUFFERED=1

# Définir le répertoire de travail dans le conteneur
ENV APP_HOME=/app
WORKDIR $APP_HOME

# Installer les dépendances système nécessaires (notamment pour LightGBM)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libgomp1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copier le code local dans l'image du conteneur
COPY . ./

# Installer les dépendances Python à partir du fichier requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Définir le port par défaut à 5000
ENV PORT=5000

# Lancer l'application Flask en utilisant le port dynamique
CMD ["sh", "-c", "waitress-serve --listen=0.0.0.0:$PORT main:app"]