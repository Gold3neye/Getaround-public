# Utiliser l'image de base Miniconda3 fournie par ContinuumIO
FROM continuumio/miniconda3

# Définir le répertoire de travail à /dashboard
WORKDIR /dashboard

# Mettre à jour la liste des paquets apt-get
RUN apt-get update

# Copier le fichier requirements.txt dans le répertoire /dependencies
COPY requirements.txt /dependencies/requirements.txt

# Installer les dépendances spécifiées dans requheroku logs --tail -a getarounddemo75irements.txt
RUN pip install -r /dependencies/requirements.txt

# Copier le script de l'application dans le répertoire de travail actuel
COPY app.py /dashboard

# Définir la commande par défaut pour exécuter l'application Streamlit
CMD streamlit run --server.port $PORT app.py