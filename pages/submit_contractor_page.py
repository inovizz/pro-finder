import streamlit as st
from sheets_operations import read_sheet, append_to_sheet
import re

@st.cache_data(ttl=600)  # Cache for 10 minutes
def get_services():
    df = read_sheet('services')
    if df.empty:
        return ["Plumbing", "Tiles", "False Ceiling", "Mesh Door", "Painting", "Electrical Work", "Carpentry", "Flooring", "Masonry", "HVAC", "Landscaping", "Cleaning", "Pest Control"]
    return df['Service Name'].tolist()  # Changed from 'service_name' to 'Service Name'

def display():
    st.header("Submit Contractor Details")
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
                    df = read_sheet('contractors')
                    if ((df['Name'] == name) & (df['Number'] == number)).any():
                        st.error("A contractor with this name and number already exists.")
                    else:
                        if selected_service == "Other":
                            services_df = read_sheet('services')
                            new_id = len(services_df) + 1
                            append_to_sheet('services', [new_id, new_service])
                            service = new_service
                        else:
                            service = selected_service

                        # Insert data into contractors sheet
                        append_to_sheet('contractors', [name, number, city, service, feedback])
                        st.success("Contractor details submitted successfully!")
                        # Clear the cache to reflect the new service
                        get_services.clear()
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")