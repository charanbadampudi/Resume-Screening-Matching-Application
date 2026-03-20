# 📄 AI-Powered Resume Screening & Matching System

<div align="center">

**Intelligent Resume Screening Application with Advanced NLP Capabilities**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg)](https://streamlit.io/)
[![spaCy](https://img.shields.io/badge/spaCy-3.5+-09A3D5.svg)](https://spacy.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

</div>

---

## 🎯 Overview

An intelligent, enterprise-grade resume screening application that revolutionizes the recruitment process using cutting-edge Natural Language Processing (NLP) techniques. The system automatically extracts, preprocesses, and intelligently matches resumes with job descriptions, providing comprehensive insights through advanced skill gap analysis and interactive visual analytics.

### 🌟 Key Features

- **📄 Multi-format Resume Parsing** - Seamless support for PDF, DOCX, and TXT formats
- **🤖 Intelligent Skill Extraction** - Automatic identification of technical, soft, and domain-specific skills
- **🎯 Advanced Job Matching** - Sophisticated algorithms using TF-IDF, cosine similarity, and weighted scoring
- **📊 Interactive Visual Analytics** - Dynamic dashboards with Plotly visualizations
- **🔍 Comprehensive Skill Gap Analysis** - Identify missing skills and training recommendations
- **📦 Batch Processing** - Efficiently process multiple resumes simultaneously
- **📈 Trend Analysis** - Track skill demands and recruitment metrics over time
- **💾 Export Capabilities** - Download matching results in CSV format for further analysis
- **🎨 Modern UI** - Clean, professional interface with custom styling
- **🔒 Secure Processing** - File validation and secure handling

---

## 📋 Prerequisites

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **OS** | Windows 10 / macOS 11 / Ubuntu 20.04 | Windows 11 / macOS 13 / Ubuntu 22.04 |
| **RAM** | 4 GB | 8 GB+ |
| **Storage** | 2 GB free | 5 GB+ free |
| **Python** | 3.8 | 3.9-3.11 |
| **Internet** | Required for initial setup | Broadband connection |

### Software Dependencies

- Python 3.8 or higher
- pip package manager
- Git (optional, for cloning)
- Modern web browser (Chrome/Firefox/Safari recommended)

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/resume-screening-app.git
cd resume-screening-app
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger'); nltk.download('maxent_ne_chunker'); nltk.download('words')"

# Download spaCy model
python -m spacy download en_core_web_sm
```

### 4. Run the Application

```bash
streamlit run app.py
```

### 5. Access the Application

Open your browser and navigate to:
```
http://localhost:8501
```

---

## 📁 Project Structure

```
resume-screening-app/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── setup.sh                    # Setup script for Unix
├── install.bat                 # Installation script for Windows
├── .gitignore                  # Git ignore file
├── README.md                   # This file
├── CONTRIBUTING.md             # Contributing guidelines
├── LICENSE                     # MIT License
│
├── utils/
│   ├── __init__.py
│   ├── text_processor.py       # Text preprocessing functions
│   ├── resume_parser.py        # Resume extraction logic
│   └── matcher.py              # Matching algorithms
│
├── models/
│   ├── __init__.py
│   ├── skill_extractor.py      # Skill extraction model
│   └── trained_model.pkl       # Pre-trained model (optional)
│
├── assets/
│   ├── style.css               # Custom styling
│   ├── demo-screenshot.png     # Application screenshot
│   └── logo.svg                # Application logo
│
├── data/
│   ├── uploads/                # Uploaded resumes (gitignored)
│   ├── processed/              # Processed files (gitignored)
│   ├── output/                 # Output files (gitignored)
│   └── skill_database.json     # Skill categories database
│
├── tests/
│   ├── test_parser.py          # Unit tests for parser
│   ├── test_matcher.py         # Unit tests for matcher
│   └── test_extractor.py       # Unit tests for extractor
│
└── docs/
    ├── api.md                  # API documentation
    ├── deployment.md           # Deployment guide
    └── troubleshooting.md      # Troubleshooting guide
```

---

## 🎮 How to Use

### 1. Single Resume Screening

1. **Select Mode**: Choose "Single Resume Screening" from the sidebar
2. **Upload Resume**: Drag & drop or click to upload a resume (PDF, DOCX, or TXT)
3. **Input Job Description**: 
   - Paste directly into the text area
   - Upload a job description file
   - Select from predefined templates
4. **Adjust Threshold**: Set the matching threshold using the slider
5. **View Results**: 
   - Overall match percentage
   - Skills match score
   - Experience match score
   - Education match score
6. **Analyze Gaps**: 
   - Matching skills list
   - Missing skills list
   - Extra skills identified
7. **Get Recommendations**: Personalized improvement suggestions

### 2. Batch Processing

1. **Select Mode**: Choose "Batch Processing" from the sidebar
2. **Upload Multiple Resumes**: Select multiple files (PDF, DOCX, or TXT)
3. **Input Job Description**: Provide the job requirements
4. **Process**: Click "Process All Resumes"
5. **Review Results**: 
   - Sort by match percentage
   - Filter by threshold
   - Compare candidates
6. **Export**: Download results as CSV for further analysis

### 3. Analytics Dashboard

1. **Select Mode**: Choose "Analytics Dashboard" from the sidebar
2. **View Metrics**:
   - Application trends over time
   - Skill demand analysis
   - Department-wise statistics
   - Match distribution charts
3. **Filter Data**: 
   - By date range
   - By department
   - By skill category
4. **Export Reports**: Download analytics reports

### 4. Skill Gap Analysis

1. **Select Mode**: Choose "Skill Gap Analysis" from the sidebar
2. **Enter Required Skills**: Input comma-separated list of required skills
3. **Enter Candidate Skills**: Input candidate's skills
4. **View Analysis**:
   - Matching skills (green)
   - Missing skills (red)
   - Extra skills (yellow)
5. **Get Recommendations**: 
   - Training suggestions
   - Learning resources
   - Certification recommendations

### 5. Settings & Configuration

- **Adjust Weights**: Customize scoring weights (skills, experience, education)
- **Skill Database**: Add/modify skill categories
- **Threshold Settings**: Set default matching thresholds
- **Export Settings**: Configure output formats

---

## 🧠 How It Works

### Text Processing Pipeline

```
Raw Resume
    ↓
Text Extraction (PDF/DOCX/TXT)
    ↓
Cleaning (Remove special characters, extra spaces)
    ↓
Tokenization (Split into words/tokens)
    ↓
Stop Words Removal (Remove common words)
    ↓
Lemmatization (Convert to base form)
    ↓
Part-of-Speech Tagging
    ↓
Named Entity Recognition
    ↓
Feature Extraction (TF-IDF Vectors)
    ↓
Matching & Scoring
```

### Matching Algorithm

```python
# Weighted Scoring Formula
Total Score = (
    Skills Match × 0.50 +
    Text Similarity × 0.30 +
    Experience Match × 0.10 +
    Education Match × 0.10
) × 100
```

### Scoring Weights

| Component | Weight | Description |
|-----------|--------|-------------|
| **Skills Match** | 50% | Direct skill matches from resume |
| **Text Similarity** | 30% | TF-IDF cosine similarity |
| **Experience Match** | 10% | Years of experience comparison |
| **Education Match** | 10% | Education level matching |

---

## 📊 Features in Detail

### Skill Categories

| Category | Examples |
|----------|----------|
| **Programming Languages** | Python, Java, JavaScript, C++, Go, Rust, Ruby |
| **Frameworks** | Django, React, Spring, Angular, Vue.js, Flask |
| **Databases** | MySQL, PostgreSQL, MongoDB, Redis, Cassandra |
| **Cloud Platforms** | AWS, Azure, GCP, Heroku, DigitalOcean |
| **DevOps Tools** | Docker, Kubernetes, Jenkins, GitLab CI, Terraform |
| **Soft Skills** | Communication, Leadership, Teamwork, Problem-solving |
| **Data Science** | Machine Learning, NLP, Computer Vision, Statistics |
| **Certifications** | PMP, AWS Certified, CISSP, Scrum Master |

### Matching Results Include

- **Overall Match Percentage** - Comprehensive score
- **Skills Match Score** - Percentage of skills matched
- **Experience Match Score** - Experience level comparison
- **Education Match Score** - Education level match
- **Matching Skills List** - Skills found in resume
- **Missing Skills List** - Skills needed but missing
- **Extra Skills List** - Additional skills identified
- **Detailed Recommendations** - Personalized improvement suggestions
- **Training Resources** - Learning materials for missing skills

### Visual Analytics

- **Match Distribution Histogram** - Distribution of match scores
- **Skill Cloud** - Most frequent skills visualization
- **Trend Lines** - Skill demand over time
- **Department Comparison** - Match scores by department
- **Time Series Analysis** - Application volume trends
- **Heat Maps** - Skill correlation analysis

---

## 🔧 Configuration

### Adjust Matching Threshold

```python
# In app.py sidebar
matching_threshold = st.slider(
    "Matching Threshold (%)",
    min_value=0,
    max_value=100,
    value=70,
    help="Minimum match percentage to consider a candidate"
)
```

### Customize Scoring Weights

```python
# In utils/matcher.py
weights = {
    'skills': 0.50,      # Skills match weight
    'text': 0.30,        # Text similarity weight
    'experience': 0.10,  # Experience match weight
    'education': 0.10    # Education match weight
}
```

### Modify Skill Database

Edit `models/skill_extractor.py`:

```python
self.skill_database = {
    'programming_languages': ['python', 'java', 'javascript', ...],
    'frameworks': ['django', 'react', 'spring', ...],
    'databases': ['mysql', 'postgresql', 'mongodb', ...],
    'cloud': ['aws', 'azure', 'gcp', ...],
    'devops': ['docker', 'kubernetes', 'jenkins', ...],
    'soft_skills': ['communication', 'leadership', ...],
    # Add your custom categories
    'custom_category': ['skill1', 'skill2', ...]
}
```

### Add New File Formats

```python
# In utils/resume_parser.py
SUPPORTED_FORMATS = {
    '.pdf': parse_pdf,
    '.docx': parse_docx,
    '.txt': parse_txt,
    '.odt': parse_odt,      # Add ODT support
    '.rtf': parse_rtf        # Add RTF support
}
```

---

## 📈 Performance Metrics

| Metric | Value | Description |
|--------|-------|-------------|
| **Processing Speed** | ~2 seconds/resume | Average processing time per resume |
| **Skill Extraction Accuracy** | ~85% | Accuracy of skill identification |
| **Batch Capacity** | 100+ resumes | Maximum batch processing capacity |
| **File Size Limit** | 10MB | Maximum file size per resume |
| **Memory Usage** | ~500MB | Average memory consumption |
| **CPU Usage** | ~30% | Average CPU utilization |

---

## 🛠️ Troubleshooting

### Common Issues & Solutions

#### 1. **ModuleNotFoundError: No module named 'streamlit'**
```bash
pip install streamlit
# or
python -m pip install streamlit
```

#### 2. **PDF Parsing Errors**
```bash
pip install --upgrade PyPDF2
pip install pdfplumber  # Alternative parser
```

#### 3. **DOCX Parsing Errors**
```bash
pip install --upgrade python-docx
```

#### 4. **NLTK Data Missing**
```bash
python -c "import nltk; nltk.download('all')"
```

#### 5. **spaCy Model Not Found**
```bash
python -m spacy download en_core_web_sm
# or for larger model
python -m spacy download en_core_web_lg
```

#### 6. **Streamlit Port Already in Use**
```bash
streamlit run app.py --server.port 8502
```

#### 7. **Memory Issues with Large Files**
```python
# In app.py, limit file size
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

if uploaded_file.size > MAX_FILE_SIZE:
    st.error("File too large. Maximum size is 10MB")
```

### Virtual Environment Tips

**Windows:**
```bash
# Create
python -m venv venv

# Activate
venv\Scripts\activate

# Deactivate
deactivate

# Delete (if needed)
rmdir /s venv
```

**Mac/Linux:**
```bash
# Create
python3 -m venv venv

# Activate
source venv/bin/activate

# Deactivate
deactivate

# Delete (if needed)
rm -rf venv
```

---

## 🚀 Deployment

### Local Deployment

```bash
# Production mode
streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false
```

### Cloud Deployment

#### Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy

#### Heroku

```bash
# Create Procfile
echo "web: sh setup.sh && streamlit run app.py" > Procfile

# Deploy
heroku create resume-screening-app
git push heroku main
```

#### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/resume-screening-app.git

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Run linting
flake8 utils/ models/
```

### Contribution Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Areas for Improvement

- [ ] Add support for more file formats (ODT, RTF)
- [ ] Implement deep learning-based matching
- [ ] Add user authentication system
- [ ] Create REST API endpoints
- [ ] Integrate with job boards (LinkedIn, Indeed)
- [ ] Add email notification system
- [ ] Implement interview scheduling
- [ ] Add multi-language support
- [ ] Create mobile app version
- [ ] Add video interview integration

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Streamlit** for the amazing web framework
- **spaCy** for industrial-strength NLP
- **NLTK** for comprehensive natural language tools
- **scikit-learn** for machine learning algorithms
- **PyPDF2** for PDF parsing
- **python-docx** for DOCX parsing

---

## 📧 Contact & Support

- **Maintainer**: Charan Badampudi
- **Email**: charanbadampudi7@gmail.com

---

