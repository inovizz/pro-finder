from db_setup import setup_db, Session
from sqlalchemy import text

def populate_dummy_data():
    setup_db()  # Ensure the database setup is done before populating data

    session = Session()
    
    # Dummy data for contractors
    contractors_data = [
        ("John Doe", "1234567890", "New York", "Plumbing", "Great work on fixing the pipes."),
        ("Jane Smith", "0987654321", "Los Angeles", "Tiles", "Excellent tiling job."),
        ("Mike Johnson", "5555555555", "Chicago", "False Ceiling", "Very professional and timely."),
        ("Sara Lee", "4444444444", "Houston", "Mesh Door", "Good quality mesh door installed."),
        ("Tom Hanks", "3333333333", "Phoenix", "Painting", "Fantastic painting work."),
    ]

    # Dummy data for service suggestions
    suggestions_data = [
        ("SolarPanelInstallation", "Alice Green", "2222222222", "San Francisco", 500.0, "Looking for a professional solar panel installer."),
        ("WindowCleaning", "Bob Brown", "1111111111", "San Diego", 75.0, "Need a reliable window cleaner."),
        ("GardenLandscaping", "Charlie Black", "6666666666", "Dallas", 400.0, "Want to redesign my garden."),
    ]

    # Insert dummy data into contractors table
    for contractor in contractors_data:
        session.execute(text('''
            INSERT INTO contractors (name, number, city, service, feedback) VALUES (:name, :number, :city, :service, :feedback)
        '''), {"name": contractor[0], "number": contractor[1], "city": contractor[2], "service": contractor[3], "feedback": contractor[4]})

    # Insert dummy data into service suggestions table
    for suggestion in suggestions_data:
        session.execute(text('''
            INSERT INTO service_suggestions (suggested_service, name, number, city, price, feedback) VALUES (:suggested_service, :name, :number, :city, :price, :feedback)
        '''), {"suggested_service": suggestion[0], "name": suggestion[1], "number": suggestion[2], "city": suggestion[3], "price": suggestion[4], "feedback": suggestion[5]})
    
    session.commit()
    session.close()

if __name__ == "__main__":
    populate_dummy_data()
