docker run -it \
        -v "./:/mlflow" \
        -e MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI \
        -e PORT=4000 \
        -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
        -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
        -e BACKEND_STORE_URI=$BACKEND_STORE_URI \
        -e ARTIFACT_ROOT=$ARTIFACT_ROOT \
        getaround-mlflow python train.py --n_estimators=10 --min_samples_split=5