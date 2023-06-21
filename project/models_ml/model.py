import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
import joblib


def fit_random_forest(database: pd.DataFrame, path: str) -> float:
    """
    Train the model and update the weights
    :param database: the path to database to use
    :param path: the path to save the model
    """
    # Pre-processing of the DataFrame
    dict_one_hot_encoder = {} # for a string column, dict_one_hot_encoder contains the correspondance between the encoded categories and the original categories
    for string_column in database.select_dtypes(include=['object']).columns: # One Hot Encoder generalized
        label_encoder = LabelEncoder()
        encoded_categories = label_encoder.fit_transform(database[string_column])
        database[string_column] = encoded_categories
        dict_one_hot_encoder[string_column] = label_encoder.classes_

    # Save the dict_one_hot_encoder
    joblib.dump(dict_one_hot_encoder, path+'dict_one_hot_encoder.pkl')

    # Select features and targets
    X = database.iloc[:, :-1] # all features (not determined yet)
    y = database.iloc[:, -1] # all targets (not determined yet)

    # Load the model
    model = RandomForestRegressor() # Support Vector Classifier Machine Learning model

    # Cross-validation to seek the best hyperparameters
    param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 5, 10],
    'min_samples_split': [2, 5, 10]
    }
    grid_search = GridSearchCV(model, param_grid, cv=2)
    grid_search.fit(X, y)

    # Update the model with the best hyperparameters
    model = grid_search.best_estimator_
    score = grid_search.best_score_

    # Save the model
    joblib.dump(model, path+'random_forest.pkl')

    return score

def fit_knn(database: pd.DataFrame, path: str) -> float:
    """
    Train the model and update the weights
    :param database: the path to database to use
    :param path: the path to save the model
    """

    # Pre-processing of the DataFrame
    dict_one_hot_encoder = {} # for a string column, dict_one_hot_encoder contains the correspondance between the encoded categories and the original categories
    for string_column in database.select_dtypes(include=['object']).columns: # One Hot Encoder generalized
        label_encoder = LabelEncoder()
        encoded_categories = label_encoder.fit_transform(database[string_column])
        database[string_column] = encoded_categories
        dict_one_hot_encoder[string_column] = label_encoder.classes_

    # Select features and targets
    X = database.iloc[:, :-1]  # all features (not determined yet)
    y = database.iloc[:, -1]  # all targets (not determined yet)

    # Load the model
    model = KNeighborsRegressor()  # k-NN (k-Nearest Neighbors) model

    # Cross-validation to find the best hyperparameters
    param_grid = {
        'n_neighbors': [3, 5, 7],
        'weights': ['uniform', 'distance']
    }
    grid_search = GridSearchCV(model, param_grid, cv=2)
    grid_search.fit(X, y)

    # Update the model with the best hyperparameters
    model = grid_search.best_estimator_
    score = grid_search.best_score_

    # Save the model
    joblib.dump(model, path + 'knn.pkl')

    return score


if __name__ == "__main__":
    database = pd.read_pickle("./project/models_ml/database.pkl")
    print(f"Précision du Random Forest : {fit_random_forest(database, './project/models_ml/')}")
    print(f"Précision du KNN : {fit_knn(database, './project/models_ml/')}")
