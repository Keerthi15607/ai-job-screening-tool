import sqlite3

def create_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Create the shortlisted_candidates table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS shortlisted_candidates (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        match_score REAL NOT NULL,
                        interview_status TEXT DEFAULT 'Not Yet Scheduled')''')
    conn.commit()
    conn.close()

def insert_sample_data():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Sample candidates
    candidates = [
        ('Candidate 1', 'candidate1@example.com', 1.5, 'Not Yet Scheduled'),
        ('Candidate 2', 'candidate2@example.com', 3.0, 'Not Yet Scheduled'),
        ('Candidate 3', 'candidate3@example.com', 2.8, 'Not Yet Scheduled'),
        ('Candidate 4', 'candidate4@example.com', 3.5, 'Not Yet Scheduled')
    ]
    
    cursor.executemany("INSERT INTO shortlisted_candidates (name, email, match_score, interview_status) VALUES (?, ?, ?, ?)", candidates)
    conn.commit()
    conn.close()

# Create the table first
create_table()

# Then insert sample data
insert_sample_data()
