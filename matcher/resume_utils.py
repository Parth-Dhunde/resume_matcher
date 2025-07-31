from pdfminer.high_level import extract_text
from keybert import KeyBERT
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

kw_model = KeyBERT()

def extract_resume_text(pdf_path):
    try:
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        return ""

def extract_keywords(text, top_n=10):
    keywords = kw_model.extract_keywords(
        text, 
        keyphrase_ngram_range=(1, 2),
        stop_words='english', 
        top_n=top_n
    )
    return [kw[0] for kw in keywords]

def calculate_match_score(resume_keywords, job_keywords):
    vectorizer = CountVectorizer().fit_transform([
        ' '.join(resume_keywords),
        ' '.join(job_keywords)
    ])
    vectors = vectorizer.toarray()
    cosine = cosine_similarity(vectors)
    return round(cosine[0][1] * 100, 2)  # Return as percentage
