import streamlit as st
from db_setup import Session
from sqlalchemy import text
import re

def display():
    st.header("Submit Contractor Details")
    session = Session()
    services = get_services()

    with st.form(key='contractor_form'):
        name = st.text_input("Contractor Name", key="contractor_name")
        number = st.text_input("Contact Number", key="contractor_number")
        city = st.text_input("City", key="contractor_city")
        service = st.selectbox("Service Provided", services, key="contractor_service")
        feedback = st.text_area("Feedback", key="contractor_feedback")

        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        if not name or not number or not city or not service:
            st.error("All fields are required.")
        elif not re.match(r'^\d{10}$', number):
            st.error("Invalid contact number. Must be 10 digits.")
        else:
            st.write("Submitting contractor details...")
            # Insert data into SQLite
            session.execute(text('''
                INSERT INTO contractors (name, number, city, service, feedback) VALUES (:name, :number, :city, :service, :feedback)
            '''), {"name": name, "number": number, "city": city, "service": service, "feedback": feedback})
            session.commit()
            st.success("Contractor details submitted!")
    session.close()

def get_services():
    session = Session()
    result = session.execute(text("SELECT service_name FROM services"))
    services = [row['service_name'] for row in result.fetchall()]
    session.close()
    if not services:
        services = ["Plumbing", "Tiles", "False Ceiling", "Mesh Door", "Painting", "Electrical Work", "Carpentry", "Flooring", "Masonry", "HVAC", "Landscaping", "Cleaning", "Pest Control"]
    return services
