import os
import re
from pdfminer.high_level import extract_text
from keybert import KeyBERT
# from sklearn.feature_extraction.text import CountVectorizer  # Removed unused import
# from sklearn.metrics.pairwise import cosine_similarity  # Removed unused import

# Initialize KeyBERT with error handling
try:
    kw_model = KeyBERT()
    print("KeyBERT model loaded successfully")
except Exception as e:
    print(f"Error loading KeyBERT model: {e}")
    kw_model = None

# Keyword synonyms and weights
KEYWORD_SYNONYMS = {
    'javascript': ['js', 'ecmascript'],
    'python': ['py'],
    'react': ['reactjs', 'react.js'],
    'node': ['nodejs', 'node.js'],
    'aws': ['amazon web services', 'amazon'],
    'machine learning': ['ml', 'ai', 'artificial intelligence'],
    'data science': ['datascience', 'data scientist'],
    'frontend': ['front-end', 'front end'],
    'backend': ['back-end', 'back end'],
    'fullstack': ['full-stack', 'full stack'],
    'devops': ['dev ops', 'development operations'],
    'api': ['apis', 'application programming interface'],
    'sql': ['database', 'mysql', 'postgresql'],
    'git': ['github', 'gitlab', 'version control'],
    'docker': ['containerization', 'kubernetes'],
    'agile': ['scrum', 'kanban'],
    'ui': ['user interface', 'ux', 'user experience'],
    'testing': ['test', 'qa', 'quality assurance'],
    'cloud': ['aws', 'azure', 'gcp', 'google cloud'],
}

# Important keywords with higher weights
IMPORTANT_KEYWORDS = {
    'python': 2.0, 'javascript': 2.0, 'react': 2.0, 'node': 2.0,
    'aws': 2.0, 'machine learning': 2.0, 'data science': 2.0,
    'docker': 1.5, 'kubernetes': 1.5, 'git': 1.5, 'agile': 1.5,
    'api': 1.5, 'sql': 1.5, 'testing': 1.5, 'devops': 1.5,
}

def validate_pdf_file(file):
    """Validate PDF file size and type"""
    # Check file size (max 10MB)
    if file.size > 10 * 1024 * 1024:
        return False
    
    # Check file extension
    if not file.name.lower().endswith('.pdf'):
        return False
    
    # Check MIME type
    if not file.content_type == 'application/pdf':
        return False
    
    return True

def extract_resume_text(pdf_path):
    """Extract text from PDF with better error handling"""
    try:
        print(f"Extracting text from: {pdf_path}")
        text = extract_text(pdf_path)
        # Clean up text
        text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
        text = text.strip()
        print(f"Extracted text length: {len(text)}")
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""

def normalize_keyword(keyword):
    """Normalize keyword and check for synonyms"""
    keyword = keyword.lower().strip()
    
    # Check synonyms
    for main_keyword, synonyms in KEYWORD_SYNONYMS.items():
        if keyword in synonyms or keyword == main_keyword:
            return main_keyword
    
    return keyword

def extract_keywords_simple(text, top_n=15):
    """Simple keyword extraction as fallback"""
    # Basic keyword extraction using common words
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    
    # Filter out common stop words
    stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their', 'mine', 'yours', 'his', 'hers', 'ours', 'theirs'}
    
    # Count word frequencies
    word_freq = {}
    for word in words:
        if word not in stop_words and len(word) > 2:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Get top keywords
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    keywords = [word for word, freq in sorted_words[:top_n]]
    
    return keywords

def extract_keywords(text, top_n=15):
    """Extract keywords with enhanced processing and fallback"""
    if not text.strip():
        print("Empty text provided for keyword extraction")
        return []
    
    try:
        # Try KeyBERT first
        if kw_model is not None:
            print("Using KeyBERT for keyword extraction")
            keywords = kw_model.extract_keywords(
                text, 
                keyphrase_ngram_range=(1, 3),
                stop_words='english', 
                top_n=top_n,
                diversity=0.7
            )
            
            # Process and normalize keywords
            processed_keywords = []
            for kw, score in keywords:
                normalized = normalize_keyword(kw)
                if normalized and len(normalized) > 2:  # Filter out very short keywords
                    processed_keywords.append(normalized)
            
            # Remove duplicates while preserving order
            seen = set()
            unique_keywords = []
            for kw in processed_keywords:
                if kw not in seen:
                    seen.add(kw)
                    unique_keywords.append(kw)
            
            print(f"KeyBERT extracted {len(unique_keywords)} keywords")
            return unique_keywords[:top_n]
        else:
            print("KeyBERT not available, using simple extraction")
            return extract_keywords_simple(text, top_n)
        
    except Exception as e:
        print(f"Error in KeyBERT extraction: {e}")
        print("Falling back to simple keyword extraction")
        return extract_keywords_simple(text, top_n)

def calculate_match_score(resume_keywords, job_keywords):
    """Calculate match score with weighted scoring and enhanced analysis"""
    print(f"Calculating match score with {len(resume_keywords)} resume keywords and {len(job_keywords)} job keywords")
    
    if not job_keywords:
        print("No job keywords found")
        return 0.0, [], []
    
    resume_set = set([kw.lower() for kw in resume_keywords])
    job_set = set([kw.lower() for kw in job_keywords])
    
    # Find matched and missing keywords
    matched = resume_set & job_set
    missing = job_set - resume_set
    
    print(f"Matched keywords: {len(matched)}")
    print(f"Missing keywords: {len(missing)}")
    
    # Calculate weighted score
    total_weight = 0
    matched_weight = 0
    
    for keyword in job_keywords:
        weight = IMPORTANT_KEYWORDS.get(keyword.lower(), 1.0)
        total_weight += weight
        if keyword.lower() in matched:
            matched_weight += weight
    
    # Calculate percentage
    score = round((matched_weight / total_weight * 100), 2) if total_weight > 0 else 0.0
    
    print(f"Calculated score: {score}%")
    
    return score, list(matched), list(missing)

def get_keyword_category(keyword):
    """Categorize keywords for better visualization"""
    tech_keywords = ['python', 'javascript', 'react', 'node', 'aws', 'docker', 'git', 'sql', 'api']
    soft_skills = ['leadership', 'communication', 'teamwork', 'problem solving', 'agile', 'scrum']
    tools = ['docker', 'kubernetes', 'jenkins', 'gitlab', 'jira', 'confluence']
    
    keyword_lower = keyword.lower()
    
    if keyword_lower in tech_keywords:
        return 'technical'
    elif keyword_lower in soft_skills:
        return 'soft_skills'
    elif keyword_lower in tools:
        return 'tools'
    else:
        return 'other'
