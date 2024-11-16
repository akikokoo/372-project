import streamlit as st

def patient_interface():
    st.text("Patient Interface")
    st.text(f"here the role is: {st.session_state.role}")