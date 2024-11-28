import streamlit as st
from login import main as login_page
from doctor_interface import doctor_interface
from patient_interface import patient_interface

def main():
    # Check if the user is logged in
    if 'role' not in st.session_state:
        login_page()  # Show the login page if not authenticated
    else:
        user_id = st.session_state.user_id
        role = st.session_state.role  # Retrieve the user role from session state
        st.text(f"role: {role}")
        # Redirect to appropriate interface based on the role
        if role == 'doctor':
            doctor_interface()
        elif role == 'patient':
            patient_interface(user_id)
        else:
            st.error("Unknown role. Please log in again.")

if __name__ == "__main__":
    main()
