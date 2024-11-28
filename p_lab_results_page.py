import streamlit as st
import json
from query_func import get_lab_results_by_patient

def lab_results_page(patient_id):
    st.header("My Lab Results")

    # Lab sonuçlarını al
    lab_results = get_lab_results_by_patient(patient_id)

    if lab_results:
        for result in lab_results:
            # [(1, 12345678901, 2, 1, 8, '{"doctor_comment": "iyi iyi", "T1": 14.0, "T2": 123.0}', '2024-11-29 01:01:31')]
            # Randevu sonucu
            st.subheader(f"Test Date: {result[6]}")  # Test tarihi
            
            # Lab result data (JSON formatında)
            result_data = json.loads(result[5])  # ResultData JSON formatında
            st.write("Doctor's Comment: ", result_data.get("doctor_comment", "No comment available"))
            
            # Eğer test türüne özgü veriler varsa onları yazdır
            for key, value in result_data.items():
                if key != "doctor_comment":
                    st.write(f"{key}: {value}")
    else:
        st.info("No lab results found for this patient.")

