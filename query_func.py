import sqlite3
from datetime import datetime


def create_connection():
    return sqlite3.connect('health_monitoring.db')


# ** Appointments Page **

# Patient UI
def add_appointment(patient_id, doctor_id, appointment_date, reason):
    """
    Adds a new appointment to the database.
    For doctors, the appointment_date can be from 9.00-17.00 with incresing 30 minutes. Example: 9.00 appointment, 9.30 appointment...
    So the patient/appointment page should be designed in that matter, there should be five days of weekdays to select and after selection available hours should be displayed to select the appointment time.

    Parameters:
        patient_id (int): The National ID of the patient. Get patient_id from st.session_state.user_id
        doctor_id (int): The ID of the doctor. Get relevant doctor IDs from the get_doctors_by_specialization function.
        appointment_date (str): The date and time of the appointment. Format: 'YYYY-MM-DD HH:MM:SS'
        reason (str): Reason for the appointment.
    """
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
    INSERT INTO Appointments (PatientID, DoctorID, AppointmentDate, Reason)
    VALUES (?, ?, ?, ?)
    ''', (patient_id, doctor_id, appointment_date, reason))
    connection.commit()
    connection.close()

# Patient UI
def get_appointments_by_patient(national_id):
    """
    Retrieves all appointments for a specific patient.
    
    Parameters:
        national_id (int): The National ID of the patient. Get patient_id from st.session_state.user_id
    
    Returns:
        list of tuples: All appointments belonging to the patient.
    """
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Appointments WHERE PatientID = ?', (national_id,))
    results = cursor.fetchall()
    connection.close()
    return results

# Doctor UI
def get_appointments_by_doctor(doctor_id):
    """
    Retrieves all appointments for a specific doctor. Use it in doctor's appointment page.
    
    Parameters:
        doctor_id (int): The ID of the doctor. Get doctor_id from st.session_state.user_id
    
    Returns:
        list of tuples: Appointments with patient names and details.
    """
    try:
        connection = create_connection()
        print('CONNECTION')
    except:
        print('NO CONNECTION')
    cursor = connection.cursor()
    cursor.execute('''
    SELECT a.AppointmentID, p.FirstName || ' ' || p.LastName AS PatientName, a.AppointmentDate, a.Reason
    FROM Appointments a
    JOIN Patients p ON a.PatientID = p.NationalID
    WHERE a.DoctorID = ?
    ORDER BY a.AppointmentDate ASC
    ''', (doctor_id,))
    results = cursor.fetchall()
    connection.close()
    return results

# Doctor UI 
def get_appointment_by_doctor_for_specific_patient(doctor_id, patient_id):
    """
    Retrieves the appointment_id based on the doctor and patient(a patient can have atmost 1 appointment for one specific doctor).
    Use it when doctor adds lab results, medical records or prescriptions to the patient. 
    The reason this function exists is to know appointment_id to link the lab results, medical records or prescriptions to the appointment.
    
    Parameters:
        doctor_id (int): The ID of the doctor. Get doctor_id from st.session_state.user_id
        patient_id (int): The National ID of the patient. Assume doctor already knows patient's id(by asking him or getting his national identity card).
    
    Returns:
        list of tuples: Appointments with patient names and details.
    """
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT AppointmentID FROM Appointments
        WHERE PatientID = ? AND DoctorID = ?
        ORDER BY AppointmentDate DESC LIMIT 1
    ''', (patient_id, doctor_id))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else None

# Patient UI
def cancel_appointment(appointment_id):
    """
    Cancels (deletes) an appointment by its ID. Get the relevant appointment ID from the get_appointments_by_patient function.

    Parameters:
        appointment_id (int): The ID of the appointment to cancel. Get appointment_id from the get_appointments_by_patient function.
    """
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Appointments WHERE AppointmentID = ?', (appointment_id,))
    connection.commit()
    connection.close()

# ** Test Types **

# Used in add_lab_result function
def get_all_test_types():
    """
    Retrieves all defined test types available for lab results.
    
    Returns:
        list of tuples: All test types available in the system.
    """
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM TestTypes')
    results = cursor.fetchall()
    connection.close()
    return results

