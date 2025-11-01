# data transformation -> Data Transformation is the process of converting raw data (collected during data ingestion) into a clean, structured, and usable format for analysis or machine learning.
# just hover any word if you wanna know about that


import os
import sys
from dataclasses import dataclass # we used a decorator dataclass in the data_ingestion

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer # used for the pipeline purpose 
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    # this pkl file will be responsible in converting categorical to numerical  or standscalar wok etc etc
    '''Why we need to save (pickle) it:

        Once the preprocessing object is trained,
        you need to use the exact same transformations later —
        during testing, model serving, or prediction on new data.
    '''
    preprocessor_obj_file_path = os.path.join('artifacts', "preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
        This function is responsible for data transformation based on diff type of columns
        '''
        try:
            numerical_columns = ['reading_score', 'writing_score']
            categorical_columns = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']

            num_pipeline = Pipeline(
                steps = [
                    # responsible in handling the missing values
                    ("imputer", SimpleImputer(strategy="median")),
                    #handle standard scaler
                    ("scaler", StandardScaler())
                ]
            )
            cat_pipeline = Pipeline(
                steps=[
                    # to handle the missing values
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder(handle_unknown="ignore")),
                    ("scaler", StandardScaler(with_mean=False))

                ]
            )

            logging.info(f"Numerical columns {numerical_columns}")
            logging.info(f"Categorical columns {categorical_columns}")


            # column transformer - > It combines multiple pipelines — one for numeric data, one for categorical data — and applies them to their respective columns in parallel.
            # means: “For the numeric columns, apply the steps defined in num_pipeline, and for the categorical columns, apply the steps defined in cat_pipeline — and then combine the results together into one final preprocessed dataset
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns)
                ]
            )

            return preprocessor
        
        except Exception as e:
            raise CustomException(e, sys)


     # you'll get the train path and test path from the dtaa ingestion file   
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            logging.info("obtaining preprocessing object")

            preprocessing_obj = self.get_data_transformer_object()

            target_column_name = "math_score"
            numerical_columns = ['writing_score','reading_score']

            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info(f"applying processing obj on training dataframe and testing dataframe")


            #  fit()->Learns the parameters/statistics from the data (like mean, standard deviation, min-max range, etc.).Does not change the data itself.Think of it as “learning from data”.
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df) # fit_transform() -> It is simply a shortcut for doing both: fit() → learn parameters transform() → apply transformationCommonly used on training data only.
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df) #  transform() -> Uses the already learned parameters (from fit) to apply the transformation to the data.Does not learn anything new.

            # np.c_ is a NumPy shortcut (indexing trick) used to concatenate (join) arrays column-wise. Think of c_ as meaning “concatenate along columns” — the “c” stands for columns.        
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]

            logging.info(f"saved preprocessing object")

            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e, sys)
            