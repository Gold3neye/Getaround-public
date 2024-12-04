# Affiche un message indiquant que l'accès se fait via le navigateur à localhost:4000/docs
echo "Accédez via le navigateur à localhost:4000/docs"

# Exécute un conteneur Docker de manière interactive
docker run -it \
    # Monte le répertoire courant dans le conteneur sous /home/app
    -v "$(pwd):/home/app" \
    # Mappe le port 4000 de l'hôte au port 4000 du conteneur
    -p 4000:4000 \
    # Définit des variables d'environnement pour le conteneur
    -e PORT=4000 \
    -e MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI \
    -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    -e BACKEND_STORE_URI=$BACKEND_STORE_URI \
    -e ARTIFACT_ROOT=$ARTIFACT_ROOT \
    # Spécifie l'image Docker à utiliser
    getaround-api