import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import joblib


int_to_flower = {'0': 'setosa', '1': 'versicolor', '2': 'virginica'}
flower_to_int = dict(zip(int_to_flower.values(), int_to_flower.keys()))


def fit_model(df, path):
    # Sélectionner les features et la target
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1].replace(flower_to_int)

    # Diviser les données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Initialiser un modèle SVM avec un noyau linéaire
    model = SVC(kernel='linear', C=1)

    # Entraîner le modèle sur l'ensemble d'entraînement
    model.fit(X_train, y_train)

    # Prédire les classes pour l'ensemble de test
    y_pred = model.predict(X_test)

    # Calculer la précision (accuracy) du modèle
    accuracy = accuracy_score(y_test, y_pred)

    joblib.dump(model, path)

    return accuracy

if __name__ == "__main__":
    # Charger les données depuis l'URL
    df = pd.read_pickle("./database.pkl")
    print(f"Précision du modèle : {fit_model(df, 'model.pkl')}")
