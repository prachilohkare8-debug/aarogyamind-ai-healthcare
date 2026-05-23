from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

import numpy as np
import joblib

app = Flask(__name__)
CORS(app)

# LOAD MODEL FILES

model = joblib.load("model/disease_model.pkl")
symptoms_list = joblib.load("model/symptoms.pkl")
encoder = joblib.load("model/encoder.pkl")

# PRECAUTIONS DATABASE

PRECAUTIONS = {

    "COVID-19": {

        "foods": [
            "Warm soup",
            "Vitamin C fruits",
            "Protein rich food"
        ],

        "avoid": [
            "Cold drinks",
            "Junk food"
        ],

        "tips": [
            "Take rest",
            "Drink water",
            "Wear mask"
        ]
    },

    "Diabetes": {

        "foods": [
            "Oats",
            "Vegetables",
            "Brown rice"
        ],

        "avoid": [
            "Sugar",
            "Soft drinks"
        ],

        "tips": [
            "Exercise daily",
            "Monitor sugar level"
        ]
    }

}

# HOME PAGE

@app.route("/")
def home():

    return render_template(
        "index.html",
        symptoms=symptoms_list
    )

# DASHBOARD PAGE

@app.route("/dashboard")
def dashboard():

    return render_template(
        "dashboard.html"
    )

# CHATBOT PAGE

@app.route("/chatbot")
def chatbot():

    return """
    <h1 style='font-family:sans-serif'>
    AI Chatbot Coming Soon
    </h1>
    """

# DISEASE LIST PAGE

@app.route("/diseases")
def diseases():

    diseases = encoder.classes_

    return render_template(
        "diseases.html",
        diseases=diseases
    )

# PREDICTION API

@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        symptoms = data["symptoms"]

        if len(symptoms) == 0:

            return jsonify({
                "error": "No symptoms selected"
            })

        input_data = []

        for symptom in symptoms_list:

            if symptom in symptoms:
                input_data.append(1)
            else:
                input_data.append(0)

        input_data = np.array(input_data).reshape(1, -1)

        probabilities = model.predict_proba(input_data)[0]

        top_indices = np.argsort(probabilities)[::-1][:3]

        top_predictions = []

        for index in top_indices:

            disease = encoder.inverse_transform([index])[0]

            confidence = round(
                probabilities[index] * 100,
                2
            )

            top_predictions.append({

                "disease": disease,

                "confidence": confidence,

                "severity": "Moderate",

                "category": "General",

                "treatment":
                "Consult doctor if symptoms continue."

            })

        return jsonify({

            "prediction": top_predictions[0],

            "top_predictions": top_predictions

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })

# PRECAUTIONS PAGE

@app.route("/precautions/<disease>")
def precautions(disease):

    data = PRECAUTIONS.get(

        disease,

        {
            "foods": ["Healthy food"],

            "avoid": ["Junk food"],

            "tips": ["Take proper rest"]
        }

    )

    return render_template(

        "precautions.html",

        disease=disease,

        data=data
    )

# BMI API

@app.route("/calculate_bmi", methods=["POST"])
def calculate_bmi():

    try:

        data = request.get_json()

        weight = float(data["weight"])
        height = float(data["height"])

        bmi = weight / ((height / 100) ** 2)

        bmi = round(bmi, 2)

        if bmi < 18.5:
            category = "Underweight"

        elif bmi < 25:
            category = "Normal"

        elif bmi < 30:
            category = "Overweight"

        else:
            category = "Obese"

        meal_plans = {

            "Underweight": {

                "breakfast":
                "Banana shake + oats",

                "lunch":
                "Rice + chicken",

                "dinner":
                "Paneer + chapati"
            },

            "Normal": {

                "breakfast":
                "Eggs + toast",

                "lunch":
                "Rice + vegetables",

                "dinner":
                "Soup + chapati"
            },

            "Overweight": {

                "breakfast":
                "Green tea + oats",

                "lunch":
                "Grilled vegetables",

                "dinner":
                "Salad + soup"
            },

            "Obese": {

                "breakfast":
                "Fruit bowl",

                "lunch":
                "Boiled vegetables",

                "dinner":
                "Light soup"
            }
        }

        return jsonify({

            "bmi": bmi,

            "category": category,

            "meal_plan":
            meal_plans[category]

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })

if __name__ == "__main__":

    app.run(debug=True)