# ** Lab Results Page **

# Doctor UI
def add_lab_result(patient_id, doctor_id, test_type_id, result_data, test_date, appointment_id):
    """
    Adds a new lab result for a patient. This has the advanced feature of the project which is result_data as json string.
    
    doctor_comment attribute is necessary across all test types
    other than doctor_comment attribute, create the needed input sections for every attribute for the selected TestType
    So that doctor can fill the needed data for the test type he/she selected.
    So firstly doctor will select TestType(MR,Röntgen,Tomografi or Kan Tahlili) then the needed attribute input sections will be displayed over this filtering. 

    For MR test type use the following attributes:
    {"doctor_comment": overall acceptable", "T1":10, "T2":20}

    For Röntgen test type use the following attribute:
    {"doctor_comment": "Leg injury, may need surgery"}

    For Tomografi test type use the following attribute:
    {"doctor_comment": "Lungs are clear, no issues"}

    For Kan Tahlili test type use the following attributes:
    {"doctor_comment": "B12 is low", "CRP":12, "B12":11, "Mg":11, "Fe":12}
    
    Here is how to store this data to db:
        import json

        # JSON data to be stored
        # let's assume Doctor selected Tomografi as TestType in lab results
        # so we only show one input section and that is for doctor_comment attribute
        json_data = {"doctor_comment": "LDL is low, overall acceptable"}

        # Serialize the JSON object to a string
        json_string = json.dumps(json_data)
    
    Parameters:
        patient_id (int): The National ID of the patient. Assume doctor know patient's id(by asking him or getting his national identity card).
        doctor_id (int): The ID of the doctor ordering the test. Get doctor_id from st.session_state.user_id
        test_type_id (int): The ID of the test type (e.g., blood test, X-ray). Get test_type_id from get_all_test_types function.
        result_data (str): The data/results of the test. The format is JSON. Example:
        test_date (str): The date the test was conducted. Format: 'YYYY-MM-DD HH:MM:SS'
        appointment_id (int): The ID of the appointment. Get appointment_id from the get_appointments_by_doctor_for_specific_patient function.
    """
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
    INSERT INTO LabResults (PatientID, DoctorID, TestTypeID, ResultData, TestDate, AppointmentID)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (patient_id, doctor_id, test_type_id, result_data, test_date, appointment_id))
    connection.commit()
    connection.close()

# Patient UI
def get_lab_results_by_patient(national_id):
    """
    Retrieves all lab results for a specific patient.
    Read the add_lab_result function's description to understand the structure of the ResultData attribute of the LabResults Table.
    
    Here is how to retrieve this data from db:
    import json 

    json_data = json.loads(ResultData)  # ResultData is the name of our advanced feature in LabResults table which doctor fills this value in Doctor UI
    print(json_data)  # Output: {"doctor_comment": "LDL is low, overall acceptable"} assuming TestType is Tomografi or any other one attributed TestType

    Parameters:
        national_id (int): The National ID of the patient. Get patient_id from st.session_state.user_id
    
    Returns:
        list of tuples: Lab results belonging to the patient.
    """
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM LabResults WHERE PatientID = ?', (national_id,))
    results = cursor.fetchall()
    connection.close()
    return results

# ** Medical Records Page **

