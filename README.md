# Student Exam Performance Predictor 🎓

This project predicts a student's math exam score based on demographic and academic features using a machine learning pipeline. The web interface is built with Flask and styled for a modern user experience.

## Features

- **Predicts math scores** based on gender, ethnicity, parental education, lunch type, test preparation, reading, and writing scores.
- **Interactive web interface** for easy data input and result visualization.
- **Automated ML pipeline**: data ingestion, transformation, model training, and prediction.
- **Model selection**: Trains and evaluates multiple regressors, saving the best one.
- **Deployment-ready**: Includes a `Procfile` for easy deployment (e.g., Render, Heroku).

## Demo

[Live App Link Here](#) <!-- Replace with your deployed app link -->

## Project Structure

```
├── app.py
├── requirements.txt
├── Procfile
├── static/
│   └── css/
│       └── style.css
├── templates/
│   ├── home.html
│   └── index.html
├── src/
│   ├── components/
│   │   ├── data_ingestion.py
│   │   ├── data_transformation.py
│   │   └── model_trainer.py
│   ├── pipeline/
│   │   └── predict_pipeline.py
│   └── utils.py
└── artifacts/
    ├── model.pkl
    └── preprocessor.pkl
```

## How It Works

1. **Data Ingestion**: Reads student data from CSV, splits into train/test sets.
2. **Data Transformation**: Preprocesses features (encoding, scaling, imputing).
3. **Model Training**: Trains several regressors, selects and saves the best.
4. **Prediction**: User inputs data via web form, receives predicted math score.

## Running Locally

1. **Clone the repo** and navigate to the project directory.
2. **Create a virtual environment** (recommended):
    ```
    conda create -p venv python=3.8 -y
    conda activate ./venv
    ```
3. **Install dependencies**:
    ```
    pip install -r requirements.txt
    ```
4. **Run the app**:
    ```
    python app.py
    ```
5. **Open your browser** at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Deployment

- The app is ready for deployment on platforms like Render or Heroku.
- `Procfile` is included for Gunicorn.
- Replace the demo link above with your deployed URL.

## Notes

- Data and model artifacts are stored in the `artifacts/` directory.
- For development, see `notes.txt` for setup and troubleshooting tips.

## License

This project is for educational purposes.

---

**Deployed at:** [Your Live Link Here](#)