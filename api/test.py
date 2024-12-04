import requests
import json
import pandas as pd


def test_prediction_2():
    """
    Teste le point de terminaison de prédiction localement en utilisant un échantillon aléatoire du dataset.
    """
    # Charger les données à partir du fichier CSV et sélectionne un échantillon aléatoire d'une ligne
    df = pd.read_csv("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv",
                     index_col=0)
    df = df.sample(1)
    values = []

    # Construire le dictionnaire de l'échantillon
    for element in df.iloc[0, :].values.tolist():
        if type(element) != str:
            values.append(element.item())
        else:
            values.append(element)

    df_dict = {key: value for key, value in zip(df.columns, values)}

    # Envoyer les données à l'API de prédiction locale
    response = requests.post(
        "http://localhost:4000/predict",
        data=json.dumps(df_dict)
    )

    # Afficher le contenu envoyé et la réponse de l'API
    print(f"post: {df_dict}")
    print(f"   response: {response.json()}")


# Exécuter la fonction pour tester la prédiction
test_prediction_2()