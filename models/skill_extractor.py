import re
from typing import List, Set, Dict, Tuple, Optional
import logging

class SkillExtractor:
    def __init__(self):
        """Initialize the skill extractor with a comprehensive skill database"""
        self.logger = logging.getLogger(__name__)
        self.skill_database = self._load_skill_database()
        self.skill_patterns = self._compile_skill_patterns()
    
    def _load_skill_database(self) -> Dict[str, List[str]]:
        """
        Load comprehensive skill database
        """
        return {
            'programming_languages': [
                'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift',
                'kotlin', 'typescript', 'go', 'rust', 'scala', 'perl', 'r',
                'matlab', 'sql', 'html', 'css', 'sass', 'less', 'bash', 'shell',
                'powershell', 'groovy', 'dart', 'lua', 'haskell', 'clojure'
            ],
            'frameworks': [
                'django', 'flask', 'spring', 'spring boot', 'react', 'react.js',
                'angular', 'angular.js', 'vue', 'vue.js', 'node.js', 'nodejs',
                'express', 'express.js', 'tensorflow', 'pytorch', 'keras',
                'scikit-learn', 'sklearn', 'pandas', 'numpy', 'hadoop', 'spark',
                'kafka', 'rails', 'laravel', 'asp.net', 'jquery', 'bootstrap',
                'tailwind', 'sass', 'less', 'redux', 'next.js', 'nuxt.js'
            ],
            'databases': [
                'mysql', 'postgresql', 'postgres', 'mongodb', 'oracle', 'sql server',
                'redis', 'elasticsearch', 'cassandra', 'dynamodb', 'firebase',
                'couchdb', 'neo4j', 'mariadb', 'sqlite', 'cassandra', 'hbase',
                'teradata', 'snowflake', 'redshift', 'bigquery'
            ],
            'cloud_platforms': [
                'aws', 'amazon web services', 'azure', 'microsoft azure', 
                'google cloud', 'gcp', 'google cloud platform', 'heroku',
                'digital ocean', 'digitalocean', 'ibm cloud', 'oracle cloud',
                'cloudflare', 'netlify', 'vercel', 'openshift'
            ],
            'devops_tools': [
                'docker', 'kubernetes', 'k8s', 'jenkins', 'git', 'github',
                'gitlab', 'bitbucket', 'ansible', 'terraform', 'puppet',
                'chef', 'circleci', 'travis ci', 'travis', 'prometheus',
                'grafana', 'elk', 'elastic stack', 'splunk', 'nagios',
                'zabbix', 'vagrant', 'packer', 'consul', 'vault'
            ],
            'soft_skills': [
                'communication', 'teamwork', 'leadership', 'problem solving',
                'problem-solving', 'critical thinking', 'time management',
                'adaptability', 'creativity', 'collaboration', 'project management',
                'agile', 'scrum', 'kanban', 'presentation', 'negotiation',
                'mentoring', 'coaching', 'conflict resolution', 'emotional intelligence',
                'empathy', 'active listening', 'decision making', 'strategic thinking'
            ],
            'data_science': [
                'machine learning', 'ml', 'deep learning', 'dl', 'nlp',
                'natural language processing', 'computer vision', 'cv',
                'statistics', 'data analysis', 'data visualization',
                'tableau', 'power bi', 'excel', 'spss', 'sas', 'r',
                'big data', 'etl', 'data warehousing', 'data mining',
                'predictive modeling', 'forecasting', 'a/b testing',
                'experimental design', 'hypothesis testing', 'regression'
            ],
            'certifications': [
                'aws certified', 'azure certified', 'google certified',
                'pmp', 'project management professional', 'scrum master',
                'csm', 'psm', 'cissp', 'ceh', 'ccna', 'ccnp',
                'comptia', 'itil', 'prince2', 'six sigma', 'cfa', 'cpa',
                'security+', 'network+', 'a+', 'aws solutions architect',
                'aws developer', 'aws sysops', 'azure administrator'
            ]
        }
    
    def _compile_skill_patterns(self) -> List[Tuple[re.Pattern, str, str]]:
        """
        Compile regex patterns for skill matching
        Returns list of tuples (pattern, category, skill)
        """
        patterns = []
        
        for category, skills in self.skill_database.items():
            for skill in skills:
                # Escape special characters and create word boundary pattern
                escaped = re.escape(skill)
                pattern = re.compile(r'\b' + escaped + r'\b', re.IGNORECASE)
                patterns.append((pattern, category, skill))
        
        return patterns
    
    def extract_skills(self, text: str) -> Set[str]:
        """
        Extract skills from text using pattern matching
        """
        if not text or not isinstance(text, str):
            return set()
        
        found_skills = set()
        text_lower = text.lower()
        
        # Check each pattern
        for pattern, category, skill in self.skill_patterns:
            if pattern.search(text_lower):
                found_skills.add(skill)
        
        # Also check for skills with common variations (fuzzy matching)
        for category, skills in self.skill_database.items():
            for skill in skills:
                if self._fuzzy_match(skill, text_lower) and skill not in found_skills:
                    # Check if it's a reasonable match (not just a substring)
                    if len(skill) > 3 or skill in text_lower.split():
                        found_skills.add(skill)
        
        self.logger.debug(f"Extracted {len(found_skills)} skills from text")
        return found_skills
    
    def _fuzzy_match(self, skill: str, text: str) -> bool:
        """
        Simple fuzzy matching for skills
        """
        # Direct match
        if skill in text:
            return True
        
        # Check for skill with common variations
        skill_variations = self._get_skill_variations(skill)
        for variation in skill_variations:
            if variation in text:
                return True
        
        # For multi-word skills, check if words appear in proximity
        skill_words = skill.split()
        if len(skill_words) > 1:
            # Check if all words appear in the text
            words_found = 0
            for word in skill_words:
                if word in text:
                    words_found += 1
            
            # If most words are found, consider it a match
            if words_found >= len(skill_words) - 1:
                return True
        
        return False
    
    def _get_skill_variations(self, skill: str) -> List[str]:
        """
        Get common variations of a skill
        """
        variations = []
        
        # Remove dots (e.g., c++ -> c)
        if '+' in skill:
            variations.append(skill.replace('++', '').replace('+', ''))
        
        # Add common abbreviations
        if 'machine learning' in skill:
            variations.append('ml')
        if 'natural language processing' in skill:
            variations.append('nlp')
        if 'computer vision' in skill:
            variations.append('cv')
        if 'deep learning' in skill:
            variations.append('dl')
        
        # Handle hyphenated terms
        if '-' in skill:
            variations.append(skill.replace('-', ' '))
            variations.append(skill.replace('-', ''))
        
        # Handle spaces
        if ' ' in skill:
            variations.append(skill.replace(' ', ''))
            variations.append(skill.replace(' ', '_'))
        
        return variations
    
    def categorize_skills(self, skills: Set[str]) -> Dict[str, List[str]]:
        """
        Categorize extracted skills
        """
        categorized = {category: [] for category in self.skill_database.keys()}
        
        for skill in skills:
            for category, category_skills in self.skill_database.items():
                if skill in category_skills or any(
                    self._fuzzy_match(skill, cat_skill) for cat_skill in category_skills
                ):
                    categorized[category].append(skill)
                    break
        
        return categorized
    
    def get_skill_recommendations(self, current_skills: Set[str], target_role: str) -> List[str]:
        """
        Recommend skills based on current skills and target role
        """
        # Role-specific skill requirements
        role_requirements = {
            'data_scientist': [
                'python', 'r', 'sql', 'machine learning', 'statistics',
                'tensorflow', 'pytorch', 'pandas', 'numpy', 'data visualization',
                'scikit-learn', 'deep learning', 'nlp', 'big data', 'spark'
            ],
            'software_engineer': [
                'java', 'python', 'javascript', 'sql', 'git', 'docker',
                'spring', 'react', 'aws', 'agile', 'rest apis', 'microservices',
                'data structures', 'algorithms', 'system design'
            ],
            'devops_engineer': [
                'docker', 'kubernetes', 'jenkins', 'aws', 'linux',
                'python', 'bash', 'ansible', 'terraform', 'git',
                'ci/cd', 'monitoring', 'prometheus', 'grafana'
            ],
            'product_manager': [
                'agile', 'scrum', 'jira', 'product strategy', 'market research',
                'user stories', 'roadmap planning', 'stakeholder management',
                'analytics', 'a/b testing', 'user experience', 'competitive analysis'
            ],
            'data_engineer': [
                'python', 'sql', 'spark', 'hadoop', 'kafka',
                'airflow', 'etl', 'data warehousing', 'aws', 'azure',
                'databases', 'data modeling', 'big data', 'redshift'
            ],
            'frontend_developer': [
                'javascript', 'html', 'css', 'react', 'angular', 'vue',
                'typescript', 'webpack', 'responsive design', 'ui/ux',
                'frontend', 'bootstrap', 'tailwind', 'sass'
            ],
            'backend_developer': [
                'python', 'java', 'node.js', 'sql', 'rest apis', 'django',
                'spring', 'microservices', 'docker', 'aws', 'databases'
            ]
        }
        
        # Normalize role name
        role_key = target_role.lower().replace(' ', '_')
        
        # Get requirements for target role (default to empty list if role not found)
        required = role_requirements.get(role_key, [])
        
        # If role not found, try to find similar role
        if not required:
            for key in role_requirements.keys():
                if role_key in key or key in role_key:
                    required = role_requirements[key]
                    break
        
        # If still not found, use default skills
        if not required:
            required = [
                'communication', 'teamwork', 'problem solving',
                'python', 'sql', 'git', 'agile'
            ]
        
        # Find missing skills (case-insensitive comparison)
        current_skills_lower = {skill.lower() for skill in current_skills}
        missing = []
        
        for skill in required:
            if skill.lower() not in current_skills_lower:
                # Check if it's a close match
                is_present = False
                for current in current_skills:
                    if self._fuzzy_match(skill.lower(), current.lower()):
                        is_present = True
                        break
                
                if not is_present:
                    missing.append(skill)
        
        return missing[:10]  # Return top 10 missing skills
    
    def get_skill_frequency(self, resumes_text: List[str]) -> Dict[str, int]:
        """
        Calculate skill frequency across multiple resumes
        """
        skill_frequency = {}
        
        for text in resumes_text:
            skills = self.extract_skills(text)
            for skill in skills:
                skill_frequency[skill] = skill_frequency.get(skill, 0) + 1
        
        return dict(sorted(skill_frequency.items(), key=lambda x: x[1], reverse=True))
    
    def extract_skill_levels(self, text: str, skills: Set[str]) -> Dict[str, str]:
        """
        Extract proficiency levels for skills (beginner, intermediate, advanced)
        """
        skill_levels = {}
        text_lower = text.lower()
        
        level_patterns = {
            'advanced': ['advanced', 'expert', 'proficient', 'senior', 'lead', 'principal'],
            'intermediate': ['intermediate', 'medium', 'working knowledge', 'familiar'],
            'beginner': ['beginner', 'basic', 'fundamental', 'learning', 'junior']
        }
        
        for skill in skills:
            # Look for skill near level indicators
            skill_index = text_lower.find(skill.lower())
            if skill_index != -1:
                # Check surrounding context (100 characters before and after)
                start = max(0, skill_index - 100)
                end = min(len(text_lower), skill_index + len(skill) + 100)
                context = text_lower[start:end]
                
                # Determine level
                level = 'unknown'
                for lvl, patterns in level_patterns.items():
                    if any(pattern in context for pattern in patterns):
                        level = lvl
                        break
                
                skill_levels[skill] = level
        
        return skill_levels