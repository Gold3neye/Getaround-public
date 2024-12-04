# Exécute un conteneur Docker de manière interactive.
docker run -it \
  # Monte le répertoire courant de l'hôte dans le conteneur Docker à /home/app.
  -v "$(pwd):/home/app" \
  # Définit la variable d'environnement PORT à 80 à l'intérieur du conteneur.
  -e PORT=80 \
  # Mappe le port 80 du conteneur au port 4000 de l'hôte.
  -p 4000:80 \
  # Spécifie l'image Docker à utiliser pour démarrer le conteneur.
  getaround-dashboard