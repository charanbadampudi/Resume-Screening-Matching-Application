import numpy as np  # This is correct - import numpy and alias it as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, Set, Tuple, List, Optional
import re
import logging

class ResumeMatcher:
    def __init__(self):
        """Initialize the matcher with TF-IDF vectorizer"""
        self.logger = logging.getLogger(__name__)
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
    
    # ... rest of the class remains the same

class ResumeMatcher:
    def __init__(self):
        """Initialize the matcher with TF-IDF vectorizer"""
        self.logger = logging.getLogger(__name__)
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
    
    def calculate_match(self, resume_text: str, jd_text: str, 
        resume_skills: Set[str], jd_skills: Set[str]) -> Dict:
        """
        Calculate match between resume and job description
        """
        # Ensure inputs are valid
        resume_text = resume_text or ""
        jd_text = jd_text or ""
        resume_skills = resume_skills or set()
        jd_skills = jd_skills or set()
        
        # Calculate skills match
        matching_skills = resume_skills.intersection(jd_skills)
        missing_skills = jd_skills - resume_skills
        
        skills_score = len(matching_skills) / len(jd_skills) * 100 if jd_skills else 0
        
        # Calculate text similarity
        text_similarity = self._calculate_text_similarity(resume_text, jd_text)
        
        # Calculate experience match
        experience_score = self._calculate_experience_match(resume_text, jd_text)
        
        # Calculate education match
        education_score, education_match = self._calculate_education_match(resume_text, jd_text)
        
        # Calculate overall score (weighted average)
        overall_score = (
            0.5 * skills_score +
            0.3 * text_similarity * 100 +
            0.1 * experience_score +
            0.1 * education_score
        )
        
        return {
            'overall_score': round(overall_score, 2),
            'skills_score': round(skills_score, 2),
            'text_similarity': round(text_similarity * 100, 2),
            'experience_score': round(experience_score, 2),
            'education_score': round(education_score, 2),
            'education_match': education_match,
            'matching_skills': list(matching_skills),
            'missing_skills': list(missing_skills),
            'skills_match_count': len(matching_skills),
            'skills_total_count': len(jd_skills)
        }
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate cosine similarity between two texts
        """
        try:
            if not text1 or not text2:
                return 0.0
                
            tfidf_matrix = self.vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            return similarity[0][0]
        except Exception as e:
            self.logger.error(f"Error calculating text similarity: {str(e)}")
            return 0.0
    
    def _calculate_experience_match(self, resume_text: str, jd_text: str) -> float:
        """
        Calculate experience match score
        """
        # Extract years of experience from resume
        resume_exp = self._extract_years_experience(resume_text)
        
        # Extract required experience from JD
        jd_exp = self._extract_years_experience(jd_text, is_requirement=True)
        
        if jd_exp == 0:
            return 100.0
        
        if resume_exp >= jd_exp:
            return 100.0
        elif resume_exp >= jd_exp * 0.8:
            return 80.0
        elif resume_exp >= jd_exp * 0.6:
            return 60.0
        elif resume_exp >= jd_exp * 0.4:
            return 40.0
        else:
            return 20.0
    
    def _extract_years_experience(self, text: str, is_requirement: bool = False) -> float:
        """
        Extract years of experience from text
        """
        if not text:
            return 0.0
            
        # Common patterns for experience
        patterns = [
            r'(\d+)\+?\s*years?.*experience',
            r'experience.*?(\d+)\+?\s*years?',
            r'(\d+)\s*years?',
            r'(\d+)\s*yr',
        ]
        
        if is_requirement:
            # For job descriptions, look for required experience
            patterns.extend([
                r'(\d+)\+?\s*years?.*required',
                r'minimum.*?(\d+)\s*years?',
                r'at least.*?(\d+)\s*years?'
            ])
        
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                # Return the highest number found
                try:
                    return float(max(matches))
                except:
                    continue
        
        return 0.0
    
    def _calculate_education_match(self, resume_text: str, jd_text: str) -> Tuple[float, bool]:
        """
        Calculate education match score
        """
        if not resume_text or not jd_text:
            return 50.0, False
            
        # Education level mapping
        education_levels = {
            'phd': 5,
            'doctorate': 5,
            'masters': 4,
            'master': 4,
            'mba': 4,
            'bachelors': 3,
            'bachelor': 3,
            'associate': 2,
            'high school': 1,
            'diploma': 1
        }
        
        # Extract education level from resume
        resume_level = 0
        for edu, level in education_levels.items():
            if edu in resume_text.lower():
                resume_level = max(resume_level, level)
        
        # Extract required education from JD
        jd_level = 0
        for edu, level in education_levels.items():
            if edu in jd_text.lower():
                jd_level = max(jd_level, level)
        
        if jd_level == 0:
            return 100.0, True
        
        if resume_level >= jd_level:
            return 100.0, True
        elif resume_level >= jd_level - 1:
            return 70.0, False
        else:
            return 30.0, False
    
    def rank_resumes(self, resumes: List[Dict], jd_text: str, 
                    jd_skills: Set[str]) -> List[Dict]:
        """
        Rank multiple resumes against a job description
        """
        if not resumes:
            return []
            
        ranked_resumes = []
        
        for resume in resumes:
            match_score = self.calculate_match(
                resume.get('text', ''), 
                jd_text, 
                resume.get('skills', set()), 
                jd_skills
            )
            
            ranked_resumes.append({
                'name': resume.get('name', 'Unknown'),
                'score': match_score['overall_score'],
                'skills_match': match_score['skills_match_count'],
                'missing_skills': match_score['missing_skills'],
                'details': match_score
            })
        
        # Sort by overall score
        ranked_resumes.sort(key=lambda x: x['score'], reverse=True)
        
        return ranked_resumes
    
    def calculate_batch_statistics(self, match_results: List[Dict]) -> Dict:
        """
        Calculate statistics from batch matching results
        """
        if not match_results:
            return {
                'total': 0,
                'average_score': 0,
                'median_score': 0,
                'std_deviation': 0,
                'max_score': 0,
                'min_score': 0,
                'top_10_percent': 0,
                'bottom_10_percent': 0
            }
            
        scores = [r['score'] for r in match_results]
        
        return {
            'total': len(match_results),
            'average_score': np.mean(scores),
            'median_score': np.median(scores),
            'std_deviation': np.std(scores),
            'max_score': np.max(scores),
            'min_score': np.min(scores),
            'top_10_percent': np.percentile(scores, 90),
            'bottom_10_percent': np.percentile(scores, 10)
        }