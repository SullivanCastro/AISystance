from flask import Flask, request, render_template
from models.model import int_to_flower, flower_to_int, fit_model
import pandas as pd
import joblib


# Declare a Flask app
app = Flask(__name__)


############################################# HOME PAGE #############################################
@app.route('/', methods=['GET', 'POST'])
def predict():
    """
    The predict function receives the information through the form. Then the model makes a prediction
    and the pages is updated.
    """
    # If a form is submitted
    if request.method == "POST":

        # Unpickle classifier
        model = joblib.load("models/model.pkl")

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
@app.route('/database.html', methods=['GET', 'POST'])
def add_to_database():
    # Load the database
    database = pd.read_pickle("models/database.pkl")

    if request.method == "POST":
        try:
            # Get values through input bars and initiate the new element
            new_element = {
                'SL': request.form.get("SepalLength"),
                'SW': request.form.get("SepalWidth"),
                'PL': request.form.get("PetalLength"),
                'PW': request.form.get("PetalWidth"),
                'FN': request.form.get("FlowerName")
            }

            # Create a DataFrame with the same column than the database
            database = database.append(new_element, ignore_index=True)

            # Save the database
            database.to_pickle("models/database.pkl")

            # Train the model and measure the new performance
            accuracy = fit_model(database, "models/model.pkl")
            prediction = "Added to the database"

        except Exception as e:
            print(f"The error {e} occured.")
            prediction = "An error occured"
            accuracy = fit_model(database, "models/model.pkl")

    else:
        prediction = "You haven't modified the dataset already."
        accuracy = fit_model(database, "models/model.pkl")

    # Update the page
    return render_template("database.html", output=prediction, accuracy=accuracy)

# Running the app
if __name__ == '__main__':
    app.run(debug=True)