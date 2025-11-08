import os
import sys
from dataclasses import dataclass
from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
# from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Splitting training and test input data")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )

            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                # "Linear Regression": LinearRegression(),
                "KNN Regressor": KNeighborsRegressor(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=0),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }

            params = {
                "Decision Tree": {'criterion': ['squared_error', 'friedman_mse']},
                "Random Forest": {'n_estimators': [64, 128, 256]},
                "Gradient Boosting": {
                    'learning_rate': [0.1, 0.05],
                    'n_estimators': [64, 128],
                },
                # "Linear Regression": {},
                "KNN Regressor": {'n_neighbors': [3, 5, 7]},
                "XGBRegressor": {
                    'learning_rate': [0.1, 0.05],
                    'n_estimators': [64, 128],
                },
                "CatBoosting Regressor": {
                    'depth': [6, 8],
                    'iterations': [50, 100],
                    'learning_rate': [0.05, 0.1],
                },
                "AdaBoost Regressor": {
                    'learning_rate': [0.1, 0.05],
                    'n_estimators': [64, 128],
                },
            }

            # ✅ Now returns both trained models and scores
            model_report, trained_models = evaluate_models(
                X_train=X_train, y_train=y_train,
                X_test=X_test, y_test=y_test,
                models=models, param=params
            )

            best_model_name = max(model_report, key=model_report.get)
            best_model_score = model_report[best_model_name]
            best_model = trained_models[best_model_name]

            logging.info(f"Best model: {best_model_name} | R2 Score: {best_model_score}")

            if best_model_score < 0.6:
                raise CustomException("No good model found (R2 < 0.6)")
            
            # just extra-----------------

            print(f"Best Model: {best_model_name}")
            print(f"Best R2 Score: {best_model_score}")
            print(f"Saving model object: {best_model}")

            # ---------------------------

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted = best_model.predict(X_test)
            return r2_score(y_test, predicted)

        except Exception as e:
            raise CustomException(e, sys)
