import streamlit as st
import pandas as pd
from datetime import date
import re
import random
import requests

from db import (
    create_table,
    get_all_patients,
    get_patient_by_id,
    update_patient,
    delete_patient,
)

# URL of your Flask prediction API
API_URL = "http://127.0.0.1:8000/predict"

# Initialize database
create_table()

# ------------------ Global CSS for larger fonts & spacing ------------------


def inject_global_css():
    st.markdown(
        """
        <style>
        html, body, [class*="css"]  {
            font-size: 18px !important;
        }
        /* Top padding so the title isn't cut but still close to top */
        .block-container {
            padding-top: 1.0rem !important;
        }
        .stMarkdown, .stText, .stMetric, .stDataFrame, .stSelectbox, .stButton, label {
            font-size: 18px !important;
        }
        h1 {
            font-size: 40px !important;
            margin-top: 0.5rem !important;
            margin-bottom: 0.25rem !important;
        }
        h2 {
            font-size: 32px !important;
            margin-top: 0.5rem !important;
            margin-bottom: 0.25rem !important;
        }
        h3 {
            font-size: 26px !important;
            margin-top: 0.25rem !important;
            margin-bottom: 0.25rem !important;
        }
        /* Make the disclaimer a bit narrower and centered */
        .disclaimer-box {
            max-width: 900px;
            margin-left: auto;
            margin-right: auto;
        }
        /* Narrow content slightly for better focus on large screens */
        .main-content-narrow {
            max-width: 1100px;
            margin-left: auto;
            margin-right: auto;
        }
        /* Sidebar branding */
        .sidebar-title {
            font-weight: 600;
            font-size: 18px;
            padding-bottom: 0.25rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ------------------ Health tips ------------------


HEALTH_TIPS = [
    "Drink at least 6–8 glasses of water a day to stay hydrated.",
    "Aim for at least 30 minutes of moderate physical activity most days.",
    "Include colorful fruits and vegetables in your meals for a variety of nutrients.",
    "Limit sugary drinks and ultra-processed snacks to protect your metabolic health.",
    "Try to sleep 7–9 hours per night to support overall wellbeing.",
    "Avoid smoking and limit alcohol for better heart and lung health.",
    "Schedule regular health check-ups, even when you feel well.",
    "Practice portion control and eat slowly to avoid overeating.",
    "Take short breaks to stretch if you sit for long periods during the day.",
    "Wash your hands regularly to reduce the spread of infections.",
    "Manage stress with deep breathing, meditation, or a relaxing hobby.",
    "Choose whole grains over refined grains for better blood sugar control.",
    "Add lean protein sources such as beans, lentils, fish, or eggs to your diet.",
    "Limit salt intake to help maintain healthy blood pressure levels.",
    "Use stairs instead of elevators when possible to add extra movement.",
    "Keep a record of your blood pressure, sugar, and cholesterol if you are at risk.",
    "Wear comfortable footwear and support your joints during exercise.",
    "Avoid screens at least 30 minutes before bedtime to improve sleep quality.",
    "Stay connected with friends and family to support your mental health.",
    "If something about your health worries you, talk to a healthcare professional early.",
]


def get_random_health_tip() -> str:
    return random.choice(HEALTH_TIPS)


# ------------------ Validation + styling helpers ------------------


def validate_email(email: str) -> bool:
    # Simple email pattern check
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


# Color for remarks column in dataframe (low / moderate / high)


def color_risk(val: str):
    if isinstance(val, str):
        if "High risk" in val:
            return "background-color: #ff4d4f; color: white;"   # red
        elif "Moderate risk" in val:
            return "background-color: #ffa500; color: black;"   # orange
        elif "Low risk" in val:
            return "background-color: #28a745; color: white;"   # green
    return ""


def style_remarks_column(col: pd.Series):
    if col.name == "remarks":
        return col.map(color_risk)
    return [""] * len(col)


# ------------------ Add patient form ------------------


def show_add_patient_form():
    st.markdown('<div class="main-content-narrow">', unsafe_allow_html=True)

    st.markdown("### 🧑‍⚕️ Add New Patient")

    full_name = st.text_input("Full Name")
    dob = st.date_input(
        "Date of Birth",
        value=date(2000, 1, 1),
        min_value=date(1940, 1, 1),
        max_value=date.today(),
    )
    email = st.text_input("Email Address")

    col1, col2, col3 = st.columns(3)
    with col1:
        glucose = st.number_input("Glucose", min_value=0.0, step=1.0)
    with col2:
        haemoglobin = st.number_input("Haemoglobin", min_value=0.0, step=0.1)
    with col3:
        cholesterol = st.number_input("Cholesterol", min_value=0.0, step=1.0)

    if st.button("Save Patient"):
        errors = []
        today = date.today()

        if not full_name.strip():
            errors.append("Full name is required.")
        if dob > today:
            errors.append("Date of birth cannot be in the future.")
        if not validate_email(email):
            errors.append("Please enter a valid email address.")

        if glucose <= 0 or haemoglobin <= 0 or cholesterol <= 0:
            errors.append("All lab values must be greater than zero.")

        if errors:
            for e in errors:
                st.error(e)
        else:
            # Call external Flask AI/ML API
            payload = {
                "glucose": float(glucose),
                "haemoglobin": float(haemoglobin),
                "cholesterol": float(cholesterol),
            }

            try:
                response = requests.post(API_URL, json=payload, timeout=5)
                response.raise_for_status()
                pred = response.json()
                remarks = pred.get("remark", "No remark from AI API")
            except Exception as e:
                st.error(f"Failed to get prediction from AI API: {e}")
                st.stop()

            from db import add_patient  # local import to avoid circular import

            add_patient(
                full_name=full_name.strip(),
                dob=str(dob),
                email=email.strip(),
                glucose=float(glucose),
                haemoglobin=float(haemoglobin),
                cholesterol=float(cholesterol),
                remarks=remarks,
            )
            st.success("Patient saved successfully!")
            st.info(f"Generated remark: {remarks}")

    st.markdown("</div>", unsafe_allow_html=True)


# ------------------ View / update / delete ------------------


def show_patient_table():
    st.markdown('<div class="main-content-narrow">', unsafe_allow_html=True)

    st.markdown("### 📋 All Patients")
    rows = get_all_patients()
    if not rows:
        st.info("No patient records yet.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    df = pd.DataFrame(
        rows,
        columns=[
            "id",
            "full_name",
            "dob",
            "email",
            "glucose",
            "haemoglobin",
            "cholesterol",
            "remarks",
        ],
    )

    # Ensure numeric and round values
    for col in ["glucose", "haemoglobin", "cholesterol"]:
        df[col] = df[col].astype(float).round(2)

    # Apply colors to the remarks column and format floats to 2 decimals
    styled_df = (
        df.style
        .apply(style_remarks_column, axis=0)
        .format({
            "glucose": "{:.2f}",
            "haemoglobin": "{:.2f}",
            "cholesterol": "{:.2f}",
        })
    )

    st.dataframe(styled_df, use_container_width=True)

    st.markdown("---")
    st.subheader("Edit or Delete a Patient")

    # Select patient by ID
    patient_ids = df["id"].tolist()
    selected_id = st.selectbox("Select Patient ID", patient_ids)

    if selected_id is not None:
        patient = get_patient_by_id(int(selected_id))
        if patient:
            (
                pid,
                full_name_init,
                dob_init,
                email_init,
                glucose_init,
                haemoglobin_init,
                cholesterol_init,
                remarks_init,
            ) = patient

            tab1, tab2 = st.tabs(["Update", "Delete"])

            # ---------- UPDATE TAB ----------
            with tab1:
                st.write("Update selected patient:")

                with st.form(key=f"update_form_{pid}"):
                    full_name = st.text_input("Full Name", value=full_name_init)
                    dob = st.date_input(
                        "Date of Birth",
                        value=date.fromisoformat(dob_init),
                        min_value=date(1940, 1, 1),
                        max_value=date.today(),
                    )
                    email = st.text_input("Email Address", value=email_init)

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        glucose = st.number_input(
                            "Glucose",
                            min_value=0.0,
                            step=1.0,
                            value=float(glucose_init),
                        )
                    with col2:
                        haemoglobin = st.number_input(
                            "Haemoglobin",
                            min_value=0.0,
                            step=0.1,
                            value=float(haemoglobin_init),
                        )
                    with col3:
                        cholesterol = st.number_input(
                            "Cholesterol",
                            min_value=0.0,
                            step=1.0,
                            value=float(cholesterol_init),
                        )

                    submitted = st.form_submit_button("Update Patient")

                if submitted:
                    errors = []
                    today = date.today()

                    if not full_name.strip():
                        errors.append("Full name is required.")
                    if dob > today:
                        errors.append("Date of birth cannot be in the future.")
                    if not validate_email(email):
                        errors.append("Please enter a valid email address.")
                    if glucose <= 0 or haemoglobin <= 0 or cholesterol <= 0:
                        errors.append("All lab values must be greater than zero.")

                    if errors:
                        for e in errors:
                            st.error(e)
                    else:
                        # Check if anything actually changed
                        nothing_changed = (
                            full_name.strip() == full_name_init
                            and str(dob) == dob_init
                            and email.strip() == email_init
                            and float(glucose) == float(glucose_init)
                            and float(haemoglobin) == float(haemoglobin_init)
                            and float(cholesterol) == float(cholesterol_init)
                        )

                        if nothing_changed:
                            st.warning(
                                "No changes detected. Please modify some values before updating."
                            )
                        else:
                            # Call external Flask AI/ML API on updated values
                            payload = {
                                "glucose": float(glucose),
                                "haemoglobin": float(haemoglobin),
                                "cholesterol": float(cholesterol),
                            }

                            try:
                                response = requests.post(API_URL, json=payload, timeout=5)
                                response.raise_for_status()
                                pred = response.json()
                                new_remarks = pred.get("remark", "No remark from AI API")
                            except Exception as e:
                                st.error(f"Failed to get prediction from AI API: {e}")
                                st.stop()

                            update_patient(
                                patient_id=pid,
                                full_name=full_name.strip(),
                                dob=str(dob),
                                email=email.strip(),
                                glucose=float(glucose),
                                haemoglobin=float(haemoglobin),
                                cholesterol=float(cholesterol),
                                remarks=new_remarks,
                            )
                            st.success("Patient updated successfully!")
                            st.info(f"Updated remark: {new_remarks}")

            # ---------- DELETE TAB ----------
            with tab2:
                st.write("Delete selected patient:")
                st.warning(
                    "This will permanently delete the record for "
                    f"**{full_name_init}** (ID {pid})."
                )
                if st.button("Delete Patient"):
                    delete_patient(pid)
                    st.success("Patient deleted successfully!")

    st.markdown("</div>", unsafe_allow_html=True)


# ------------------ Main layout ------------------


def main():
    st.set_page_config(page_title="MediRisk 360", page_icon="🩺", layout="wide")

    # Inject global CSS for bigger fonts and adjusted top gap
    inject_global_css()

    # Centered title + subtitle + intro
    st.markdown(
        """
        <div style="text-align: center; margin-top: 0.25rem;">
            <h1>MediRisk 360</h1>
            <h3>Simple labs, smart risk insights.</h3>
            <p>
            This app allows you to add patient blood test details, store them in a database,
            and generate an AI-powered remark from an external prediction API that estimates health risk.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Disclaimer in a narrower, centered box
    st.markdown('<div class="disclaimer-box">', unsafe_allow_html=True)
    st.info(
        "Disclaimer: This tool is for educational and demonstration purposes only. "
        "It is not a medical device and must not be used for diagnosis or treatment. "
        "Always consult a qualified healthcare professional for medical advice."
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Sidebar navigation with small branded title
    st.sidebar.markdown(
        '<div class="sidebar-title">🩺 MediRisk 360</div>',
        unsafe_allow_html=True,
    )
    menu = ["Home", "Add Patient", "View Patients"]
    choice = st.sidebar.selectbox("Navigation", menu)

    if choice == "Home":
        st.markdown('<div class="main-content-narrow">', unsafe_allow_html=True)

        st.subheader("Home")
        st.write("Use the sidebar to add new patients or view stored records.")

        rows = get_all_patients()
        total_patients = len(rows)
        high_risk = sum(1 for r in rows if r[7] and "High risk" in r[7])
        moderate_risk = sum(1 for r in rows if r[7] and "Moderate risk" in r[7])
        low_risk = sum(1 for r in rows if r[7] and "Low risk" in r[7])

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total patients", total_patients)
        with col2:
            st.metric("High risk", high_risk)
        with col3:
            st.metric("Moderate risk", moderate_risk)
        with col4:
            st.metric("Low risk", low_risk)

        st.markdown("---")
        st.markdown(
            """
            **How it works**

            - Enter patient details and lab values on the *Add Patient* page.  
            - The app validates the data and calls an external Flask-based AI prediction API.  
            - The generated risk remark is stored in the database and shown in the table.  
            - You can update or delete records at any time from the *View Patients* page.
            """
        )

        st.markdown("---")
        st.markdown("### 💡 Health Tip of the Moment")
        st.success(get_random_health_tip())

        st.markdown("</div>", unsafe_allow_html=True)

    elif choice == "Add Patient":
        show_add_patient_form()
    elif choice == "View Patients":
        show_patient_table()


if __name__ == "__main__":
    main()