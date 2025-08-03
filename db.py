import mysql.connector

# Connect to the MySQL database
def connect_to_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="nishanth",
        database="movie_booking_db"
    )
    return conn

# Drop existing tables
def drop_tables(conn):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Tickets")
    conn.commit()
    cursor.close()

# Create the Tickets table
def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tickets (
            ticket_id VARCHAR(10) PRIMARY KEY,
            movie_name VARCHAR(100),
            available_tickets INT,
            ticket_price FLOAT
        )
    """)
    conn.commit()
    cursor.close()

# Clear all rows from the Tickets table
def clear_table(conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Tickets")
    conn.commit()
    cursor.close()

# Insert initial ticket records
def insert_tickets(conn):
    cursor = conn.cursor()
    tickets_data = [
        ('1', 'movie1', 3, 50),
        ('2', 'movie2', 2, 40),
        ('3', 'Movie3', 4, 60),
        ('4', 'Movie4', 5, 70),
        ('5', 'Movie5', 1, 65)
    ]
    cursor.executemany(
        "INSERT INTO Tickets (ticket_id, movie_name, available_tickets, ticket_price) VALUES (%s, %s, %s, %s)",
        tickets_data
    )
    conn.commit()
    cursor.close()

# Fetch all tickets
def get_tickets(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Tickets')
    tickets = cursor.fetchall()
    cursor.close()
    return tickets

# Update ticket quantity after booking
def update_quantity(conn, id, reserved_quantity):
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE Tickets SET available_tickets = available_tickets - %s WHERE ticket_id = %s',
        (reserved_quantity, id)
    )
    conn.commit()
    cursor.close()

# Sample execution (only runs when the file is executed directly)
if __name__ == "__main__":
    conn = connect_to_database()
    drop_tables(conn)         # Drop existing tables
    create_tables(conn)       # Create new table
    insert_tickets(conn)      # Insert initial ticket data
    tickets = get_tickets(conn)  # Retrieve tickets (optional use)
    update_quantity(conn, '1', 2)  # Update ticket quantity (example)
    conn.close()
