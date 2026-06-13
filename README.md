# 🩺 MediRisk 360 – Health Risk Prediction App

MediRisk 360 is a Streamlit web application that records basic lab results for patients and calls an external Flask **Health Risk API** to generate an AI-style health risk remark.  
This project was built as part of the **Junior AI/ML Developer task**.

🔗 **Live App (Streamlit Community Cloud)**  
https://medirisk-360-nuptfpokzkiwbzyqh8u3ul.streamlit.app/

🔗 **External Health Risk API (Flask on Render)**  
https://health-risk-api.onrender.com/predict  
(Used internally by the app; accepts POST requests with lab values.)

---

## 🚀 Features

- Add new patient records with:
  - Full name, date of birth, email address  
  - Glucose, haemoglobin, and cholesterol values  
- Automatic **risk assessment** using an external Flask Health Risk API (Low / Moderate / High)  
- Display of API-generated **Remarks** explaining which values are abnormal  
- View all saved patients in a table with colored risk indicators  
- ✏️ **Update** existing patient records  
- 🗑️ **Delete** patients when they are no longer needed  
- Persistent storage using a lightweight **SQLite** database (`patients.db`)  
- Clean, responsive UI built with Streamlit and custom CSS

---

## 🧰 Tech Stack

- 🐍 Python  
- 🧊 Streamlit – UI + application logic  
- 💾 SQLite – persistent local storage of patient records  
- 📊 Pandas – data handling  
- 🌐 Flask (separate repo) – external Health Risk API deployed on Render  
- 🔗 HTTP integration via `requests` – Streamlit calls the Flask API for predictions

---

## 🔗 Architecture Overview

- **Frontend**: Streamlit app (`app.py`) for CRUD operations and data validation.  
- **Backend API**: Flask service (`health-risk-api` repo) deployed on Render, exposing `/predict`.  
- When a valid patient record is saved or updated, the app sends a POST request to the Render API with `glucose`, `haemoglobin`, and `cholesterol`.  
- The API responds with a `risk_level` and a human-readable `remark`, which are stored and displayed in the **Remarks** column.

---

## 🧪 Running the App Locally

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/<your-streamlit-repo>.git
   cd <your-streamlit-repo>
   ```

2. **(Optional) Create and activate a virtual environment**

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the API URL**

   In `app.py`, make sure `API_URL` points to the deployed Flask API (for example):

   ```python
   API_URL = "https://health-risk-api.onrender.com/predict"
   ```

5. **Run the Streamlit app**

   ```bash
   streamlit run app.py
   ```

6. Open the URL shown in the terminal (usually `http://localhost:8501`) in your browser.

---

## 📁 Project Structure

```text
.
├── app.py           # Main Streamlit application (UI + API calls)
├── db.py            # Database helper functions (SQLite)
├── patients.db      # SQLite database file (sample / local data)
├── requirements.txt # Python dependencies
└── README.md        # Project documentation
```

The Flask Health Risk API lives in a separate repository (`health-risk-api`) and is deployed on Render.

---

## 👩‍💻 Author

**Afiga Begum**

- 📧 Email: afiga97@gmail.com  
- 🔗 LinkedIn: https://www.linkedin.com/in/afigabegum/

If you use or build on MediRisk 360, feel free to reach out or open an issue/PR.  
Contributions, suggestions, and feedback are always welcome!

---

## ⚠️ Disclaimer

- The health risk logic and API are **for educational/demo purposes only** and are **not** medical devices.  
- Do not use this app for real diagnosis or treatment decisions; always consult a qualified healthcare professional.
