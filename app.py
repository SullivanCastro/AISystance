from flask import Flask, request, render_template
from models.model import int_to_flower, flower_to_int, fit_model
import pandas as pd
import joblib


# Declare a Flask app
app = Flask(__name__)


# Main function here
# ------------------
@app.route('/', methods=['GET', 'POST'])
def predict():
    # If a form is submitted
    if request.method == "POST":

        # Unpickle classifier
        clf = joblib.load("models/model.pkl")

        # Get values through input bars
        SL = request.form.get("SepalLength")
        SW = request.form.get("SepalWidth")
        PL = request.form.get("PetalLength")
        PW = request.form.get("PetalWidth")

        # Get prediction
        prediction = int_to_flower[clf.predict([[SL, SW, PL, PW]])[0]]

    else:
        prediction = ""

    return render_template("index.html", output=prediction)

@app.route('/database.html', methods=['GET', 'POST'])
def add_to_database():
    # If a form is submitted
    df = pd.read_pickle("models/database.pkl")

    if request.method == "POST":
        try:
            # Unpickle classifier
            clf = joblib.load("models/model.pkl")

            # Get values through input bars
            SL = request.form.get("SepalLength")
            SW = request.form.get("SepalWidth")
            PL = request.form.get("PetalLength")
            PW = request.form.get("PetalWidth")
            FN = request.form.get("FlowerName")

            # Get prediction
            df = pd.read_pickle("models/database.pkl")
            X = pd.DataFrame([[SL, SW, PL, PW, FN]], columns=df.columns)
            df = pd.concat([df, X])

            df.to_pickle("models/database.pkl")
            accuracy = fit_model(df, "models/model.pkl")
            prediction = "Added to the database"

        except Exception as e:
            print(f"The error {e} occured.")
            prediction = "An error occured"
            accuracy = fit_model(df, "models/model.pkl")

    else:
        prediction = "You haven't modified the dataset already."
        accuracy = fit_model(df, "models/model.pkl")

    return render_template("database.html", output=prediction, accuracy=accuracy)

# Running the app
if __name__ == '__main__':
    app.run(debug=True)