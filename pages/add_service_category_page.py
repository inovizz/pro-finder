import streamlit as st
from db_setup import Session
from sqlalchemy import text
import re

def display():
    st.header("Add New Service Category")
    session = Session()

    with st.form(key='service_category_form'):
        suggested_service = st.text_input("Service Category Name", key="suggested_service")

        submit_button = st.form_submit_button(label='Add Category')

    if submit_button:
        if not suggested_service:
            st.error("Service category name is required.")
        elif not re.match(r'^[A-Za-z0-9_]{1,20}$', suggested_service):
            st.error("Service category name must be 1-20 characters long, no spaces, and only letters, numbers, and underscores are allowed.")
        else:
            try:
                st.write("Adding new service category...")
                # Insert data into SQLite
                session.execute(text('''
                    INSERT INTO services (service_name) VALUES (:service_name)
                '''), {"service_name": suggested_service})
                session.commit()
                st.success("Service category added successfully!")
            except:
                st.error("Service category already exists.")
    session.close()
