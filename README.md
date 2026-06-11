# 🩺 MediRisk 360 – Health Risk Prediction App

MediRisk 360 is a Streamlit web application that records basic lab results for patients and generates a simple rule‑based health risk remark.  
This project was built as part of the **Junior AI/ML Developer task**. ✨

🔗 **Live App:**  
[https://medirisk-360-nuptfpokzkiwbzyqh8u3ul.streamlit.app/](https://medirisk-360-nuptfpokzkiwbzyqh8u3ul.streamlit.app/)

---

## 🚀 Features

- Add new patient records with:
  - Full name, date of birth, email  
  - Glucose, haemoglobin, and cholesterol values  
- Automatic **risk assessment** using a simple rule‑based model (Low / Moderate / High risk)  
- View all saved patients in a table with colored risk indicators  
- ✏️ **Update** existing patient records  
- 🗑️ **Delete** patients when they are no longer needed  
- Lightweight **SQLite** database (`patients.db`) for persistent storage  
- Clean, responsive UI built with Streamlit and custom CSS

---

## 🧰 Tech Stack

- 🐍 Python  
- 🧊 Streamlit (UI + backend)  
- 💾 SQLite (persistent storage)  
- 📊 Pandas for data handling  
- ⚖️ Simple rule‑based logic for risk estimation

---

## 🧪 Running the App Locally

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username/<your-repo-name>.git
   cd <your-repo-name>
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

4. **Run the Streamlit app**

   ```bash
   streamlit run app.py
   ```

5. Open the URL shown in the terminal (usually `http://localhost:8501`) in your browser. 🌐

---

## 📁 Project Structure

```text
.
├── app.py           # Main Streamlit application
├── db.py            # Database helper functions (SQLite)
├── patients.db      # SQLite database file (sample data)
├── requirements.txt # Python dependencies
└── README.md        # Project documentation
```

---

## 👩‍💻 Author

**Afiga**

- 📧 Email: afiga97@gmail.com  
- 🔗 LinkedIn: https://www.linkedin.com/in/afigabegum/

If you use or build on MediRisk 360, feel free to reach out or open an issue/PR.  
Contributions, suggestions, and feedback are always welcome! 💬✨

---

## ⚠️ Disclaimer

- The health risk logic is **for educational/demo purposes only** and is **not** a medical device.  
- Do not use this app for real diagnosis or treatment decisions; always consult a qualified healthcare professional. 🩺
