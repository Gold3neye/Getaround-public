# Se connecte à votre compte Heroku.
heroku login

# Se connecte au registre de conteneurs Heroku.
heroku container:login

# Envoie le conteneur Docker à Heroku pour l'application spécifiée par le nom "api-melchior".
# L'option -a permet de spécifier le nom de l'application Heroku à laquelle s'applique la commande.
heroku container:push web -a api-melchior

# Déploie le conteneur envoyé sur l'application Heroku.
# L'option -a est utilisée pour indiquer le nom de l'application Heroku cible.
heroku container:release web -a api-melchior

# Ouvre l'application Heroku dans votre navigateur.
# L'option -a spécifie le nom de l'application à ouvrir.
heroku open -a api-melchior