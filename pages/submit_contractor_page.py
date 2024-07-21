import streamlit as st
from db_setup import Session
from sqlalchemy import text
import re

def display():
    st.header("Submit Contractor Details")
    session = Session()
    services = get_services()
    services.append("Other")

    with st.form(key='contractor_form'):
        name = st.text_input("Contractor Name", key="contractor_name")
        number = st.text_input("Contact Number (10 digits)", key="contractor_number")
        city = st.text_input("City", key="contractor_city")
        
        selected_service = st.selectbox("Service Provided", services, key="contractor_service")
        
        if selected_service == "Other":
            new_service = st.text_input("Enter new service category", key="new_service")
        else:
            new_service = None
        
        feedback = st.text_area("Feedback", key="contractor_feedback")
        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            if not name or not number or not city or not selected_service:
                st.error("All fields are required.")
            elif not re.match(r'^\d{10}$', number):
                st.error("Invalid contact number. Must be exactly 10 digits.")
            elif selected_service == "Other" and not new_service:
                st.error("Please enter a new service category.")
            else:
                try:
                    # Check for duplicate
                    result = session.execute(text('''
                        SELECT * FROM contractors WHERE name = :name AND number = :number
                    '''), {"name": name, "number": number})
                    if result.first():
                        st.error("A contractor with this name and number already exists.")
                    else:
                        if selected_service == "Other":
                            # Add new service to the services table
                            session.execute(text('''
                                INSERT OR IGNORE INTO services (service_name) VALUES (:service_name)
                            '''), {"service_name": new_service})
                            session.commit()
                            service = new_service
                        else:
                            service = selected_service

                        # Insert data into contractors table
                        session.execute(text('''
                            INSERT INTO contractors (name, number, city, service, feedback) 
                            VALUES (:name, :number, :city, :service, :feedback)
                        '''), {"name": name, "number": number, "city": city, "service": service, "feedback": feedback})
                        session.commit()
                        st.success("Contractor details submitted successfully!")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

    session.close()

def get_services():
    session = Session()
    result = session.execute(text("SELECT service_name FROM services"))
    services = [row[0] for row in result.fetchall()]  # Changed this line
    session.close()
    if not services:
        services = ["Plumbing", "Tiles", "False Ceiling", "Mesh Door", "Painting", "Electrical Work", "Carpentry", "Flooring", "Masonry", "HVAC", "Landscaping", "Cleaning", "Pest Control"]
    return services