import os
import pandas as pd
import mlflow
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, precision_recall_curve, auc
from imblearn.over_sampling import SMOTE
import xgboost as xgb

# --- 1. Configuration and Setup ---
# Define project directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
DATA_FILE = os.path.join(DATA_DIR, "creditcard.csv")

# Ensure the models directory exists
os.makedirs(MODELS_DIR, exist_ok=True)

# Set up MLflow tracking
mlflow.set_experiment("Credit Card Fraud Detection")

# --- 2. Main Training Logic ---
with mlflow.start_run() as run:
    print(f"MLflow Run ID: {run.info.run_id}")

    # Load data
    print("Loading data...")
    df = pd.read_csv(DATA_FILE)

    # Preprocessing
    print("Preprocessing data...")
    
    # Separate features and target
    X = df.drop('Class', axis=1)
    y = df['Class']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # --- FIX: Scale all 30 features at once ---
    # This ensures the scaler is fitted on the entire dataset, which is crucial for Phase 2.
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Log class distribution before SMOTE
    print("Original training set shape: %s" % y_train.value_counts())
    mlflow.log_param("original_train_distribution", y_train.value_counts().to_dict())

    # Apply SMOTE to handle class imbalance
    print("Applying SMOTE to handle class imbalance...")
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train_scaled, y_train)
    
    # Log class distribution after SMOTE
    print("Resampled training set shape: %s" % pd.Series(y_train_resampled).value_counts())
    mlflow.log_param("resampled_train_distribution", pd.Series(y_train_resampled).value_counts().to_dict())

    # Model Training
    print("Training XGBoost model...")
    model = xgb.XGBClassifier(
        objective='binary:logistic',
        eval_metric='logloss',
        use_label_encoder=False,
        n_estimators=100,
        learning_rate=0.1,
        max_depth=3,
        random_state=42
    )
    model.fit(X_train_resampled, y_train_resampled)
    mlflow.log_params(model.get_params())

    # Evaluation
    print("Evaluating model...")
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]

    # Generate and print classification report
    report = classification_report(y_test, y_pred, output_dict=True)
    print("\n--- Classification Report ---")
    print(classification_report(y_test, y_pred))
    
    # Log metrics to MLflow
    mlflow.log_metric("accuracy", report['accuracy'])
    mlflow.log_metric("precision_fraud", report['1']['precision'])
    mlflow.log_metric("recall_fraud", report['1']['recall'])
    mlflow.log_metric("f1_score_fraud", report['1']['f1-score'])

    # Calculate and log AUPRC
    precision, recall, _ = precision_recall_curve(y_test, y_pred_proba)
    auprc = auc(recall, precision)
    print(f"\nArea Under the Precision-Recall Curve (AUPRC): {auprc:.4f}")
    mlflow.log_metric("auprc", auprc)

    # Save the model and scaler
    print("Saving model and scaler...")
    model_path = os.path.join(MODELS_DIR, "xgb_fraud_detector.joblib")
    scaler_path = os.path.join(MODELS_DIR, "scaler.joblib")
    
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    
    print(f"Model saved to: {model_path}")
    print(f"Scaler saved to: {scaler_path}")
    mlflow.log_artifact(model_path)
    mlflow.log_artifact(scaler_path)

    print("\n--- Training complete! ---")
    print("Run 'mlflow ui' in your terminal to see the experiment results.")


