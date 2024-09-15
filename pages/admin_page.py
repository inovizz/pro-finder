import streamlit as st
from sheets_operations import read_sheet, append_to_sheet, delete_from_sheet
import pandas as pd

def display():
    st.header("Admin Login")

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
        df_suggestions = read_sheet('service_suggestions')

        if df_suggestions.empty:
            st.write("No service suggestions found.")
        else:
            st.dataframe(df_suggestions)

            for i, suggestion in df_suggestions.iterrows():
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Approve {suggestion['suggested_service']}", key=f"approve_{suggestion['id']}"):
                        # Insert approved suggestion into contractors
                        append_to_sheet('contractors', [suggestion["name"], suggestion["number"],
                                                        suggestion["city"], suggestion["suggested_service"],
                                                        suggestion["feedback"]])
                        delete_from_sheet('service_suggestions', i + 2)  # +2 because sheet is 1-indexed and has a header
                        st.success(f"Approved and added {suggestion['suggested_service']} to contractors")
                        st.rerun()
                with col2:
                    if st.button(f"Reject {suggestion['suggested_service']}", key=f"reject_{suggestion['id']}"):
                        # Delete from suggestions sheet
                        delete_from_sheet('service_suggestions', i + 2)  # +2 because sheet is 1-indexed and has a header
                        st.success(f"Rejected {suggestion['suggested_service']}")
                        st.rerun()
        
        st.header("Feature Suggestions")
        df_features = read_sheet('feature_suggestions')

        if df_features.empty:
            st.write("No feature suggestions found.")
        else:
            st.dataframe(df_features)

        if st.button("Logout", key="admin_logout"):
            st.session_state["admin_logged_in"] = False
            st.rerun()