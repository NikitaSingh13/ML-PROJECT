# data ingestion -> Data Ingestion is the process of collecting data from various sources 
# and bringing it into a system (like a database, data warehouse, or machine learning pipeline) 
# for further processing, analysis, or storage.

# --------------------------------------------
# Importing required libraries and modules
# --------------------------------------------

import sys    # used for system-specific parameters and functions (helps in exception handling)
import os     # helps in file and directory path operations
from src.exception import CustomException   # custom exception class to handle errors
from src.logger import logging              # custom logger for tracking the program flow
import pandas as pd                         # used for data manipulation and analysis
from sklearn.model_selection import train_test_split   # used to split dataset into training and testing data
from dataclasses import dataclass            # used to create data classes (for storing config info easily)

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig


from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer

# --------------------------------------------
# Dataclass: used to store configuration data (paths of files in this case)
# It automatically creates __init__() method, so we don't need to define it manually.
# --------------------------------------------
@dataclass
class DataIngestionConfig: # this class will store all the o/p of input data coming
    train_data_path: str = os.path.join('artifacts', "train_csv") # artifacts-o/p folder, train.csv- o/p file
    test_data_path: str = os.path.join('artifacts', "test_csv")   # test.csv- o/p file
    raw_data_path: str = os.path.join('artifacts', "data_csv")    # raw data before train-test split

# --------------------------------------------
# Class: DataIngestion
# This class handles the entire data ingestion process 
# (reading data, saving raw data, splitting into train/test, and saving outputs)
# --------------------------------------------
class DataIngestion:
    # Constructor: initializes the config object which contains paths for saving data
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
    
    # --------------------------------------------
    # Function: initiate_data_ingestion
    # This function performs the following:
    # 1. Reads dataset from a CSV file
    # 2. Saves it as a raw copy
    # 3. Splits it into train and test sets
    # 4. Saves both sets into 'artifacts' folder
    # --------------------------------------------
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            # here you read the data from mongoDb, mySQL, or anywhere 
            # and other code will remain the same — just the path provided in the first line will be changed
            df = pd.read_csv('notebook\data\stud.csv')
            logging.info('Read the dataset as dataframe')

            # creates the artifacts folder if it doesn’t exist already
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            # used to save the csv file to given folder and file named raw_data_path
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Train test split initiated")

            # splitting the dataset into train and test sets (80% train, 20% test)
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # saving both train and test datasets into separate CSV files
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info('Ingestion of the data is completed')

            # we are returning this so that my model can just grab the dataset from here and start the process
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        # handles any exception that might occur during data ingestion
        except Exception as e:
            raise CustomException(e, sys)

# --------------------------------------------
# Main function: runs the ingestion process when the file is executed directly
# --------------------------------------------
if __name__ == "__main__":
    obj = DataIngestion()               # create object of DataIngestion class
    train_data, test_data = obj.initiate_data_ingestion()       # call the function to start data ingestion

    data_transformation = DataTransformation()
    train_arr, test_arr,_ = data_transformation.initiate_data_transformation(train_data, test_data)

    modeltrainer = ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr, test_arr))
