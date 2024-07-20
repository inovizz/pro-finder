import streamlit as st
from db_setup import Session
from sqlalchemy import text
import pandas as pd

def display():
    st.header("Admin Login")
    session = Session()

    username = st.text_input("Username", key="admin_username")
    password = st.text_input("Password", type="password", key="admin_password")
    login_button = st.button("Login", key="admin_login_button")

    if login_button:
        if username == st.secrets["admin"]["admin_username"] and password == st.secrets["admin"]["admin_password"]:
            st.session_state["admin_logged_in"] = True
            st.success("Logged in successfully")
        else:
            st.error("Invalid credentials")

    if st.session_state.get("admin_logged_in"):
        st.header("Review Service Suggestions")
        result = session.execute(text("SELECT * FROM service_suggestions"))
        suggestions = result.fetchall()
        columns = result.keys()

        if not suggestions:
            st.write("No service suggestions found.")
        else:
            df = pd.DataFrame(suggestions, columns=columns)
            st.dataframe(df)

            for i, suggestion in df.iterrows():
                approve_button = st.button(f"Approve {suggestion['suggested_service']}", key=f"approve_{suggestion['id']}")
                reject_button = st.button(f"Reject {suggestion['suggested_service']}", key=f"reject_{suggestion['id']}")

                if approve_button:
                    # Insert approved suggestion into contractors
                    session.execute(text('''
                        INSERT INTO contractors (name, number, city, service, feedback) VALUES (:name, :number, :city, :service, :feedback)
                    '''), {"name": suggestion["name"], "number": suggestion["number"], "city": suggestion["city"], "service": suggestion["suggested_service"], "feedback": suggestion["feedback"]})
                    session.execute(text("DELETE FROM service_suggestions WHERE id = :id"), {"id": suggestion["id"]})
                    session.commit()
                    st.success(f"Approved and added {suggestion['suggested_service']} to contractors")

                if reject_button:
                    # Delete from suggestions table
                    session.execute(text("DELETE FROM service_suggestions WHERE id = :id"), {"id": suggestion["id"]})
                    session.commit()
                    st.success(f"Rejected {suggestion['suggested_service']}")

        if st.button("Back to Home", key="admin_back_home"):
            st.experimental_set_query_params(page="Home")
    session.close()
