import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import joblib


int_to_flower = {'0': 'setosa', '1': 'versicolor', '2': 'virginica'}
flower_to_int = dict(zip(int_to_flower.values(), int_to_flower.keys()))


def fit_model(database, path):
    """
    Train the model and update the weights
    """
    # Select features and targets
    X = database.iloc[:, :-1]
    y = database.iloc[:, -1].replace(flower_to_int)

    # Divide the data in train and test dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Load the model
    model = SVC(kernel='linear', C=1)

    # Train the model
    model.fit(X_train, y_train)

    # Measure the performance on the test set
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    # Save the model
    joblib.dump(model, path)

    return accuracy


if __name__ == "__main__":
    database = pd.read_pickle("./database.pkl")
    print(f"Précision du modèle : {fit_model(database, 'model.pkl')}")
