import os
import re
import pdfplumber
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from transformers import pipeline
import spacy

# Initialize Flask app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///candidates.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Load SpaCy model for Named Entity Recognition
nlp = spacy.load("en_core_web_sm")

# Define the Candidate model
class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    match_score = db.Column(db.Float, nullable=False)
    interview_status = db.Column(db.String(50), default="Not Yet Scheduled")

# Function to extract text from PDF (resume)
def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to extract name and email from resume text using regex
def extract_name_and_email(text):
    # Sample regex for email extraction
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    email_match = re.search(email_pattern, text)

    # Attempt to extract name based on simple heuristics (this could be improved further)
    name = "Not Extracted"
    if email_match:
        email = email_match.group(0)
        # Try to get name from the text by considering the text before the email
        name_pattern = r"(?:Name:|Full Name:)\s*(\w+\s*\w*)"
        name_match = re.search(name_pattern, text)
        if name_match:
            name = name_match.group(1)
    else:
        email = "Not Extracted"

    return name, email

# Function to calculate match score between resume and job description
def calculate_match_score(resume_text, jd_text):
    # Use a simple pipeline for text similarity using HuggingFace
    model = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')
    result = model(resume_text, candidate_labels=[jd_text])
    return result['scores'][0]

# Route for uploading resume and job description
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files or 'jd' not in request.files:
        return "Missing files", 400
    
    resume_file = request.files['resume']
    jd_file = request.files['jd']

    # Extract text from uploaded resume
    resume_text = extract_text_from_pdf(resume_file)

    # Extract name and email
    name, email = extract_name_and_email(resume_text)
    
    # Extract job description text
    jd_text = jd_file.read().decode("utf-8", errors="ignore")

    # Calculate the match score
    match_score = calculate_match_score(resume_text, jd_text)

    # Store the candidate in the database
    candidate = Candidate(
        name=name,  # Extracted name from resume
        email=email,  # Extracted email from resume
        match_score=match_score
    )

    db.session.add(candidate)
    db.session.commit()

    return render_template('shortlist.html', match_score=match_score)

# Route to display shortlisted candidates
@app.route('/shortlisted')
def shortlisted():
    candidates = Candidate.query.all()
    return render_template('shortlist.html', candidates=candidates)

# Run the Flask app
if __name__ == '__main__':
    db.create_all()  # Create database tables if not already created
    app.run(debug=True)