# Doctor UI
def add_medical_record(patient_id, doctor_id, diagnosis, treatment, notes, created_date, appointment_id):
    """
    Adds a new medical record for a patient.
    
    Parameters:
        patient_id (int): The National ID of the patient. Assume doctor know patient's id(by asking him or getting his national identity card).
        doctor_id (int): The ID of the doctor creating the record. Get doctor_id from st.session_state.user_id
        diagnosis (str): The diagnosis of the patient.
        treatment (str): Treatment plan for the patient.
        notes (str): Additional notes from the doctor.
        created_date (str): The date the record was created. Format: 'YYYY-MM-DD HH:MM:SS'
        appointment_id (int): The ID of the appointment. Get appointment_id from the get_appointments_by_doctor_for_specific_patient function.
    """
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute('''
    INSERT INTO MedicalRecords (PatientID, DoctorID, Diagnosis, Treatment, Notes, CreatedDate)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (patient_id, doctor_id, diagnosis, treatment, notes, created_date))
    
    connection.commit()
    connection.close()

# Patient UI
def get_medical_records_by_patient(patient_id):
    """
    Retrieves all medical records for a specific patient, including doctor names.
    
    Parameters:
        patient_id (int): The National ID of the patient. Get patient_id from st.session_state.user_id
    
    Returns:
        list of tuples: Medical records along with doctor details.
    """
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute('''
    SELECT 
        mr.RecordID, 
        mr.Diagnosis, 
        mr.Treatment, 
        mr.Notes, 
        mr.CreatedDate,
        d.FirstName || ' ' || d.LastName AS DoctorName
    FROM MedicalRecords AS mr
    INNER JOIN Doctors AS d ON mr.DoctorID = d.DoctorID
    WHERE mr.PatientID = ?
    ORDER BY mr.CreatedDate DESC
    ''', (patient_id,))
    
    records = cursor.fetchall()
    connection.close()
    return records

# ** Prescriptions Page **

# Doctor UI
def add_prescription(patient_id, doctor_id, appointment_id, medicines, prescription_date):
    connection = sqlite3.connect("your_database.db")
    cursor = connection.cursor()

    # Add prescription metadata
    cursor.execute('''
        INSERT INTO Prescriptions (PatientID, DoctorID, AppointmentID, PrescribedDate)
        VALUES (?, ?, ?, ?)
    ''', (patient_id, doctor_id, appointment_id, prescription_date))
    
    prescription_id = cursor.lastrowid  # Get the newly created PrescriptionID

    # Add medicine details
    for medicine in medicines:
        cursor.execute('''
            INSERT INTO PrescriptionDetails (PrescriptionID, MedicineName, Dosage, Instructions)
            VALUES (?, ?, ?, ?)
        ''', (prescription_id, medicine['name'], medicine['dosage'], medicine.get('instructions', '')))
    
    connection.commit()
    connection.close()

# Patient UI
def get_prescriptions_by_patient(national_id):
    """
    Retrieves all prescriptions for a specific patient.
    
    Parameters:
        national_id (int): The National ID of the patient. Get patient_id from st.session_state.user_id
    
    Returns:
        list of tuples: Prescriptions belonging to the patient.
    """
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Prescriptions WHERE PatientID = ?', (national_id,))
    results = cursor.fetchall()
    connection.close()
    return results

# ** Specializations **

# Patient UI
def get_all_specializations():
    """
    Retrieves all specializations available for doctors.
    
    Returns:
        list of tuples: All doctor specializations.
    """
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM DoctorsSpecializations')
    results = cursor.fetchall()
    connection.close()
    return results

# ** Doctors by Specialization / Patient Appointment UI**

# Patient UI
def get_doctors_by_specialization(specialization):
    """
    Retrieves all doctors for a specific specialization. Use this function to filter doctor results based on specialization select in Patient/Appointment page.
    
    Parameters:
        specialization (str): The specialization to filter by (e.g., "Cardiology"). Get specialization from get_all_specializations function.
    
    Returns:
        list of tuples: Doctors matching the specified specialization.
    """
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute('''
    SELECT d.DoctorID, d.FirstName, d.LastName, ds.Specialization, d.ContactInfo, d.HireDate
    FROM Doctors d
    INNER JOIN DoctorsSpecializations ds ON d.SpecializationID = ds.SpecializationID
    WHERE ds.Specialization = ?
    ''', (specialization,))
    
    doctors = cursor.fetchall()
    connection.close()
    return doctors


# Doctor UI
def get_doctor_name_from_id(doctor_id):
    """
    Retrieves the name of the doctor using the doctor's ID.

    Parameters:
        doctor_id (int): The ID of the doctor.

    Returns:
        str: The full name of the doctor, or None if no doctor is found.
    """
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT FirstName || ' ' || LastName AS DoctorName
        FROM Doctors
        WHERE DoctorID = ?
    ''', (doctor_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else None
