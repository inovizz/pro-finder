from db_setup import setup_db, Session
from sqlalchemy import text

def populate_dummy_data():
    setup_db()  # Ensure the database setup is done before populating data
    session = Session()

    # Actual data for contractors
    contractors_data = [
        ("Shival", "9116339639", "Hyderabad", "Carpenter", "Good and reasonable but can do basic work not exposed to complex work yet."),
        ("Anil", "6306332342", "Hyderabad", "Painter", "Reasonable in rates"),
        ("Syed S", "9966851213", "Hyderabad", "Mesh Doors", "Good work and decent quality"),
    ]

    # Insert actual data into contractors table
    for contractor in contractors_data:
        session.execute(text('''
            INSERT OR IGNORE INTO contractors (name, number, city, service, feedback) 
            VALUES (:name, :number, :city, :service, :feedback)
        '''), {"name": contractor[0], "number": contractor[1], "city": contractor[2], "service": contractor[3], "feedback": contractor[4]})

    # We'll keep the service suggestions as they were, but you can update or remove them if you prefer
    suggestions_data = [
        ("Home Tutoring", "Sneha Gupta", "6543210987", "Chennai", 500.0, "Looking for a Math tutor for 10th standard."),
        ("Interior Design", "Vikram Singh", "5432109876", "Hyderabad", 10000.0, "Need help redesigning my living room."),
    ]

    # Insert data into service suggestions table
    for suggestion in suggestions_data:
        session.execute(text('''
            INSERT OR IGNORE INTO service_suggestions (suggested_service, name, number, city, price, feedback) 
            VALUES (:suggested_service, :name, :number, :city, :price, :feedback)
        '''), {"suggested_service": suggestion[0], "name": suggestion[1], "number": suggestion[2], "city": suggestion[3], "price": suggestion[4], "feedback": suggestion[5]})

    session.commit()
    session.close()

if __name__ == "__main__":
    populate_dummy_data()