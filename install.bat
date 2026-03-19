@echo off
echo ========================================
echo Resume Screening Application Installer
echo ========================================
echo.

echo Step 1: Upgrading pip...
python -m pip install --upgrade pip
echo.

echo Step 2: Installing required packages...
pip install numpy pandas streamlit scikit-learn nltk spacy PyPDF2 python-docx plotly matplotlib seaborn wordcloud Pillow typing-extensions protobuf
echo.

echo Step 3: Downloading NLTK data...
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger'); nltk.download('punkt_tab')"
echo.

echo Step 4: Downloading spaCy model...
python -m spacy download en_core_web_sm
echo.

echo Step 5: Checking Imports
python check_imports.py
echo.

echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo To run the application:
echo streamlit run app.py
echo.
pause