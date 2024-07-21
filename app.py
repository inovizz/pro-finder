import streamlit as st
from pages import home_page, submit_contractor_page, add_service_category_page, admin_page, feature_suggestion_page
import db_setup

db_setup.setup_db()

# Set page config
st.set_page_config(layout="wide", page_title="Pro Finder", initial_sidebar_state="collapsed")

# Add custom CSS
st.markdown(
    """
    <style>
    .navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #0073e6;
        padding: 1rem;
        z-index: 1000000;  /* Increase z-index */
    }
    .navbar a {
        color: white;
        text-decoration: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
    .navbar a:hover {
        background-color: #005bb5;
    }
    .app-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: white;
    }
    .content {
        margin-top: 6rem;
        padding: 1rem;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f0f2f6;
        color: black;
        text-align: center;
        padding: 10px;
    }
    .footer a {
        color: #0073e6;
        text-decoration: none;
    }
    .stButton > button {
        background-color: #0073e6;
        color: white;
    }
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Navigation
st.markdown(
    """
    <div class="navbar">
        <div class="app-title">Pro Finder</div>
        <div>
            <a href="/" target="_self">Home</a>
            <a href="/?page=SubmitContractor" target="_self">Submit Contractor</a>
            <a href="/?page=AddServiceCategory" target="_self">Add New Service Category</a>
            <a href="/?page=AdminPage" target="_self">Admin Page</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Get the current page from the query parameters
page = st.query_params.get("page", "Home")

# Main content div
with st.container():
    st.markdown('<div class="content">', unsafe_allow_html=True)
    if page == "Home":
        home_page.display()
    elif page == "SubmitContractor":
        submit_contractor_page.display()
    elif page == "AddServiceCategory":
        add_service_category_page.display()
    elif page == "AdminPage":
        admin_page.display()
    elif page == "SuggestFeature":
        feature_suggestion_page.display()
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <div class="footer">
        <p>Developed with ❤️ by <a href="https://linkedin.com/in/inovizz" target="_blank">Sanchit</a> | 
        <a href="https://inovizz.com" target="_blank">Portfolio</a> | 
        <a href="/?page=SuggestFeature" target="_self">Suggest a Feature</a></p>
    </div>
    """,
    unsafe_allow_html=True
)