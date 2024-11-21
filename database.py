import sqlite3

def create_connection():
    connection = sqlite3.connect('health_monitoring.db')
    return connection

def create_tables():
    connection = create_connection()
    cursor = connection.cursor()

    # Patients table with NationalID as primary key
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Patients (
        NationalID INTEGER PRIMARY KEY NOT NULL,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        DateOfBirth TEXT NOT NULL,
        Gender TEXT,
        ContactInfo TEXT,
        CreatedAt TEXT,
        Username TEXT UNIQUE NOT NULL,
        Password TEXT NOT NULL
    )
    ''')

    # DoctorsSpecializations table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS DoctorsSpecializations (
        SpecializationID INTEGER PRIMARY KEY AUTOINCREMENT,
        Specialization TEXT NOT NULL
    )
    ''')

    # Doctors table (with SpecializationID reference)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Doctors (
        DoctorID INTEGER PRIMARY KEY AUTOINCREMENT,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        SpecializationID INTEGER NOT NULL,
        ContactInfo TEXT,
        HireDate TEXT,
        Username TEXT UNIQUE NOT NULL,
        Password TEXT NOT NULL,
        FOREIGN KEY (SpecializationID) REFERENCES DoctorsSpecializations(SpecializationID)
    )
    ''')

    # TestTypes table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS TestTypes (
        TestTypeID INTEGER PRIMARY KEY AUTOINCREMENT,
        TestType TEXT NOT NULL,
        Description TEXT
    )
    ''')

    # LabResults table (with PatientID as NationalID reference)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS LabResults (
        ResultID INTEGER PRIMARY KEY AUTOINCREMENT,
        PatientID INTEGER NOT NULL,
        DoctorID INTEGER NOT NULL,
        TestTypeID INTEGER NOT NULL,
        ResultData TEXT,
        TestDate TEXT,
        FOREIGN KEY (PatientID) REFERENCES Patients(NationalID),
        FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID),
        FOREIGN KEY (TestTypeID) REFERENCES TestTypes(TestTypeID)
    )
    ''')

    # MedicalRecords table (with PatientID as NationalID reference)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS MedicalRecords (
        RecordID INTEGER PRIMARY KEY AUTOINCREMENT,
        PatientID INTEGER NOT NULL,
        DoctorID INTEGER NOT NULL,
        Diagnosis TEXT,
        Treatment TEXT,
        Notes TEXT,
        CreatedDate TEXT,
        FOREIGN KEY (PatientID) REFERENCES Patients(NationalID),
        FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID)
    )
    ''')

    # Appointments table (with PatientID as NationalID reference)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Appointments (
        AppointmentID INTEGER PRIMARY KEY AUTOINCREMENT,
        PatientID INTEGER NOT NULL,
        DoctorID INTEGER NOT NULL,
        AppointmentDate TEXT,
        Reason TEXT,
        FOREIGN KEY (PatientID) REFERENCES Patients(NationalID),
        FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID)
    )
    ''')

    # Prescriptions table
    cursor.execute('''
        CREATE TABLE Prescriptions (
            PrescriptionID INTEGER PRIMARY KEY AUTOINCREMENT,
            PatientID INTEGER NOT NULL,
            DoctorID INTEGER NOT NULL,
            AppointmentID INTEGER,
            PrescribedDate TEXT NOT NULL,
            FOREIGN KEY (PatientID) REFERENCES Patients(NationalID),
            FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID),
            FOREIGN KEY (AppointmentID) REFERENCES Appointments(AppointmentID)
        )
    ''')

    # PrescriptionDetails table
    cursor.execute('''
    CREATE TABLE PrescriptionDetails (
        DetailID INTEGER PRIMARY KEY AUTOINCREMENT,
        PrescriptionID INTEGER NOT NULL,
        MedicineName TEXT NOT NULL,
        Dosage TEXT NOT NULL,
        Instructions TEXT,
        FOREIGN KEY (PrescriptionID) REFERENCES Prescriptions(PrescriptionID)
    )
    ''')

    connection.commit()
    connection.close()

if __name__ == '__main__':
    create_tables()
