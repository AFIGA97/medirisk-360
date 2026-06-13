from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow calls from Streamlit

# Adjust these ranges if you want
GLUCOSE_MIN, GLUCOSE_MAX = 70, 140
HB_MIN, HB_MAX = 12, 16
CHOL_MIN, CHOL_MAX = 125, 200


def build_risk_and_remark(glucose: float, haemoglobin: float, cholesterol: float):
    abnormal = []

    if not (GLUCOSE_MIN <= glucose <= GLUCOSE_MAX):
        abnormal.append("glucose")
    if not (HB_MIN <= haemoglobin <= HB_MAX):
        abnormal.append("haemoglobin")
    if not (CHOL_MIN <= cholesterol <= CHOL_MAX):
        abnormal.append("cholesterol")

    n = len(abnormal)

    if n == 0:
        risk = "Low"
        remark = "Low risk: All lab values are within approximate normal ranges."
    elif n == 1:
        risk = "Moderate"
        remark = (
            f"Moderate risk: Abnormal {abnormal[0]} level detected. "
            "Please monitor and consult a healthcare professional if needed."
        )
    else:
        # Build a readable list: "glucose and cholesterol" or "glucose, haemoglobin and cholesterol"
        if n == 2:
            names = " and ".join(abnormal)
        else:
            names = ", ".join(abnormal[:-1]) + f" and {abnormal[-1]}"

        risk = "High"
        remark = (
            f"High risk: Abnormal {names} levels detected. "
            "Please consult a healthcare professional as soon as possible."
        )

    return risk, remark


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True)

    try:
        glucose = float(data["glucose"])
        haemoglobin = float(data["haemoglobin"])
        cholesterol = float(data["cholesterol"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Invalid or missing input values"}), 400

    risk_level, remark = build_risk_and_remark(glucose, haemoglobin, cholesterol)

    return jsonify({
        "risk_level": risk_level,
        "remark": remark
    })


if __name__ == "__main__":
    # Run on port 8000 so it's easy to remember
    app.run(host="127.0.0.1", port=8000, debug=True)