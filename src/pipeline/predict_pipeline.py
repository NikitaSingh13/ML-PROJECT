import sys
import os
import pandas as pd
from src.exception import CustomException
from src.utils import load_object 


class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            # Multiple strategies to find artifacts directory
            artifacts_path = None
            
            # Strategy 1: From current working directory (deployment scenario)
            if os.path.exists(os.path.join(os.getcwd(), 'artifacts')):
                artifacts_path = os.path.join(os.getcwd(), 'artifacts')
            
            # Strategy 2: Relative to this file location
            elif os.path.exists('artifacts'):
                artifacts_path = 'artifacts'
            
            # Strategy 3: From project root (calculated from file location)
            else:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
                potential_path = os.path.join(project_root, 'artifacts')
                if os.path.exists(potential_path):
                    artifacts_path = potential_path
            
            # If still not found, print debug info and raise error
            if artifacts_path is None:
                cwd = os.getcwd()
                file_dir = os.path.dirname(os.path.abspath(__file__))
                available_files = os.listdir(cwd) if os.path.exists(cwd) else []
                error_msg = f"""
                Artifacts directory not found!
                Current working directory: {cwd}
                This file location: {file_dir}
                Files in current dir: {available_files}
                """
                raise FileNotFoundError(error_msg)
            
            model_path = os.path.join(artifacts_path, 'model.pkl')
            preprocessor_path = os.path.join(artifacts_path, 'preprocessor.pkl')
            
            print(f"Working directory: {os.getcwd()}")
            print(f"Using artifacts path: {artifacts_path}")
            print(f"Model path: {model_path}")
            print(f"Preprocessor path: {preprocessor_path}")
            
            # Verify files exist
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found at: {model_path}")
            if not os.path.exists(preprocessor_path):
                raise FileNotFoundError(f"Preprocessor file not found at: {preprocessor_path}")

            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)

            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            return preds
        except Exception as e:
            raise CustomException(e, sys)


class CustomData:
    def __init__(self,
        gender: str,
        race_ethnicity: str,
        parental_level_of_education,
        lunch: str,
        test_preparation_course: str,
        reading_score: int,
        writing_score: int):

        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        self.reading_score = reading_score
        self.writing_score = writing_score


    def get_data_as_data_frame(self):
        try:
            # ✅ Added: lowercase for categorical columns (avoid unseen category errors)
            custom_data_input_dict = {
                "gender": [self.gender.lower()],
                "race_ethnicity": [self.race_ethnicity.lower()],
                "parental_level_of_education": [self.parental_level_of_education.lower()],
                "lunch": [self.lunch.lower()],
                "test_preparation_course": [self.test_preparation_course.lower()],
                "reading_score": [float(self.reading_score)],
                "writing_score": [float(self.writing_score)]
            }

            return pd.DataFrame(custom_data_input_dict)
        
        except Exception as e:
            raise CustomException(e, sys)
