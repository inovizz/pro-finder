import streamlit as st
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import asyncio
import threading

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_spreadsheet_id():
    return st.secrets["google_sheets"]["spreadsheet_id"]

def get_sheets_service():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )
    service = build('sheets', 'v4', credentials=creds)
    return service.spreadsheets()

async def setup_sheets():
    sheets = get_sheets_service()
    spreadsheet_id = get_spreadsheet_id()
    
    required_sheets = ['contractors', 'service_suggestions', 'services', 'feature_suggestions']
    
    try:
        spreadsheet = sheets.get(spreadsheetId=spreadsheet_id).execute()
        existing_sheets = [sheet['properties']['title'] for sheet in spreadsheet.get('sheets', [])]
        
        for sheet_name in required_sheets:
            if sheet_name not in existing_sheets:
                sheets.batchUpdate(spreadsheetId=spreadsheet_id, body={
                    "requests": [{
                        "addSheet": {
                            "properties": {
                                "title": sheet_name
                            }
                        }
                    }]
                }).execute()
        
        await populate_dummy_data_if_empty(sheets, spreadsheet_id)
        
    except HttpError as error:
        st.error(f"An error occurred: {error}")
        st.error("Please check your Google Sheets setup and try again.")

async def populate_dummy_data_if_empty(sheets, spreadsheet_id):
    from populate_dummy_data import populate_dummy_data
    
    result = sheets.values().get(spreadsheetId=spreadsheet_id, range='services!A1:B').execute()
    if 'values' not in result or len(result['values']) <= 1:  # Only header or empty
        await populate_dummy_data(spreadsheet_id)

def run_async(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

if __name__ == "__main__":
    run_async(setup_sheets())