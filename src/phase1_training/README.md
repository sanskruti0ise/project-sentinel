# Project Sentinel: Phase 1 - Foundational Model Development

## 1. Objective

The primary objective of Phase 1 was to establish a strong, reliable baseline for our fraud detection capabilities. The goal was to develop a high-performing machine learning model that could accurately distinguish between legitimate and fraudulent credit card transactions. This phase focused on creating a fully automated, reproducible, and well-documented training pipeline, which serves as the core analytical engine for the subsequent AI agent phases.

---

## 2. Architecture and Core Components

The training pipeline was constructed using industry-standard Python libraries known for their robustness and performance in machine learning tasks.

- **XGBoost** — A powerful and efficient gradient boosting algorithm, chosen for its high performance on structured, tabular data like financial transactions.
- **Scikit-learn** — Used for essential preprocessing tasks, including data splitting and feature scaling (`StandardScaler`).
- **Pandas** — The primary tool for data manipulation and loading the initial CSV dataset.
- **MLflow** — Integrated for comprehensive experiment tracking. Every training run automatically logs parameters, performance metrics, and model artifacts, ensuring full traceability and reproducibility.
- **SMOTE (from imbalanced-learn)** — A critical component used to address the severe class imbalance in the dataset by synthetically generating new samples for the minority (fraud) class.

---

## 3. How It Works: The Training Pipeline

The entire training process is automated and follows these key steps:

1. **Data Ingestion:** The script automatically downloads the *Credit Card Fraud Detection* dataset from Kaggle.
2. **Preprocessing:** The data is loaded, features are separated from the target variable, and the `StandardScaler` is fitted to the training data to normalize feature values.
3. **Imbalance Handling:** The SMOTE algorithm is applied to the training set to create a balanced distribution of fraudulent and legitimate transactions, preventing bias towards the majority class.
4. **Model Training:** An XGBoost classifier is trained on the balanced, preprocessed data.
5. **Evaluation:** The trained model is evaluated on a completely unseen test set. Performance is measured using a classification report, confusion matrix, and **Area Under the Precision-Recall Curve (AUPRC)** — the most suitable metric for this imbalanced problem.
6. **Experiment Logging:** All hyperparameters, performance metrics (like Recall and AUPRC), and the resulting model/scaler files are logged to an MLflow experiment.
7. **Artifact Saving:** The final trained model (`xgb_fraud_detector.joblib`) and the fitted scaler (`scaler.joblib`) are saved to the `models/` directory for use in later phases.

---

## 4. Key Achievements

- **High-Performing Model:** The final model achieved an **89% recall** on the fraud class and a strong **AUPRC of 0.80**, demonstrating its effectiveness at the primary business goal of catching fraudsters.
- **Automated & Reproducible Pipeline:** The entire workflow, from data download to model saving, is encapsulated in a single script, ensuring consistency and ease of use.
- **Robust Experiment Tracking:** Integration with MLflow provides a professional and transparent way to view, compare, and manage different model training runs.

---

## 5. How to Run This Phase

The process is fully automated for simplicity.

1. Ensure your **Kaggle API credentials (`kaggle.json`)** are placed in the project's root directory.
2. From the project's root, make the script executable (one-time setup):

```bash
chmod +x run_phase1.sh
```

3. Execute the training pipeline:

```bash
./run_phase1.sh
```

4. After the run, you can view the detailed experiment logs by running:

```bash
mlflow ui
```

---

*End of Phase 1 report.*

