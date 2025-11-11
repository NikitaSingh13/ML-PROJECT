import os
import sys
import dill
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from src.exception import CustomException

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise CustomException(e, sys)


def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        from sklearn.model_selection import GridSearchCV
        from sklearn.metrics import r2_score

        report = {}
        trained_models = {}

        for model_name, model in models.items():
            print(f"\nTraining {model_name}...")

            para = param.get(model_name, {})
            gs = GridSearchCV(model, para, cv=3, n_jobs=-1)
            gs.fit(X_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            y_test_pred = model.predict(X_test)
            score = r2_score(y_test, y_test_pred)

            print(f"✅ {model_name} | R²: {score:.4f}")

            report[model_name] = score
            trained_models[model_name] = model  # save trained model

        return report, trained_models

    except Exception as e:
        raise CustomException(e, sys)



def load_object(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        print(f"Attempting to load object from: {file_path}")
        with open(file_path, 'rb') as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        print(f"Error loading object from {file_path}: {str(e)}")
        raise CustomException(e, sys)
