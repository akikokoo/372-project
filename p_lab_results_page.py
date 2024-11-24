import streamlit as st
import json
from query_func import get_lab_results_by_patient

def lab_results_page(patient_id):
    st.header("My Lab Results")

    # Lab sonuçlarını al
    lab_results = get_lab_results_by_patient(patient_id)

    if lab_results:
        for result in lab_results:
            # Randevu sonucu
            st.subheader(f"Test Date: {result[5]}")  # Test tarihi
            
            # Lab result data (JSON formatında)
            result_data = json.loads(result[4])  # ResultData JSON formatında
            st.write("Doctor's Comment: ", result_data.get("doctor_comment", "No comment available"))
            
            # Eğer test türüne özgü veriler varsa onları yazdır
            for key, value in result_data.items():
                if key != "doctor_comment":
                    st.write(f"{key}: {value}")
    else:
        st.info("No lab results found for this patient.")

