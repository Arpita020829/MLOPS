from pathlib import Path
import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,precision_score,recall_score

import mlflow
import mlflow.sklearn

#Configure mlflow tracking
# MLFlow server store experiment metadata and model records 
mlflow.set_tracking_uri("http://127.0.0.1:6001")

# Group related training runs under one experiment 
mlflow.set_experiment("iris-classification")

iris = load_iris()
X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(X, 
                                                    y, 
                                                    test_size=0.2, 
                                                    random_state=42)
n_estimators =100
random_state=42

#model settings we want to track in mlflow
model_params={
    "model_type":"RandomForestClassifier",
    "n_estimators":n_estimators,
    "random_state":random_state,
    "test_size":0.2
}

#start a tracked training run
with mlflow.start_run() as run:
    #record the training configuration beg=fore model fitting
    mlflow.log_params(model_params)

    #build classifier using selected params
    model=RandomForestClassifier(
        n_estimators=n_estimators,
        random_state=random_state)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision= precision_score(y_test,y_pred,average="macro",zero_division=0)
    recall= recall_score(y_test,y_pred,average="macro",zero_division=0)

    #log the evaluated results so that different runs can be compared
    mlflow.log_metrics({
        "test_accuracy":accuracy,
        "test_precision":precision,
        "test_recall":recall
    })
    print("MLFlow run ID:",run.info.run_id)
    print("Test Accuracy",accuracy)
    print("Test Precision",precision)
    print("Test Recall",recall)


# model = RandomForestClassifier(random_state=42)
# model.fit(X_train, y_train)
# y_pred = model.predict(X_test)
# accuracy = accuracy_score(y_test, y_pred)
# print(f"Accuracy: {accuracy}")

# Save the trained model as reusable artifact
model_dir = Path("models")
model_dir.mkdir(parents=True, exist_ok=True)
joblib.dump(model, model_dir / "iris_model.joblib")
print(f"Model saved to {model_dir / 'iris_model.joblib'}")

mlflow.sklearn.log_model(
    sk_model=model,
    name="iris-model",
    registered_model_name="iris-classifier",
    skops_trusted_types=[
        "sklearn.tree._tree.Tree"
    ]
)
print("Registered Model: iris-classifier")