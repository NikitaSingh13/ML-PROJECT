#  front-end using flask
'''
    running command : python app.py
    port type on the chrome: http://127.0.0.1:5000/

'''

from flask import Flask, request, render_template
import numpy as np 
import pandas as pd
import os
import sys

# Ensure we're in the right directory for deployment
if not os.path.exists('artifacts') and __name__ == "__main__":
    # Try to find the project root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(os.path.join(current_dir, 'artifacts')):
        os.chdir(current_dir)
        print(f"Changed working directory to: {current_dir}")
    else:
        print(f"Warning: artifacts directory not found. Current dir: {os.getcwd()}")

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application= Flask(__name__)

app = application

# route for the home page

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/debug')
def debug():
    """Debug route to check file paths and working directory"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        debug_info = {
            'cwd': os.getcwd(),
            'app_file_location': current_dir,
            'artifacts_in_cwd': os.path.exists('artifacts'),
            'artifacts_in_app_dir': os.path.exists(os.path.join(current_dir, 'artifacts')),
            'model_in_cwd': os.path.exists('artifacts/model.pkl'),
            'preprocessor_in_cwd': os.path.exists('artifacts/preprocessor.pkl'),
            'files_in_cwd': os.listdir('.') if os.path.exists('.') else 'Not accessible',
            'sys_path': sys.path[0] if sys.path else 'No sys.path'
        }
        
        if os.path.exists('artifacts'):
            debug_info['artifacts_contents'] = os.listdir('artifacts')
        elif os.path.exists(os.path.join(current_dir, 'artifacts')):
            debug_info['artifacts_contents'] = os.listdir(os.path.join(current_dir, 'artifacts'))
        else:
            debug_info['artifacts_contents'] = 'Artifacts directory not found'
            
        return f"<pre>{debug_info}</pre>"
    except Exception as e:
        return f"<pre>Debug error: {str(e)}</pre>"

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        try:
            data = CustomData(
                gender=request.form.get('gender'),
                race_ethnicity=request.form.get('race_ethnicity'),
                parental_level_of_education=request.form.get('parental_level_of_education'),
                lunch=request.form.get('lunch'),
                test_preparation_course=request.form.get('test_preparation_course'),
                reading_score=request.form.get('reading_score'),
                writing_score=request.form.get('writing_score')
            )
            pred_df = data.get_data_as_data_frame()
            print("Input data:")
            print(pred_df)

            predict_pipeline = PredictPipeline()
            results = predict_pipeline.predict(pred_df)
            print(f"Prediction results: {results}")
            return render_template('home.html', results=results[0])
        except Exception as e:
            print(f"Error in prediction: {str(e)}")
            return render_template('home.html', results=f"Error: {str(e)}")
    

if __name__=="__main__":
    app.run(host = "0.0.0.0")