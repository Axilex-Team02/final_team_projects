import sqlite3

def create_database():
    conn = sqlite3.connect('contractor.db')
    cursor = conn.cursor()

    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'admin'
        )
    ''')

    # Electricians Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Electricians (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            status TEXT DEFAULT 'Available'
        )
    ''')

    # Jobs Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            assigned_electrician_id INTEGER,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY (assigned_electrician_id) REFERENCES Electricians (id)
        )
    ''')

    # Tasks Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'Incomplete',
            FOREIGN KEY (job_id) REFERENCES Jobs (id)
        )
    ''')
    
    # Insert a default admin user if not exists
    cursor.execute("SELECT * FROM Users WHERE username='admin'")
    if not cursor.fetchone():
        # Using a simple raw password for demonstration; hashed passwords in real app
        from werkzeug.security import generate_password_hash
        hashed_pw = generate_password_hash('admin123')
        cursor.execute("INSERT INTO Users (username, email, password, role) VALUES (?, ?, ?, ?)", ('admin', 'admin@example.com', hashed_pw, 'admin'))

    # Insert some dummy electricians
    cursor.execute("SELECT COUNT(*) FROM Electricians")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO Electricians (name, phone, email, status) VALUES (?, ?, ?, ?)", [
            ('John Doe', '555-0101', 'john@example.com', 'Available'),
            ('Jane Smith', '555-0102', 'jane@example.com', 'Busy')
        ])

    conn.commit()
    conn.close()
    print("Database contractor.db created successfully.")

if __name__ == '__main__':
    create_database()
