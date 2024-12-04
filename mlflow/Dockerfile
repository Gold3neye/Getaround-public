# Utilisation de l'image de base Miniconda3 de ContinuumIO, idéale pour gérer les environnements Python
FROM continuumio/miniconda3

# Définir le répertoire de travail à /mlflow
WORKDIR /mlflow

# Mise à jour de la liste des paquets apt-get pour obtenir les informations les plus récentes sur les packages disponibles
RUN apt update

# Installation de quelques outils utiles : nano (éditeur de texte), unzip (outil de décompression), curl (outil de transfert de données)
RUN apt install -y nano unzip curl

# Installation de Deta CLI en utilisant curl pour télécharger et exécuter le script d'installation
RUN curl -fsSL https://get.deta.dev/cli.sh | sh

# Télécharger le fichier zip de l'interface de ligne de commande AWS v2
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
# Décompresser le fichier zip téléchargé
RUN unzip awscliv2.zip
# Exécuter le script d'installation pour l'interface de ligne de commande AWS
RUN ./aws/install

# Copier le fichier des dépendances Python requirements.txt dans le répertoire /dependencies du conteneur
COPY requirements.txt /dependencies/requirements.txt
# Installer les dépendances Python listées dans requirements.txt
RUN pip install -r /dependencies/requirements.txt

# Copier le fichier train.py (script de formation) dans le répertoire de travail du conteneur
COPY train.py /mlflow

# Définir des variables d'environnement pour les informations d'identification AWS et pour les URIs nécessaires à MLflow
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV BACKEND_STORE_URI=$BACKEND_STORE_URI
ENV ARTIFACT_ROOT=$ARTIFACT_ROOT

# Définir la commande par défaut pour exécuter le serveur MLflow.
# Le serveur MLflow écoutera sur le port spécifié par la variable d'environnement $PORT, accessible à partir de l'hôte 0.0.0.0.
# Les URI pour le backend store et l'artifact root sont également spécifiées via les variables d'environnement définies précédemment.
CMD mlflow server -p $PORT \
    --host 0.0.0.0 \
    --backend-store-uri $BACKEND_STORE_URI \
    --default-artifact-root $ARTIFACT_ROOT