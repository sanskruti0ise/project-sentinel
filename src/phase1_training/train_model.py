import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, average_precision_score
from imblearn.over_sampling import SMOTE
import joblib
import mlflow
from pathlib import Path

# --- Configuration & Setup ---
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DATA_FILE = DATA_DIR / "creditcard.csv"
MODEL_DIR = PROJECT_ROOT / "models"
MODEL_DIR.mkdir(exist_ok=True) # Ensure the models directory exists

# MLflow configuration
MLFLOW_EXPERIMENT_NAME = "Credit_Card_Fraud_Detection"
mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

# --- Main Training Function ---
def train():
    """Main function to run the model training pipeline."""
    
    # Start an MLflow run to log all our parameters, metrics, and artifacts
    with mlflow.start_run() as run:
        print(f"MLflow Run ID: {run.info.run_id}")
        mlflow.log_param("data_path", str(DATA_FILE))

        # 1. Load Data
        print("Loading data...")
        try:
            df = pd.read_csv(DATA_FILE)
        except FileNotFoundError:
            print(f"ERROR: Data file not found at {DATA_FILE}")
            print("Please run the setup.py script first to download the data.")
            return

        # 2. Preprocessing
        print("Preprocessing data...")
        
        # Scale 'Amount' and 'Time' features
        scaler = StandardScaler()
        df['scaled_amount'] = scaler.fit_transform(df['Amount'].values.reshape(-1, 1))
        df['scaled_time'] = scaler.fit_transform(df['Time'].values.reshape(-1, 1))
        df = df.drop(['Time', 'Amount'], axis=1)

        # Define features (X) and target (y)
        X = df.drop('Class', axis=1)
        y = df['Class']

        # 3. Train-Test Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        print(f"Original training set shape: {y_train.value_counts()}")

        # 4. Handle Imbalance with SMOTE
        print("Applying SMOTE to handle class imbalance...")
        smote = SMOTE(random_state=42)
        X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
        print(f"Resampled training set shape: {y_train_resampled.value_counts()}")
        mlflow.log_param("resampling_strategy", "SMOTE")
        
        # 5. Model Training (XGBoost)
        print("Training XGBoost model...")
        model = xgb.XGBClassifier(
            objective='binary:logistic',
            eval_metric='aucpr', # Area Under the Precision-Recall Curve
            use_label_encoder=False,
            n_estimators=100,
            learning_rate=0.1,
            max_depth=3,
            random_state=42
        )
        
        model.fit(X_train_resampled, y_train_resampled)
        
        # Log model parameters to MLflow
        mlflow.log_params(model.get_params())

        # 6. Evaluation
        print("Evaluating model...")
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]

        # Generate and print classification report
        report = classification_report(y_test, y_pred, output_dict=True)
        print("\n--- Classification Report ---")
        print(classification_report(y_test, y_pred))

        # Calculate AUPRC (Area Under the Precision-Recall Curve)
        auprc = average_precision_score(y_test, y_pred_proba)
        print(f"Area Under the Precision-Recall Curve (AUPRC): {auprc:.4f}")

        # Log metrics to MLflow
        mlflow.log_metric("auprc", auprc)
        mlflow.log_metric("precision_fraud", report['1']['precision'])
        mlflow.log_metric("recall_fraud", report['1']['recall'])
        mlflow.log_metric("f1_score_fraud", report['1']['f1-score'])
        
        # 7. Save Artifacts (Model and Scaler)
        print("Saving model and scaler...")
        model_path = MODEL_DIR / "xgb_fraud_detector.joblib"
        scaler_path = MODEL_DIR / "scaler.joblib"
        
        joblib.dump(model, model_path)
        joblib.dump(scaler, scaler_path)
        print(f"Model saved to: {model_path}")
        print(f"Scaler saved to: {scaler_path}")
        
        # Log artifacts to MLflow
        mlflow.log_artifact(str(model_path))
        mlflow.log_artifact(str(scaler_path))

    print("\n--- Training complete! ---")
    print("Run 'mlflow ui' in your terminal to see the experiment results.")

if __name__ == "__main__":
    train()


