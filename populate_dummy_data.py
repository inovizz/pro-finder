from db_setup import get_sheets_service
import asyncio

async def populate_dummy_data(spreadsheet_id):
    sheets = get_sheets_service()

    # Contractors data
    contractors_data = [
        ["Name", "Number", "City", "Service", "Feedback"],
        ["Shival", "9116339639", "Hyderabad", "Carpenter", "Good and reasonable but can do basic work not exposed to complex work yet."],
        ["Anil", "6306332342", "Hyderabad", "Painter", "Reasonable in rates"],
        ["Syed S", "9966851213", "Hyderabad", "Mesh Doors", "Good work and decent quality"],
    ]

    await asyncio.to_thread(
        sheets.values().update,
        spreadsheetId=spreadsheet_id,
        range='contractors!A1',
        valueInputOption='RAW',
        body={'values': contractors_data}
    )

    # Service suggestions data
    suggestions_data = [
        ["ID", "Suggested Service", "Name", "Number", "City", "Price", "Feedback"],
        [1, "Home Tutoring", "Sneha Gupta", "6543210987", "Chennai", "500.0", "Looking for a Math tutor for 10th standard."],
        [2, "Interior Design", "Vikram Singh", "5432109876", "Hyderabad", "10000.0", "Need help redesigning my living room."],
    ]

    await asyncio.to_thread(
        sheets.values().update,
        spreadsheetId=spreadsheet_id,
        range='service_suggestions!A1',
        valueInputOption='RAW',
        body={'values': suggestions_data}
    )

    # Services data
    services_data = [
        ["ID", "Service Name"],
        [1, "Plumbing"], [2, "Electrician"], [3, "Painting"], [4, "Carpentry"], [5, "AC Repair"],
        [6, "Pest Control"], [7, "Deep Cleaning"], [8, "Home Tutoring"], [9, "Packers Movers"],
        [10, "Tiling Work"], [11, "RO Service"], [12, "Geyser Repair"], [13, "Interior Design"],
        [14, "False Ceiling"], [15, "Home Salon"]
    ]

    await asyncio.to_thread(
        sheets.values().update,
        spreadsheetId=spreadsheet_id,
        range='services!A1',
        valueInputOption='RAW',
        body={'values': services_data}
    )

if __name__ == "__main__":
    from db_setup import get_spreadsheet_id, run_async
    run_async(populate_dummy_data(get_spreadsheet_id()))