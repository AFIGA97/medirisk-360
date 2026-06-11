import sqlite3
from typing import List, Tuple, Optional

DB_NAME = "patients.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    return conn


def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            dob TEXT NOT NULL,
            email TEXT NOT NULL,
            glucose REAL NOT NULL,
            haemoglobin REAL NOT NULL,
            cholesterol REAL NOT NULL,
            remarks TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def add_patient(full_name: str, dob: str, email: str,
                glucose: float, haemoglobin: float,
                cholesterol: float, remarks: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO patients (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks),
    )
    conn.commit()
    conn.close()


def get_all_patients() -> List[Tuple]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_patient_by_id(patient_id: int) -> Optional[Tuple]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    row = cur.fetchone()
    conn.close()
    return row


def update_patient(patient_id: int, full_name: str, dob: str, email: str,
                   glucose: float, haemoglobin: float,
                   cholesterol: float, remarks: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE patients
        SET full_name = ?, dob = ?, email = ?,
            glucose = ?, haemoglobin = ?, cholesterol = ?, remarks = ?
        WHERE id = ?
        """,
        (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks, patient_id),
    )
    conn.commit()
    conn.close()


def delete_patient(patient_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
    conn.commit()
    conn.close()