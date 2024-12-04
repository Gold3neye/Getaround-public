import argparse
import pandas as pd
import time
import mlflow
from mlflow.models.signature import infer_signature
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score

if __name__ == "__main__":
    # Configuration MLflow
    mlflow.set_tracking_uri("http://getaround-mlflow:4000")
    experiment_name = "car_rental_price"
    mlflow.set_experiment(experiment_name)

    # Parsing des arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_estimators", type=int, default=100)
    parser.add_argument("--min_samples_split", type=int, default=2)
    args = parser.parse_args()

    # Chargement des données
    df = pd.read_csv("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv")

    # Préparation des données
    X = df.drop('rental_price_per_day', axis=1)
    y = df['rental_price_per_day']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Définition des colonnes
    categorical_features = [
        "model_key", "fuel", "paint_color", "car_type",
        "private_parking_available", "has_gps", "has_air_conditioning",
        "automatic_car", "has_getaround_connect", "has_speed_regulator",
        "winter_tires"
    ]
    numerical_features = ["mileage", "engine_power"]

    # Préprocesseurs
    categorical_transformer = OneHotEncoder(drop='first', sparse_output=False)
    numerical_transformer = StandardScaler()

    # Création du preprocesseur
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    # Création du pipeline
    model = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(
            n_estimators=args.n_estimators,
            min_samples_split=args.min_samples_split,
            random_state=42
        ))
    ])

    # Entraînement avec MLflow
    with mlflow.start_run():
        print("Début de l'entraînement...")
        start_time = time.time()

        # Entraînement
        model.fit(X_train, y_train)

        # Prédictions
        train_predictions = model.predict(X_train)
        test_predictions = model.predict(X_test)

        # Calcul des métriques
        train_rmse = mean_squared_error(y_train, train_predictions, squared=False)
        test_rmse = mean_squared_error(y_test, test_predictions, squared=False)
        train_r2 = r2_score(y_train, train_predictions)
        test_r2 = r2_score(y_test, test_predictions)

        # Log des paramètres
        mlflow.log_params({
            "n_estimators": args.n_estimators,
            "min_samples_split": args.min_samples_split
        })

        # Log des métriques
        mlflow.log_metrics({
            "train_rmse": train_rmse,
            "test_rmse": test_rmse,
            "train_r2": train_r2,
            "test_r2": test_r2,
            "training_time": time.time() - start_time
        })

        # Log du modèle
        signature = infer_signature(X_train, train_predictions)
        mlflow.sklearn.log_model(
            model,
            experiment_name,
            signature=signature,
            registered_model_name=f"Random_Forest_{experiment_name}"
        )

        print(f"Entraînement terminé en {time.time() - start_time:.2f} secondes")