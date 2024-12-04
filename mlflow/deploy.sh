# Se connecte à votre compte Heroku.
heroku login

# Se connecte au registre de conteneurs Heroku.
heroku container:login

# Envoie le conteneur Docker à Heroku pour l'application spécifiée par le nom "mlflowm".
# Remarque : remplacez "mlflowm" par le nom de votre application si nécessaire.
heroku container:push web -a mlflowm

# Déploie le conteneur envoyé sur l'application Heroku nommée "mlflowm".
# Remarque : remplacez "mlflowm" par le nom de votre application si nécessaire.
heroku container:release web -a mlflowm

# Ouvre l'application Heroku dans votre navigateur.
# Remarque : remplacez "mlflowm" par le nom de votre application si nécessaire.
# Vous pouvez également ouvrir manuellement : https://mlflowm.herokuapp.com/
heroku open -a mlflowm