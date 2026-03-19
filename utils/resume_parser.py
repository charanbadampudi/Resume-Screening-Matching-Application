import PyPDF2
import docx
import io
import re
from typing import Dict, Any
import PyPDF2
import io
import re
from typing import Dict, Any, Optional, List
import logging

# Try to import docx with error handling
try:
    import docx
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False
    print("Warning: python-docx not installed. DOCX files will not be supported.")

class ResumeParser:
    def __init__(self):
        """Initialize the resume parser"""
        pass
    
    def parse(self, file) -> str:
        """
        Parse resume file and extract text
        Supports PDF, DOCX, and TXT formats
        """
        if file is None:
            return ""
        
        file_extension = file.name.split('.')[-1].lower()
        
        try:
            if file_extension == 'pdf':
                return self._parse_pdf(file)
            elif file_extension == 'docx':
                return self._parse_docx(file)
            elif file_extension == 'txt':
                return self._parse_txt(file)
            else:
                return "Unsupported file format"
        except Exception as e:
            return f"Error parsing file: {str(e)}"
    
    def _parse_pdf(self, file) -> str:
        """
        Extract text from PDF file
        """
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        text = ""
        
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        return text
    
    def _parse_docx(self, file) -> str:
        """
        Extract text from DOCX file
        """
        doc = docx.Document(io.BytesIO(file.read()))
        text = ""
        
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        
        return text
    
    def _parse_txt(self, file) -> str:
        """
        Extract text from TXT file
        """
        return file.read().decode('utf-8')
    
    def extract_contact_info(self, text: str) -> Dict[str, Any]:
        """
        Extract contact information from resume text
        """
        contact_info = {
            'name': '',
            'email': '',
            'phone': '',
            'location': '',
            'linkedin': '',
            'github': ''
        }
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact_info['email'] = emails[0]
        
        # Extract phone
        phone_pattern = r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
        phones = re.findall(phone_pattern, text)
        if phones:
            contact_info['phone'] = phones[0]
        
        # Extract LinkedIn
        linkedin_pattern = r'(?:https?://)?(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+/?'
        linkedin = re.findall(linkedin_pattern, text, re.IGNORECASE)
        if linkedin:
            contact_info['linkedin'] = linkedin[0]
        
        # Extract GitHub
        github_pattern = r'(?:https?://)?(?:www\.)?github\.com/[A-Za-z0-9_-]+/?'
        github = re.findall(github_pattern, text, re.IGNORECASE)
        if github:
            contact_info['github'] = github[0]
        
        return contact_info
    
    def extract_education(self, text: str) -> list:
        """
        Extract education information
        """
        education = []
        
        # Common education keywords
        education_keywords = [
            'bachelor', 'master', 'phd', 'b.sc', 'm.sc', 'b.tech', 'm.tech',
            'b.e', 'm.e', 'mba', 'b.a', 'm.a', 'high school', 'diploma',
            'university', 'college', 'institute', 'school'
        ]
        
        lines = text.split('\n')
        current_education = {}
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # Check if line contains education keywords
            for keyword in education_keywords:
                if keyword in line_lower:
                    if current_education:
                        education.append(current_education)
                    
                    current_education = {
                        'institution': line.strip(),
                        'degree': '',
                        'field': '',
                        'dates': '',
                        'description': ''
                    }
                    
                    # Try to extract more details from next lines
                    for j in range(1, 4):
                        if i + j < len(lines):
                            next_line = lines[i + j].strip()
                            if next_line:
                                if not current_education['degree']:
                                    current_education['degree'] = next_line
                                elif not current_education['field']:
                                    current_education['field'] = next_line
                    
                    break
        
        if current_education:
            education.append(current_education)
        
        return education
    
    def extract_experience(self, text: str) -> list:
        """
        Extract work experience information
        """
        experience = []
        
        # Split into sections
        lines = text.split('\n')
        current_exp = {}
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Look for date patterns (e.g., "2020 - Present", "Jan 2020 - Dec 2021")
            date_pattern = r'\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)?\s?\d{4}\s*(?:-|to|–)\s*(?:(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)?\s?\d{4}|present|current)\b'
            dates = re.findall(date_pattern, line.lower())
            
            if dates and not current_exp:
                # This might be a new experience entry
                current_exp = {
                    'company': '',
                    'position': '',
                    'dates': line,
                    'description': []
                }
                
                # Get company name from previous line if available
                if i > 0:
                    prev_line = lines[i - 1].strip()
                    if prev_line:
                        current_exp['company'] = prev_line
                
                # Get position from next line
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if next_line and not re.findall(date_pattern, next_line.lower()):
                        current_exp['position'] = next_line
                        
            elif current_exp:
                # Collect description
                current_exp['description'].append(line)
                
                # Check if we've reached the end of this experience
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    next_has_date = bool(re.findall(date_pattern, next_line.lower()))
                    if next_has_date or i == len(lines) - 1:
                        experience.append(current_exp)
                        current_exp = {}
        
        return experience