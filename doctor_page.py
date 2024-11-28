import streamlit as st
from datetime import datetime
from p_appointment_page import appointments_page
from p_lab_results_page import lab_results_page
from p_medical_records_page import medical_records_page
from p_prescriptions_page import prescriptions_page
from query_func import (
    get_doctor_name_from_id,
    get_appointments_by_doctor,
    get_appointment_by_doctor_for_specific_patient,
    add_lab_result,
    add_medical_record,
    add_prescription
)

#Main page for the doctors
def main_doctor_page():
    #Get doctor id using session state
    doctor_id = st.session_state.get("user_id")

    #Get doctor's first name using doctor id
    doctor_first_name = get_doctor_name_from_id(doctor_id)

    st.title("Doctor Dashboard")
    st.write(f"Welcome Dr. {doctor_first_name}\n")
    st.write(f"Your ID is: {doctor_id}")

    # Sidebar menu for navigation
    doctor_menu = st.sidebar.selectbox(
        "What would you like to do?",
        ["All Appointments", "Add Lab Result For Patient", "Add Medical Result For Patient", "Add Prescription"]
    )

    #All Appointments
    if doctor_menu == "All Appointments":
        all_appointments_page(doctor_id)
        
    #"Add Lab Result For Patient
    if doctor_menu == "Add Lab Result For Patient":
        add_lab_results_page(doctor_id)
        
    #Add Medical Result For Patient
    if doctor_menu == "Add Medical Result For Patient":
        add_medical_result_page(doctor_id)
        
    #Add Prescription
    if doctor_menu == "Add Prescription":
        add_prescription_page(doctor_id)

# All Appointments Page
def all_appointments_page(doctor_id):
    """
    Displays all appointments for the logged-in doctor.

    Parameters:
        doctor_id (int): The ID of the doctor. Retrieved from session state.
    """
    # Set page title
    st.title("All Appointments")

    # Fetch appointments for the doctor
    appointments = get_appointments_by_doctor(doctor_id)

    # Check if there are appointments
    if not appointments:
        st.info("No appointments found.")
        return

    # Display appointments in a table format
    st.write("Here are your upcoming appointments:")
    appointments_data = [
        {
            "Appointment ID": appointment[0],
            "Patient Name": appointment[1],
            "Appointment Date": appointment[2],
            "Reason": appointment[3],
        }
        for appointment in appointments
    ]

    # Use Streamlit's DataFrame component to display data
    st.dataframe(appointments_data)

    # Add a feature to filter appointments by date
    st.subheader("Filter Appointments by Date")
    filter_date = st.date_input("Select a date to filter appointments:")

    # Filter appointments based on the selected date
    if filter_date:
        filtered_appointments = [
            appointment for appointment in appointments
            if appointment[2].startswith(filter_date.strftime('%Y-%m-%d'))
        ]

        if filtered_appointments:
            st.write("Appointments on selected date:")
            filtered_appointments_data = [
                {
                    "Appointment ID": appointment[0],
                    "Patient Name": appointment[1],
                    "Appointment Date": appointment[2],
                    "Reason": appointment[3],
                }
                for appointment in filtered_appointments
            ]
            st.dataframe(filtered_appointments_data)
        else:
            st.info("No appointments found for the selected date.")

# Add Prescription For Patient Page
def add_prescription_page(doctor_id):
    """
    Allows the doctor to add a prescription for a specific patient.

    Parameters:
        doctor_id (int): The ID of the doctor. Retrieved from session state.
    """
    st.title("Add Prescription for Patient")

    # Input for Patient ID
    patient_id = st.text_input("Enter Patient National ID:")

    if patient_id:
        # Get Appointment ID
        appointment_id = get_appointment_by_doctor_for_specific_patient(doctor_id, patient_id)

        if not appointment_id:
            st.error("No active appointment found for this patient.")
            return

        # Input for medicines
        st.subheader("Add Medicines to Prescription")
        medicines = []
        medicine_count = st.number_input("Number of medicines to prescribe:", min_value=1, step=1)

        for i in range(medicine_count):
            with st.expander(f"Medicine {i+1} Details"):
                medicine_name = st.text_input(f"Medicine {i+1} Name:", key=f"medicine_name_{i}")
                dosage = st.text_input(f"Medicine {i+1} Dosage:", key=f"dosage_{i}")
                instructions = st.text_area(f"Medicine {i+1} Instructions (optional):", key=f"instructions_{i}")

                if medicine_name and dosage:
                    medicines.append({
                        "name": medicine_name,
                        "dosage": dosage,
                        "instructions": instructions
                    })

        # Prescription date
        prescription_date = st.date_input("Prescription Date", datetime.now()).strftime('%Y-%m-%d')

        # Submit button
        if st.button("Submit Prescription"):
            if not medicines:
                st.error("Please add at least one medicine to the prescription.")
                return
            
            add_prescription(patient_id, doctor_id, appointment_id, medicines, prescription_date)
            st.success("Prescription added successfully.")

