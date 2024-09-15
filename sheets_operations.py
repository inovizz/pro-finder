import streamlit as st
from db_setup import get_sheets_service, get_spreadsheet_id
import pandas as pd
import asyncio

@st.cache_data(ttl=600)  # Cache for 10 minutes
def read_sheet(sheet_name):
    sheets = get_sheets_service()
    spreadsheet_id = get_spreadsheet_id()
    result = sheets.values().get(spreadsheetId=spreadsheet_id, range=f'{sheet_name}!A1:Z').execute()
    values = result.get('values', [])
    if not values:
        return pd.DataFrame()
    return pd.DataFrame(values[1:], columns=values[0])

async def append_to_sheet(sheet_name, values):
    sheets = get_sheets_service()
    spreadsheet_id = get_spreadsheet_id()
    await asyncio.to_thread(
        sheets.values().append,
        spreadsheetId=spreadsheet_id,
        range=f'{sheet_name}!A1',
        valueInputOption='RAW',
        body={'values': [values]}
    )
    read_sheet.clear()

async def update_sheet(sheet_name, row_index, values):
    sheets = get_sheets_service()
    spreadsheet_id = get_spreadsheet_id()
    await asyncio.to_thread(
        sheets.values().update,
        spreadsheetId=spreadsheet_id,
        range=f'{sheet_name}!A{row_index}',
        valueInputOption='RAW',
        body={'values': [values]}
    )
    read_sheet.clear()

async def delete_from_sheet(sheet_name, row_index):
    sheets = get_sheets_service()
    spreadsheet_id = get_spreadsheet_id()
    await asyncio.to_thread(
        sheets.batchUpdate,
        spreadsheetId=spreadsheet_id,
        body={
            "requests": [
                {
                    "deleteDimension": {
                        "range": {
                            "sheetId": get_sheet_id(sheet_name),
                            "dimension": "ROWS",
                            "startIndex": row_index - 1,
                            "endIndex": row_index
                        }
                    }
                }
            ]
        }
    )
    read_sheet.clear()

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_sheet_id(sheet_name):
    sheets = get_sheets_service()
    spreadsheet_id = get_spreadsheet_id()
    sheet_metadata = sheets.get(spreadsheetId=spreadsheet_id).execute()
    for sheet in sheet_metadata['sheets']:
        if sheet['properties']['title'] == sheet_name:
            return sheet['properties']['sheetId']
    return None