import sqlite3
import streamlit as st
from query_func import get_prescriptions_by_patient


def get_prescription_details_by_id(prescription_id):
    """
    Retrieves the details of a specific prescription.
    
    Parameters:
        prescription_id (int): The ID of the prescription to retrieve details for.
    
    Returns:
        list of tuples: Details of the prescription including medicine name, dosage, and instructions.
    """
    connection = sqlite3.connect('health_monitoring.db')  # Veritabanı bağlantısı
    cursor = connection.cursor()
    cursor.execute('''
        SELECT MedicineName, Dosage, Instructions 
        FROM PrescriptionDetails 
        WHERE PrescriptionID = ?
    ''', (prescription_id,))
    details = cursor.fetchall()
    connection.close()
    return details

def prescriptions_page(patient_id):
    st.header("My Prescriptions")

    # Hastanın reçetelerini al
    prescriptions = get_prescriptions_by_patient(patient_id)

    if prescriptions:
        for prescription in prescriptions:
            st.subheader(f"Prescription Date: {prescription[4]}")  # Reçete tarihi
            st.write(f"**Prescription ID:** {prescription[0]}")
            st.write(f"**Doctor ID:** {prescription[2]}")  # Doktor bilgisi

            # Reçete detaylarını al ve göster
            details = get_prescription_details_by_id(prescription[0])
            if details:
                st.write("**Prescription Details:**")
                for detail in details:
                    st.write(f"- **Medicine:** {detail[0]}, **Dosage:** {detail[1]}, **Instructions:** {detail[2]}")
            else:
                st.write("No details available for this prescription.")
    else:
        st.info("No prescriptions found for this patient.")