# Add Medical Result For Patient Page
def add_medical_result_page(doctor_id):
    """
    Allows the doctor to add a medical result for a specific patient.

    Parameters:
        doctor_id (int): The ID of the doctor. Retrieved from session state.
    """
    st.title("Add Medical Result for Patient")

    # Input for Patient ID
    patient_id = st.text_input("Enter Patient National ID:")

    if patient_id:
        # Get Appointment ID
        appointment_id = get_appointment_by_doctor_for_specific_patient(doctor_id, patient_id)

        if not appointment_id:
            st.error("No active appointment found for this patient.")
            return

        # Input fields for medical record
        st.subheader("Enter Medical Record Details")
        diagnosis = st.text_input("Diagnosis:")
        treatment = st.text_area("Treatment Plan:")
        notes = st.text_area("Additional Notes:")
        created_date = st.date_input("Record Date", datetime.now()).strftime('%Y-%m-%d')
        created_time = st.time_input("Record Time", datetime.now().time()).strftime('%H:%M:%S')
        created_datetime = f"{created_date} {created_time}"

        # Submit button
        if st.button("Submit Medical Record"):
            if not diagnosis or not treatment:
                st.error("Diagnosis and Treatment Plan are required fields.")
                return
            
            add_medical_record(patient_id, doctor_id, diagnosis, treatment, notes, created_datetime, appointment_id)
            st.success("Medical record added successfully.")

# Add Lab Results For Patient Page
def add_lab_results_page(doctor_id):
    """
    Allows the doctor to add lab results for a specific patient, dynamically displaying fields based on the test type.

    Parameters:
        doctor_id (int): The ID of the doctor. Retrieved from session state.
    """
    st.title("Add Lab Result for Patient")

    # Input for Patient ID
    patient_id = st.text_input("Enter Patient National ID:")

    if patient_id:
        # Get Appointment ID
        appointment_id = get_appointment_by_doctor_for_specific_patient(doctor_id, patient_id)

        if not appointment_id:
            st.error("No active appointment found for this patient.")
            return

        # Menu to select test type
        st.subheader("Select Test Type")
        test_types = {
            1: "MR",
            2: "Röntgen",
            3: "Tomografi",
            4: "Kan Tahlili"
        }

        selected_test_type_id = st.selectbox(
            "Choose the test type",
            options=test_types.keys(),
            format_func=lambda x: test_types[x]
        )

        # Display appropriate input fields based on the selected test type
        st.subheader("Enter Test Results")
        result_data = {"doctor_comment": st.text_input("Doctor Comment:")}

        if selected_test_type_id == 1:  # MR
            result_data["T1"] = st.number_input("T1 Value:", min_value=0.0)
            result_data["T2"] = st.number_input("T2 Value:", min_value=0.0)

        elif selected_test_type_id == 2:  # Röntgen
            # No additional fields for Röntgen, only the doctor_comment is required
            pass

        elif selected_test_type_id == 3:  # Tomografi
            # No additional fields for Tomografi, only the doctor_comment is required
            pass

        elif selected_test_type_id == 4:  # Kan Tahlili
            result_data["CRP"] = st.number_input("CRP Value:", min_value=0.0)
            result_data["B12"] = st.number_input("B12 Value:", min_value=0.0)
            result_data["Mg"] = st.number_input("Mg Value:", min_value=0.0)
            result_data["Fe"] = st.number_input("Fe Value:", min_value=0.0)

        # Date and time input for the test
        test_date = st.date_input("Test Date", datetime.now()).strftime('%Y-%m-%d')
        test_time = st.time_input("Test Time", datetime.now().time()).strftime('%H:%M:%S')
        test_datetime = f"{test_date} {test_time}"

        # Submit button
        if st.button("Submit Lab Result"):
            import json
            result_data_json = json.dumps(result_data)  # Convert the result data to a JSON string

            # Validate if required fields are filled
            if not result_data.get("doctor_comment"):
                st.error("Doctor Comment is required.")
                return

            # Save lab result to the database
            add_lab_result(patient_id, doctor_id, selected_test_type_id, result_data_json, test_datetime, appointment_id)
            st.success("Lab result added successfully.")
