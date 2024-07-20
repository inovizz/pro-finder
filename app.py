import streamlit as st
from pages import home_page, submit_contractor_page, add_service_category_page, admin_page
import db_setup

db_setup.setup_db()

# Collapse the sidebar by default and hide the collapse button
st.set_page_config(initial_sidebar_state="collapsed")
st.markdown(
    """
    <style>
        [data-testid="collapsedControl"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add title and logo
st.markdown(
    """
    <style>
    .navbar {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: center;
        background-color: #0073e6;
        padding: 10px;
        width: 100%;
    }
    .navbar a {
        color: white;
        text-decoration: none;
        padding: 10px;
        margin: 0 5px;
    }
    .navbar a:hover {
        background-color: #005bb5;
    }
    .navbar .buttons {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
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
    .logo {
        height: 50px;
    }
    .main-content {
        width: 100%;
        padding: 20px;
        box-sizing: border-box;
    }
    @media (max-width: 768px) {
        .navbar {
            flex-direction: column;
        }
        .navbar .buttons {
            flex-direction: column;
            width: 100%;
        }
        .navbar a {
            width: 100%;
            text-align: center;
            margin: 5px 0;
        }
    }
    </style>
    <div class="navbar">
        <img src="logo.png" class="logo">
        <div class="buttons">
            <a href="?page=Home">Home</a>
            <a href="?page=SubmitContractor">Submit Contractor</a>
            <a href="?page=AddServiceCategory">Add New Service Category</a>
            <a href="?page=AdminPage">Admin Page</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Get the current page from the query parameters
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["Home"])[0]

# Main content div
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Display the selected page
if page == "Home":
    home_page.display()
elif page == "SubmitContractor":
    submit_contractor_page.display()
elif page == "AddServiceCategory":
    add_service_category_page.display()
elif page == "AdminPage":
    admin_page.display()

# Close main content div
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <div class="footer">
        <p>Developed with <3 by <a href="https://linkedin.com/in/inovizz" target="_blank">Sanchit</a> | <a href="https://inovizz.com" target="_blank">Portfolio</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
