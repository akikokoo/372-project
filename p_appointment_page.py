import streamlit as st
from datetime import datetime, timedelta
from query_func import (
    add_appointment,
    get_appointments_by_patient,
    get_appointments_by_doctor,
    get_doctors_by_specialization,
    get_all_specializations,
    cancel_appointment
)

def is_time_slot_available(doctor_id, appointment_date):
    """
    Checks if the selected time slot is available for the doctor.
    """
    appointments = get_appointments_by_doctor(doctor_id)  # Fetch all appointments for the doctor
    for appointment in appointments:
        if appointment[2] == appointment_date:  # Check if the date and time matches
            return False
    return True

def is_patient_time_slot_available(patient_id, appointment_date):
    """
    Checks if the selected time slot is already booked by the patient.
    """
    appointments = get_appointments_by_patient(patient_id)  # Fetch all appointments for the patient
    for appointment in appointments:
        if appointment[3] == appointment_date:  # Check if the date and time matches
            return False
    return True

def get_doctor_unavailable_hours(doctor_id, date):
    """
    Retrieves the unavailable hours for a doctor on a specific date.
    """
    appointments = get_appointments_by_doctor(doctor_id)  # Fetch all appointments for the doctor
    unavailable_hours = []
    for appointment in appointments:
        appointment_date, appointment_time = appointment[2].split(" ")  # Split date and time
        if appointment_date == date:  # Check if the appointment is on the selected date
            unavailable_hours.append(appointment_time)  # Add the time to the unavailable list
    return unavailable_hours

def appointments_page(patient_id):
    st.header("Appointments")

    # Kullanıcının mevcut randevularını görüntüleme
    st.subheader("My Appointments")
    appointments = get_appointments_by_patient(patient_id)  # Fetch updated appointments every time

    if appointments:
        for appointment in appointments:
            st.write(f"**Date:** {appointment[3]}, **Reason:** {appointment[4]}")

            # Cancel Appointment Butonu
            if st.button(f"Cancel Appointment {appointment[0]}", key=f"cancel-{appointment[0]}"):
                cancel_appointment(appointment[0])  # Randevuyu iptal et
                st.success("Appointment canceled successfully!")
    else:
        st.info("No appointments found.")

    # Yeni randevu ekleme
    st.subheader("Add New Appointment")

    # Uzmanlık seçimi
    specializations = get_all_specializations()
    specialization_names = [spec[1] for spec in specializations]
    selected_specialization = st.selectbox("Select Specialization", specialization_names)

    if selected_specialization:
        # Uzmanlığa göre doktor seçimi
        doctors = get_doctors_by_specialization(selected_specialization)
        doctor_options = {f"{doctor[1]} {doctor[2]}": doctor[0] for doctor in doctors}
        selected_doctor = st.selectbox("Select Doctor", list(doctor_options.keys()))

        if selected_doctor:
            doctor_id = doctor_options[selected_doctor]

            # Tarih seçimi (önümüzdeki 5 iş günü)
            today = datetime.now()
            weekdays = [today + timedelta(days=i) for i in range(5) if (today + timedelta(days=i)).weekday() < 5]
            selected_date = st.selectbox("Select Appointment Date", [day.strftime("%Y-%m-%d") for day in weekdays])

            if selected_date:
                # Doktorun dolu saatlerini al
                unavailable_hours = get_doctor_unavailable_hours(doctor_id, selected_date)
                all_hours = [f"{hour}:00" for hour in range(9, 18)] + [f"{hour}:30" for hour in range(9, 17)]
                
                # Müsait saatleri filtrele
                available_hours = [hour for hour in all_hours if hour not in unavailable_hours]

                # Eğer tüm saatler doluysa bilgi göster
                if not available_hours:
                    st.info("No available times for this date. Please choose another day.")
                else:
                    selected_time = st.selectbox("Select Appointment Time", available_hours)

                    if selected_time:
                        # Randevu nedeni
                        reason = st.text_input("Reason for Appointment")

                        if st.button("Confirm Appointment"):
                            appointment_date = f"{selected_date} {selected_time}:00"

                            # Hasta ve doktor için çakışma kontrolü
                            if not is_time_slot_available(doctor_id, appointment_date):
                                st.error("The selected time slot is not available for this doctor.")
                            elif not is_patient_time_slot_available(patient_id, appointment_date):
                                st.error("You already have an appointment at this time. Please choose a different time.")
                            else:
                                add_appointment(patient_id, doctor_id, appointment_date, reason)
                                st.success("Appointment added successfully!")

                                # My Appointments kısmını otomatik olarak güncellemek için çağrılıyor
                                appointments = get_appointments_by_patient(patient_id)  # Fetch updated appointments
