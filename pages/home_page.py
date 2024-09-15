import streamlit as st
import pandas as pd
from sheets_operations import read_sheet

@st.cache_data(ttl=600)  # Cache for 10 minutes
def get_contractors_data():
    return read_sheet('contractors')

@st.cache_data(ttl=600)  # Cache for 10 minutes
def get_services():
    df = read_sheet('services')
    if df.empty:
        return ["Plumbing", "Tiles", "False Ceiling", "Mesh Door", "Painting", "Electrical Work", "Carpentry", "Flooring", "Masonry", "HVAC", "Landscaping", "Cleaning", "Pest Control"]
    return df['Service Name'].tolist()

@st.cache_data(ttl=60)  # Cache for 1 minute
def filter_contractors(df, search_query, selected_service, selected_city):
    if search_query:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
    if selected_service != "All":
        df = df[df['Service'] == selected_service]
    if selected_city:
        df = df[df['City'].str.contains(selected_city, case=False)]
    return df

def display():
    st.header("Search and Filter Contractors")

    contractors_df = get_contractors_data()

    # Get query parameters
    query_params = st.query_params
    
    with st.expander("Search and Filter Options", expanded=True):
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        with col1:
            search_query = st.text_input("Search by keyword", value=query_params.get("search", ""), key="search_keyword")
        with col2:
            selected_service = st.selectbox("Filter by service", ["All"] + get_services(), index=get_services().index(query_params.get("service", "All")) if query_params.get("service") in get_services() else 0, key="filter_service")
        with col3:
            selected_city = st.text_input("Filter by city", value=query_params.get("city", ""), key="filter_city")
        with col4:
            if st.button("Reset Filters"):
                st.query_params.clear()
                st.rerun()

    # Update query parameters
    if search_query:
        st.query_params["search"] = search_query
    if selected_service != "All":
        st.query_params["service"] = selected_service
    if selected_city:
        st.query_params["city"] = selected_city

    filtered_df = filter_contractors(contractors_df, search_query, selected_service, selected_city)

    st.data_editor(
        filtered_df,
        column_config={
            "Name": st.column_config.TextColumn("Name"),
            "Number": st.column_config.TextColumn("Number"),
            "City": st.column_config.TextColumn("City"),
            "Service": st.column_config.TextColumn("Service"),
            "Feedback": st.column_config.TextColumn("Feedback"),
        },
        hide_index=True,
        use_container_width=True,
        num_rows="dynamic",
        disabled=True,
        key="contractor_table"
    )