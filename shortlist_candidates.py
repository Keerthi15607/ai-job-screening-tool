# shortlist_candidates.py
import spacy
from sklearn.metrics.pairwise import cosine_similarity

# Load spaCy model for text processing
nlp = spacy.load("en_core_web_sm")

def get_similarity_score(jd_text, candidate_text):
    """Calculate the similarity score between JD and candidate resume."""
    jd_doc = nlp(jd_text)
    candidate_doc = nlp(candidate_text)
    return cosine_similarity([jd_doc.vector], [candidate_doc.vector])[0][0]

def shortlist_candidates(jd_text, candidate_files):
    """Shortlist candidates based on similarity score."""
    shortlisted_candidates = []
    for candidate_file in candidate_files:
        with open(candidate_file, 'r') as file:
            candidate_text = file.read()
        similarity_score = get_similarity_score(jd_text, candidate_text)
        if similarity_score > 0.7:  # Adjust this threshold as needed
            shortlisted_candidates.append((candidate_file, similarity_score))
    return shortlisted_candidates
