from flask import Blueprint, request, render_template, redirect
from flask_security import roles_required
from flask_login import login_required, current_user
from project.models_ml.model import fit_random_forest
import pandas as pd
import joblib
import os
main = Blueprint('main', __name__)


################################################# LOGIN PAGE #################################################
@main.route('/', methods=['GET', 'POST'])
def home():
    return redirect("login.html")


############################################# RANDOM FOREST PAGE #############################################
@main.route('/index.html', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def predict():
    """
    The predict function receives the information through the form. Then the model makes a prediction
    and the pages is updated.
    """
    # Load the database
    database = joblib.load("project/models_ml/database.pkl")
    prediction = ""

    # Submit the columns names to the page
    columns = database.columns[:-1].tolist()

    # If a form is submitted
    if request.method == "POST":

        # Unpickle classifier
        model = joblib.load("project/models_ml/random_forest.pkl")

        # Get values through input bars
        input_values = []
        for column in columns:
            input_value = float(request.form[column])
            input_values.append(input_value)

        # Get prediction
        prediction = model.predict([input_values])

    # Update the page
    return render_template("index.html", columns=columns, output=prediction)

################################################## KNN PAGE ##################################################
@main.route('/knn.html', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def neighbor():
    """
    The predict function receives the information through the form. Then the model makes a prediction
    and the pages is updated.
    """
    # Load the database
    database = joblib.load("project/models_ml/database.pkl")

    # If a form is submitted
    if request.method == "POST":

        # Unpickle classifier
        model = joblib.load("project/models_ml/knn.pkl")

        # Get values through input bars
        input_values = []
        for column in database[:-1].columns:
            input_value = float(request.form[column])
            input_values.append(input_value)

        # Get prediction
        prediction = model.predict([input_values])

    else:
        prediction = ""

    # Submmit the columns names to the page
    columns = database.columns[:-1].tolist()

    # Update the page
    return render_template("index.html", columns=columns, output=prediction)


############################################# DATABASE PAGE #############################################
@main.route('/database.html', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def add_to_database():
    # Load the database
    database = joblib.load("project/models_ml/database.pkl")

    if request.method == "POST":
        try:
            # Get values through input bars and initiate the new element
            new_element = {
                column: request.form[column] for column in database.columns
            }

            # Create a DataFrame with the same column than the database
            database = database.append(new_element, ignore_index=True)

            # Save the database
            database.to_pickle("project/models_ml/database.pkl")

            # Train the model and measure the new performance
            accuracy = fit_random_forest(database, "project/models_ml/")
            prediction = "Added to the database"

        except Exception as e:
            print(f"The error {e} occured.")
            prediction = "An error occured"
            accuracy = fit_random_forest(database, "project/models_ml/")

    else:
        prediction = "You haven't modified the dataset already."
        accuracy = fit_random_forest(database, "project/models_ml/")

    # Submit the columns names to the page
    columns = database.columns.tolist()

    # Update the page
    return render_template("database.html", columns=columns, output=prediction, accuracy=accuracy)


################################################# LOOK UP #################################################
@main.route('/lookup.html', methods=['GET', 'POST'])
@login_required
def see_dataset():
    # Load the database
    database = joblib.load("project/models_ml/database.pkl")

    elements = []
    selected_string_column = False
    selected_num_column = False
    data = database

    if request.method=="POST":
        selected_string_column = request.form.get('StringColumns')
        selected_num_column = request.form.get('NumColumns')
        filtered_string_element = request.form.get('FilteredElement')
        lower_bound = request.form.get('LowerBound')
        upper_bound = request.form.get('UpperBound')

        # Query the database according the string criteria
        if selected_string_column != 'None':
            elements = database[selected_string_column].unique().tolist()
            if filtered_string_element!='None':
                data = data[data[selected_string_column] == filtered_string_element]

        # Query the database according the numerical criteria
        if selected_num_column!='None':
            elements = database[selected_num_column].unique().tolist()
            if lower_bound!='' and upper_bound!='':
                data = data[(data[selected_num_column] >= float(lower_bound)) & (database[selected_num_column] <= float(upper_bound))]
            

        # Convert filtered data into html
        data = data
    
    if request.method=="GET":
        selected_string_column = request.args.get('StringColumns')
        if selected_string_column is not None:
            elements = data[selected_string_column].unique().tolist()



    # Submit the columns names to the page
    string_columns = database.select_dtypes(include=['object']).columns.tolist() 
    num_columns = database.select_dtypes(include=['float64', 'int64']).columns.tolist()

    # Update the page
    return render_template('lookup.html',
                           selected_string_column=selected_string_column,
                           selected_num_column=selected_num_column, 
                           string_columns=string_columns, 
                           num_columns=num_columns,
                           elements=elements, 
                           data=data.to_html()
                        )
