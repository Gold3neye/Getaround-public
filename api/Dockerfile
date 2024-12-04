# Utilise une image de base basée sur Miniconda pour la gestion des environnements Python
FROM continuumio/miniconda3

# Définit le répertoire de travail de l'application
WORKDIR /app

# Met à jour la liste des paquets et installe les outils nécessaires
RUN apt update && apt install -y nano unzip python3 curl

# Copie le fichier des dépendances Python dans le conteneur
COPY requirements.txt /dependencies/requirements.txt

# Installe les dépendances Python spécifiées dans le fichier requirements.txt
RUN pip install -r /dependencies/requirements.txt

# Copie le fichier principal de l'application dans le répertoire de travail
COPY app.py /app/

# Copie le répertoire de données dans le conteneur
COPY data /app/data/

# Copie le répertoire du modèle dans le conteneur
COPY model /app/model/

# Définit la commande à exécuter lorsque le conteneur démarre
CMD gunicorn app:app --bind 0.0.0.0:$PORT --worker-class uvicorn.workers.UvicornWorker