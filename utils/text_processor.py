import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import spacy
from typing import Dict, List, Set, Tuple, Optional
import logging

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')

class TextProcessor:
    def __init__(self):
        """Initialize the text processor with NLP models"""
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except:
            import subprocess
            subprocess.run(['python', '-m', 'spacy', 'download', 'en_core_web_sm'])
            self.nlp = spacy.load('en_core_web_sm')
        
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
    def clean_text(self, text):
        """
        Clean and preprocess text
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize(self, text):
        """
        Tokenize text into words
        """
        return word_tokenize(text)
    
    def remove_stopwords(self, tokens):
        """
        Remove stopwords from tokens
        """
        return [token for token in tokens if token not in self.stop_words]
    
    def lemmatize(self, tokens):
        """
        Lemmatize tokens
        """
        return [self.lemmatizer.lemmatize(token) for token in tokens]
    
    def extract_entities(self, text):
        """
        Extract named entities using spaCy
        """
        doc = self.nlp(text)
        entities = {
            'PERSON': [],
            'ORG': [],
            'GPE': [],
            'DATE': [],
            'SKILL': []
        }
        
        for ent in doc.ents:
            if ent.label_ in entities:
                entities[ent.label_].append(ent.text)
        
        return entities
    
    def extract_sections(self, text):
        """
        Extract common resume sections
        """
        sections = {
            'education': '',
            'experience': '',
            'skills': '',
            'projects': '',
            'certifications': ''
        }
        
        # Define section patterns
        patterns = {
            'education': r'(?i)(education|academic background|qualifications?)[\s\n]+(.*?)(?=\n\s*\n|\n\s*[A-Z][a-z]+:|$)',
            'experience': r'(?i)(experience|work history|employment)[\s\n]+(.*?)(?=\n\s*\n|\n\s*[A-Z][a-z]+:|$)',
            'skills': r'(?i)(skills?|technical skills|competencies)[\s\n]+(.*?)(?=\n\s*\n|\n\s*[A-Z][a-z]+:|$)',
            'projects': r'(?i)(projects?|personal projects)[\s\n]+(.*?)(?=\n\s*\n|\n\s*[A-Z][a-z]+:|$)',
            'certifications': r'(?i)(certifications?|licenses)[\s\n]+(.*?)(?=\n\s*\n|\n\s*[A-Z][a-z]+:|$)'
        }
        
        for section, pattern in patterns.items():
            match = re.search(pattern, text, re.DOTALL)
            if match:
                sections[section] = match.group(2).strip()
        
        return sections
    
    def extract_emails(self, text):
        """
        Extract email addresses from text
        """
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(email_pattern, text)
    
    def extract_phone_numbers(self, text):
        """
        Extract phone numbers from text
        """
        phone_pattern = r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
        return re.findall(phone_pattern, text)
    
    def calculate_readability(self, text):
        """
        Calculate readability scores
        """
        sentences = nltk.sent_tokenize(text)
        words = self.tokenize(text)
        
        if not sentences or not words:
            return 0
        
        avg_sentence_length = len(words) / len(sentences)
        return min(100, avg_sentence_length * 10)  # Simplified score
    
    def get_keywords(self, text, top_n=10):
        """
        Extract key keywords using TF-IDF like approach
        """
        # Simple frequency based keyword extraction
        words = self.tokenize(text.lower())
        words = self.remove_stopwords(words)
        
        freq_dist = nltk.FreqDist(words)
        return freq_dist.most_common(top_n)