from app import app, db, Candidate

# Create an application context
with app.app_context():
    # Query all candidates in the database
    candidates = Candidate.query.all()

    # Print the details of the candidates
    for candidate in candidates:
        print(f"Name: {candidate.name}, Email: {candidate.email}, Match Score: {candidate.match_score}")
