import os
from flask import Blueprint, request, render_template, redirect
from project.models_ml.model import int_to_flower, flower_to_int, fit_model
import pandas as pd
from flask_login import login_required
import joblib

main = Blueprint('main', __name__)


################################################# LOGIN PAGE #################################################
@main.route('/', methods=['GET', 'POST'])
def home():
    return redirect("login.html")


############################################# RANDOM FOREST PAGE #############################################
@main.route('/index.html', methods=['GET', 'POST'])
@login_required
def predict():
    """
    The predict function receives the information through the form. Then the model makes a prediction
    and the pages is updated.
    """
    # If a form is submitted
    if request.method == "POST":

        # Unpickle classifier
        model = joblib.load("models_ml/model.pkl")

        # Get values through input bars
        SL = request.form.get("SepalLength")
        SW = request.form.get("SepalWidth")
        PL = request.form.get("PetalLength")
        PW = request.form.get("PetalWidth")

        # Get prediction
        prediction = int_to_flower[model.predict([[SL, SW, PL, PW]])[0]]

    else:
        prediction = ""

    return render_template("index.html", output=prediction)


############################################# DATABASE PAGE #############################################
@main.route('/database.html', methods=['GET', 'POST'])
@login_required
def add_to_database():
    # Load the database
    database = pd.read_pickle("models_ml/database.pkl")
    SL, SW, PL, PW, FN = database.columns

    if request.method == "POST":
        try:
            # Get values through input bars and initiate the new element
            new_element = {
                SL: request.form.get("SepalLength"),
                SW: request.form.get("SepalWidth"),
                PL: request.form.get("PetalLength"),
                PW: request.form.get("PetalWidth"),
                FN: request.form.get("FlowerName")
            }

            # Create a DataFrame with the same column than the database
            database = database.append(new_element, ignore_index=True)

            # Save the database
            database.to_pickle("models_ml/database.pkl")

            # Train the model and measure the new performance
            accuracy = fit_model(database, "models_ml/model.pkl")
            prediction = "Added to the database"

        except Exception as e:
            print(f"The error {e} occured.")
            prediction = "An error occured"
            accuracy = fit_model(database, "models_ml/model.pkl")

    else:
        prediction = "You haven't modified the dataset already."
        accuracy = fit_model(database, "models_ml/model.pkl")

    # Update the page
    return render_template("database.html", output=prediction, accuracy=accuracy)

################################################# LOOK UP #################################################
@main.route('/lookup.html', methods=['GET', 'POST'])
@login_required
def see_dataset():
    df = pd.read_pickle('models_ml/database.pkl')
    first_30_rows = df.head(30)
    return render_template('lookup.html', data=first_30_rows.to_html())