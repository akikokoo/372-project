import streamlit as st
from datetime import datetime
from p_appointment_page import appointments_page
from p_lab_results_page import lab_results_page
from p_medical_records_page import medical_records_page
from p_prescriptions_page import prescriptions_page
from query_func import (
    get_appointments_by_patient,
    cancel_appointment,
    get_lab_results_by_patient,
    get_medical_records_by_patient,
    get_prescriptions_by_patient,
    get_all_specializations,
    get_doctors_by_specialization
)

def patient_page(patient_id):
    st.title("Patient Dashboard")
    st.write("Welcome to the Patient Interface!")

    # Kullanıcının hasta ID'sini session'dan çekiyoruz
    patient_id = st.session_state.get("user_id")

    # Menü Seçimi
    menu = st.sidebar.selectbox("Menu", ["Appointments", "Lab Results", "Medical Records", "Prescriptions", "Doctors & Specializations"])

    # ** Appointments Section **
    if menu == "Appointments":
        appointments_page(patient_id)


    # ** Lab Results Section **
    elif menu == "Lab Results":
        lab_results_page(patient_id)

    # ** Medical Records Section **
    elif menu == "Medical Records":
        medical_records_page(patient_id)

    # ** Prescriptions Section **
    elif menu == "Prescriptions":
        prescriptions_page(patient_id)
        

    # ** Doctors & Specializations Section **
    elif menu == "Doctors & Specializations":
        st.header("Doctors & Specializations")
        
        # Tüm uzmanlıkları getir
        specializations = get_all_specializations()
        specialization_names = [spec[1] for spec in specializations]
        selected_specialization = st.selectbox("Select Specialization", specialization_names)
        
        if selected_specialization:
            doctors = get_doctors_by_specialization(selected_specialization)
            if doctors:
                for doctor in doctors:
                    st.write(f"**Name:** {doctor[1]} {doctor[2]}, **Contact Info:** {doctor[4]}, **Hire Date:** {doctor[5]}")
            else:
                st.info("No doctors found for this specialization.")

