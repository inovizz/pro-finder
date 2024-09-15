import streamlit as st
from sheets_operations import append_to_sheet
from datetime import datetime

def display():
    st.header("Suggest a Feature")
    
    with st.form(key="feature_suggestion_form"):
        suggestion = st.text_area("What feature would you like to see?", max_chars=500)
        submit_button = st.form_submit_button("Submit Suggestion")
        
        if submit_button and suggestion:
            try:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                append_to_sheet('feature_suggestions', [suggestion, timestamp])
                st.success("Thank you for your suggestion!")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    st.markdown("[Back to Home](/?page=Home)")