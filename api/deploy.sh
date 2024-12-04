# Se connecter à Heroku
heroku login

# Se connecter au registre de conteneurs Heroku
heroku container:login

# Envoyer le conteneur vers Heroku pour l'application "api-melchior"
heroku container:push web -a api-melchior

# Déployer le conteneur sur Heroku pour l'application "api-melchior"
heroku container:release web -a api-melchior

# Ouvrir l'application Heroku "api-melchior" dans le navigateur
heroku open -a api-melchior