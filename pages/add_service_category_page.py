import streamlit as st
from sheets_operations import read_sheet, append_to_sheet
import re

def validate_category(category):
    if len(category.split()) > 2:
        return False, "Category must not be more than two words."
    
    if len(category) < 3 or len(category) > 30:
        return False, "Category length must be between 3 and 30 characters."
    
    if not re.match(r'^[A-Za-z0-9_ ]{3,30}$', category):
        return False, "Category must only contain letters, numbers, spaces, and underscores."
    
    return True, ""

def display():
    st.header("Add New Service Category")

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
                        df = read_sheet('services')
                        if df.empty:
                            st.error("Unable to read services sheet. Please check your connection and try again.")
                        elif 'Service Name' not in df.columns:
                            st.error("'Service Name' column not found in services sheet. Please check the sheet structure.")
                        elif suggested_service in df['Service Name'].values:
                            st.error("This service category already exists.")
                        else:
                            new_id = len(df) + 1
                            append_to_sheet('services', [new_id, suggested_service])
                            st.success("Service category added successfully!")
                            # Clear the cache for services
                            st.cache_data.clear()
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
                        st.error("If this error persists, please contact the administrator.")
                else:
                    st.error(error_message)