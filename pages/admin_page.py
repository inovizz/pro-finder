import streamlit as st
from db_setup import Session
from sqlalchemy import text
import pandas as pd

def display():
    st.header("Admin Login")
    session = Session()

    if "admin_logged_in" not in st.session_state:
        st.session_state["admin_logged_in"] = False

    if not st.session_state["admin_logged_in"]:
        with st.form("admin_login"):
            username = st.text_input("Username", key="admin_username")
            password = st.text_input("Password", type="password", key="admin_password")
            login_button = st.form_submit_button("Login")

            if login_button:
                if username == st.secrets["admin"]["admin_username"] and password == st.secrets["admin"]["admin_password"]:
                    st.session_state["admin_logged_in"] = True
                    st.success("Logged in successfully")
                    st.rerun()
                else:
                    st.error("Invalid credentials")

    if st.session_state["admin_logged_in"]:
        st.header("Review Service Suggestions")
        result = session.execute(text("SELECT * FROM service_suggestions"))
        suggestions = result.fetchall()
        columns = result.keys()

        if not suggestions:
            st.write("No service suggestions found.")
        else:
            df = pd.DataFrame([dict(zip(columns, row)) for row in suggestions])
            st.dataframe(df)

            for i, suggestion in df.iterrows():
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Approve {suggestion['suggested_service']}", key=f"approve_{suggestion['id']}"):
                        # Insert approved suggestion into contractors
                        session.execute(text('''
                            INSERT INTO contractors (name, number, city, service, feedback)
                            VALUES (:name, :number, :city, :service, :feedback)
                        '''), {"name": suggestion["name"], "number": suggestion["number"],
                               "city": suggestion["city"], "service": suggestion["suggested_service"],
                               "feedback": suggestion["feedback"]})
                        session.execute(text("DELETE FROM service_suggestions WHERE id = :id"), {"id": suggestion["id"]})
                        session.commit()
                        st.success(f"Approved and added {suggestion['suggested_service']} to contractors")
                        st.rerun()
                with col2:
                    if st.button(f"Reject {suggestion['suggested_service']}", key=f"reject_{suggestion['id']}"):
                        # Delete from suggestions table
                        session.execute(text("DELETE FROM service_suggestions WHERE id = :id"), {"id": suggestion["id"]})
                        session.commit()
                        st.success(f"Rejected {suggestion['suggested_service']}")
                        st.rerun()
        
        st.header("Feature Suggestions")
        result = session.execute(text("SELECT * FROM feature_suggestions ORDER BY timestamp DESC"))
        feature_suggestions = result.fetchall()
        columns = result.keys()

        if not feature_suggestions:
            st.write("No feature suggestions found.")
        else:
            df = pd.DataFrame([dict(zip(columns, row)) for row in feature_suggestions])
            st.dataframe(df)

        if st.button("Logout", key="admin_logout"):
            st.session_state["admin_logged_in"] = False
            st.rerun()

    session.close()