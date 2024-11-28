import streamlit as st
from patient_page import patient_page

def patient_interface(user_id):
    st.write("Redirecting to the patient page...")
    patient_page(user_id)
