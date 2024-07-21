import streamlit as st
from db_setup import Session
from sqlalchemy import text

def display():
    st.header("Suggest a Feature")
    
    with st.form(key="feature_suggestion_form"):
        suggestion = st.text_area("What feature would you like to see?", max_chars=500)
        submit_button = st.form_submit_button("Submit Suggestion")
        
        if submit_button and suggestion:
            session = Session()
            try:
                session.execute(text('''
                    INSERT INTO feature_suggestions (suggestion) VALUES (:suggestion)
                '''), {"suggestion": suggestion})
                session.commit()
                st.success("Thank you for your suggestion!")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
            finally:
                session.close()

    st.markdown("[Back to Home](/?page=Home)")