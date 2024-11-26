import streamlit as st
from query_func import get_medical_records_by_patient

def medical_records_page(patient_id):
    st.header("My Medical Records")

    # Hastanın tıbbi kayıtlarını al
    medical_records = get_medical_records_by_patient(patient_id)

    if medical_records:
        for record in medical_records:
            st.subheader(f"Record ID: {record[0]}")  # Tıbbi kayıt ID'si
            st.write(f"**Date:** {record[4]}")  # Kayıt tarihi
            st.write(f"**Doctor Name:** {record[5]}")  # Doktor adı
            st.write(f"**Diagnosis:** {record[1]}")  # Tanı
            st.write(f"**Treatment:** {record[2]}")  # Tedavi
            st.write(f"**Notes:** {record[3]}")  # Notlar
            st.markdown("---")  # Kayıtlar arasında ayırıcı çizgi
    else:
        st.info("No medical records found for this patient.")
