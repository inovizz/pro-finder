import streamlit as st
from db_setup import Session
from sqlalchemy import text
import re

def validate_category(category):
    # Check if the category is not more than two words
    if len(category.split()) > 2:
        return False, "Category must not be more than two words."
    
    # Check if the category length is within the acceptable range
    if len(category) < 3 or len(category) > 30:
        return False, "Category length must be between 3 and 30 characters."
    
    # Check if the category only contains letters, numbers, spaces, and underscores
    if not re.match(r'^[A-Za-z0-9_ ]{3,30}$', category):
        return False, "Category must only contain letters, numbers, spaces, and underscores."
    
    return True, ""

def display():
    st.header("Add New Service Category")
    session = Session()

    with st.form(key='service_category_form'):
        suggested_service = st.text_input("Service Category Name", key="suggested_service")
        submit_button = st.form_submit_button(label='Add Category')

        if submit_button:
            if not suggested_service:
                st.error("Service category name is required.")
            else:
                is_valid, error_message = validate_category(suggested_service)
                if is_valid:
                    try:
                        # Insert data into SQLite
                        session.execute(text('''
                            INSERT OR IGNORE INTO services (service_name) VALUES (:service_name)
                        '''), {"service_name": suggested_service})
                        session.commit()
                        st.success("Service category added successfully!")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
                else:
                    st.error(error_message)

    session.close()