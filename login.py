import streamlit as st
import sqlite3
from patient_interface import patient_interface
from doctor_interface import doctor_interface


def get_db_connection():
    conn = sqlite3.connect('health_monitoring.db')
    return conn

def authenticate_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    

    cursor.execute("SELECT NationalID FROM Patients WHERE Username = ? AND Password = ?", (username, password))
    patient = cursor.fetchone()
    
    if patient:
        conn.close()
        return patient[0], 'patient'
    
    cursor.execute("SELECT DoctorID FROM Doctors WHERE Username = ? AND Password = ?", (username, password))
    doctor = cursor.fetchone()
    conn.close()
    if doctor:
        return doctor[0], 'doctor'

    return None

def main():
    st.title("Login Page")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    
    if st.button("Login"):
        user = authenticate_user(username, password)
        
        if user:
            user_id, role = user  # user[0] = UserID, user[1] = Role
            st.session_state.user_id = user_id
            st.session_state.role = role
            
            st.success(f"Logged in as {role.capitalize()}")
            doctor_interface() if role == 'doctor' else patient_interface(user_id)
            
            
        else:
            st.error("Invalid username or password")

if __name__ == "__main__":
    main()
