import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import base64
import io
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import re

# Import custom modules
from utils.text_processor import TextProcessor
from utils.resume_parser import ResumeParser
from utils.matcher import ResumeMatcher
from models.skill_extractor import SkillExtractor

# Page configuration
st.set_page_config(
    page_title="AI Resume Screening & Matching System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def load_css():
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .success-text {
        color: #28a745;
        font-weight: bold;
    }
    .warning-text {
        color: #ffc107;
        font-weight: bold;
    }
    .danger-text {
        color: #dc3545;
        font-weight: bold;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize components
@st.cache_resource
def init_components():
    text_processor = TextProcessor()
    resume_parser = ResumeParser()
    skill_extractor = SkillExtractor()
    matcher = ResumeMatcher()
    return text_processor, resume_parser, skill_extractor, matcher

def main():
    # Load CSS
    load_css()
    
    # Initialize components
    text_processor, resume_parser, skill_extractor, matcher = init_components()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📄 AI-Powered Resume Screening & Matching System</h1>
        <p>Intelligent resume parsing and job matching using advanced NLP techniques</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/resume.png", width=100)
        st.title("Navigation")
        option = st.radio(
            "Choose Mode",
            ["Single Resume Screening", "Batch Processing", "Analytics Dashboard", "Skill Gap Analysis"]
        )
        
        st.markdown("---")
        st.subheader("⚙️ Settings")
        
        matching_threshold = st.slider(
            "Matching Threshold (%)",
            min_value=0,
            max_value=100,
            value=70,
            step=5
        )
        
        use_advanced_nlp = st.checkbox("Use Advanced NLP", value=True)
        show_skill_gaps = st.checkbox("Show Skill Gaps", value=True)
        
        st.markdown("---")
        st.markdown("### 📊 Statistics")
        st.info("Processed: 0 resumes")
        st.info("Match Rate: 0%")
    
    # Main content area
    if option == "Single Resume Screening":
        single_resume_screening(text_processor, resume_parser, skill_extractor, matcher, matching_threshold)
    
    elif option == "Batch Processing":
        batch_processing(text_processor, resume_parser, skill_extractor, matcher, matching_threshold)
    
    elif option == "Analytics Dashboard":
        analytics_dashboard()
    
    elif option == "Skill Gap Analysis":
        skill_gap_analysis(skill_extractor)

def single_resume_screening(text_processor, resume_parser, skill_extractor, matcher, threshold):
    st.header("🎯 Single Resume Screening")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Upload Resume")
        resume_file = st.file_uploader(
            "Choose a resume file",
            type=['pdf', 'docx', 'txt'],
            help="Upload resume in PDF, DOCX, or TXT format"
        )
        
        if resume_file:
            st.success(f"✅ Uploaded: {resume_file.name}")
            
            # Parse resume
            with st.spinner("Parsing resume..."):
                resume_text = resume_parser.parse(resume_file)
                cleaned_text = text_processor.clean_text(resume_text)
                skills = skill_extractor.extract_skills(cleaned_text)
                
                # Display resume preview
                with st.expander("📝 Resume Preview"):
                    st.text(resume_text[:500] + "..." if len(resume_text) > 500 else resume_text)
    
    with col2:
        st.subheader("💼 Job Description")
        jd_option = st.radio(
            "Job Description Input Method",
            ["Paste Text", "Upload File", "Select Template"]
        )
        
        job_description = ""
        
        if jd_option == "Paste Text":
            job_description = st.text_area(
                "Paste job description here",
                height=300,
                placeholder="Paste the job description..."
            )
        
        elif jd_option == "Upload File":
            jd_file = st.file_uploader(
                "Upload job description",
                type=['pdf', 'docx', 'txt']
            )
            if jd_file:
                job_description = resume_parser.parse(jd_file)
        
        else:  # Select Template
            templates = {
                "Data Scientist": "Looking for a Data Scientist with experience in Python, ML, and Statistics...",
                "Software Engineer": "Seeking a Software Engineer proficient in Java, Spring Boot, and Microservices...",
                "Product Manager": "Need a Product Manager with Agile experience and technical background..."
            }
            selected_template = st.selectbox("Select Template", list(templates.keys()))
            job_description = templates[selected_template]
            st.info(job_description)
    
    # Perform matching if both inputs are available
    if resume_file and job_description:
        st.markdown("---")
        st.subheader("📊 Matching Results")
        
        # Process job description
        cleaned_jd = text_processor.clean_text(job_description)
        jd_skills = skill_extractor.extract_skills(cleaned_jd)
        
        # Calculate matches
        match_results = matcher.calculate_match(cleaned_text, cleaned_jd, skills, jd_skills)
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Overall Match",
                f"{match_results['overall_score']}%",
                delta=f"{match_results['overall_score'] - 50}% vs avg"
            )
        
        with col2:
            st.metric(
                "Skills Match",
                f"{match_results['skills_score']}%",
                delta=f"{match_results['skills_match_count']} skills"
            )
        
        with col3:
            st.metric(
                "Experience Match",
                f"{match_results['experience_score']}%",
                delta="Good fit" if match_results['experience_score'] > 70 else "Needs improvement"
            )
        
        with col4:
            st.metric(
                "Education Match",
                f"{match_results['education_score']}%",
                delta="✓" if match_results['education_match'] else "✗"
            )
        
        # Detailed analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("✅ Matching Skills")
            matching_skills = match_results['matching_skills']
            if matching_skills:
                for skill in matching_skills:
                    st.markdown(f"✓ {skill}")
            else:
                st.warning("No matching skills found")
        
        with col2:
            st.subheader("❌ Missing Skills")
            missing_skills = match_results['missing_skills']
            if missing_skills:
                for skill in missing_skills:
                    st.markdown(f"✗ {skill}")
            else:
                st.success("All required skills found!")
        
        # Visualization
        st.subheader("📈 Match Visualization")
        
        fig = go.Figure()
        
        categories = ['Skills', 'Experience', 'Education', 'Overall']
        values = [
            match_results['skills_score'],
            match_results['experience_score'],
            match_results['education_score'],
            match_results['overall_score']
        ]
        
        fig.add_trace(go.Bar(
            x=categories,
            y=values,
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'],
            text=[f'{v}%' for v in values],
            textposition='auto',
        ))
        
        fig.update_layout(
            title="Match Score Breakdown",
            yaxis_range=[0, 100],
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendation
        st.subheader("💡 Recommendation")
        
        if match_results['overall_score'] >= threshold:
            st.success(f"✅ Strong Candidate! (Score: {match_results['overall_score']}%)")
            st.markdown("This candidate shows strong potential for the role. Consider scheduling an interview.")
        elif match_results['overall_score'] >= threshold - 20:
            st.warning(f"⚠️ Potential Candidate (Score: {match_results['overall_score']}%)")
            st.markdown("This candidate has some relevant skills but may need additional training.")
        else:
            st.error(f"❌ Not a Good Match (Score: {match_results['overall_score']}%)")
            st.markdown("This candidate doesn't meet the minimum requirements for the position.")

def batch_processing(text_processor, resume_parser, skill_extractor, matcher, threshold):
    st.header("📦 Batch Resume Processing")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📁 Upload Multiple Resumes")
        resume_files = st.file_uploader(
            "Choose resume files",
            type=['pdf', 'docx', 'txt'],
            accept_multiple_files=True,
            help="Upload multiple resumes for batch processing"
        )
    
    with col2:
        st.subheader("💼 Job Description")
        job_description = st.text_area(
            "Paste job description for batch matching",
            height=200,
            placeholder="Paste the job description to match against all resumes..."
        )
    
    if resume_files and job_description:
        if st.button("🚀 Process All Resumes"):
            with st.spinner("Processing resumes..."):
                results = []
                progress_bar = st.progress(0)
                
                # Process job description
                cleaned_jd = text_processor.clean_text(job_description)
                jd_skills = skill_extractor.extract_skills(cleaned_jd)
                
                for i, resume_file in enumerate(resume_files):
                    # Parse resume
                    resume_text = resume_parser.parse(resume_file)
                    cleaned_text = text_processor.clean_text(resume_text)
                    skills = skill_extractor.extract_skills(cleaned_text)
                    
                    # Calculate match
                    match_results = matcher.calculate_match(cleaned_text, cleaned_jd, skills, jd_skills)
                    
                    results.append({
                        'Resume Name': resume_file.name,
                        'Overall Score': match_results['overall_score'],
                        'Skills Score': match_results['skills_score'],
                        'Experience Score': match_results['experience_score'],
                        'Education Score': match_results['education_score'],
                        'Matching Skills': ', '.join(match_results['matching_skills'][:5]),
                        'Missing Skills': ', '.join(match_results['missing_skills'][:5]),
                        'Status': 'Selected' if match_results['overall_score'] >= threshold else 'Rejected'
                    })
                    
                    progress_bar.progress((i + 1) / len(resume_files))
                
                # Create DataFrame
                df_results = pd.DataFrame(results)
                df_results = df_results.sort_values('Overall Score', ascending=False)
                
                # Display results
                st.subheader("📊 Batch Processing Results")
                
                # Summary metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Resumes", len(df_results))
                
                with col2:
                    selected = len(df_results[df_results['Status'] == 'Selected'])
                    st.metric("Selected", selected, f"{(selected/len(df_results))*100:.1f}%")
                
                with col3:
                    avg_score = df_results['Overall Score'].mean()
                    st.metric("Average Score", f"{avg_score:.1f}%")
                
                with col4:
                    max_score = df_results['Overall Score'].max()
                    st.metric("Highest Score", f"{max_score}%")
                
                # Display table
                st.dataframe(
                    df_results.style.apply(
                        lambda x: ['background: lightgreen' if v == 'Selected' else 'background: lightcoral' 
                                 for v in x] if x.name == 'Status' else [''] * len(x),
                        axis=0
                    ),
                    use_container_width=True
                )
                
                # Download results
                csv = df_results.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv,
                    file_name=f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
                # Visualization
                st.subheader("📈 Score Distribution")
                
                fig = px.histogram(
                    df_results, 
                    x='Overall Score',
                    nbins=20,
                    title="Distribution of Match Scores",
                    labels={'Overall Score': 'Match Score (%)'},
                    color_discrete_sequence=['#667eea']
                )
                
                fig.add_vline(x=threshold, line_dash="dash", line_color="red")
                st.plotly_chart(fig, use_container_width=True)

def analytics_dashboard():
    st.header("📊 Analytics Dashboard")
    
    # Sample data for demonstration
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', end='2024-03-31', freq='D')
    
    # Create sample data
    sample_data = pd.DataFrame({
        'Date': dates,
        'Applications': np.random.poisson(lam=15, size=len(dates)),
        'Matches': np.random.poisson(lam=8, size=len(dates)),
        'Interviews': np.random.poisson(lam=3, size=len(dates))
    })
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Applications",
            f"{sample_data['Applications'].sum():,}",
            delta="+12.5%"
        )
    
    with col2:
        match_rate = (sample_data['Matches'].sum() / sample_data['Applications'].sum()) * 100
        st.metric(
            "Match Rate",
            f"{match_rate:.1f}%",
            delta="+3.2%"
        )
    
    with col3:
        interview_rate = (sample_data['Interviews'].sum() / sample_data['Matches'].sum()) * 100
        st.metric(
            "Interview Rate",
            f"{interview_rate:.1f}%",
            delta="-1.8%"
        )
    
    with col4:
        avg_time = 5.2
        st.metric(
            "Avg Processing Time",
            f"{avg_time} days",
            delta="-0.5 days"
        )
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Application Trends")
        
        # Daily applications
        fig = px.line(
            sample_data,
            x='Date',
            y=['Applications', 'Matches', 'Interviews'],
            title="Daily Application Metrics",
            labels={'value': 'Count', 'variable': 'Metric'},
            color_discrete_map={
                'Applications': '#667eea',
                'Matches': '#4CAF50',
                'Interviews': '#FF9800'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Skill Demand Analysis")
        
        # Sample skill demand
        skills = ['Python', 'Java', 'SQL', 'Machine Learning', 'AWS', 'JavaScript', 'React', 'Docker']
        demand = np.random.randint(50, 200, size=len(skills))
        
        fig = px.bar(
            x=demand,
            y=skills,
            orientation='h',
            title="Top Skills in Demand",
            labels={'x': 'Number of Job Postings', 'y': 'Skills'},
            color=demand,
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Department analysis
    st.subheader("🏢 Department-wise Analysis")
    
    dept_data = pd.DataFrame({
        'Department': ['Engineering', 'Data Science', 'Product', 'Marketing', 'Sales'],
        'Applications': np.random.randint(100, 500, 5),
        'Hired': np.random.randint(10, 50, 5),
        'Open Positions': np.random.randint(5, 30, 5)
    })
    
    fig = go.Figure(data=[
        go.Bar(name='Applications', x=dept_data['Department'], y=dept_data['Applications']),
        go.Bar(name='Hired', x=dept_data['Department'], y=dept_data['Hired']),
        go.Bar(name='Open Positions', x=dept_data['Department'], y=dept_data['Open Positions'])
    ])
    
    fig.update_layout(
        title="Recruitment by Department",
        barmode='group',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def skill_gap_analysis(skill_extractor):
    st.header("🔍 Skill Gap Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💼 Required Skills")
        required_skills = st.text_area(
            "Enter required skills (comma-separated)",
            height=150,
            placeholder="e.g., Python, Machine Learning, SQL, AWS"
        )
    
    with col2:
        st.subheader("📄 Candidate Skills")
        candidate_skills = st.text_area(
            "Enter candidate skills (comma-separated)",
            height=150,
            placeholder="e.g., Python, Java, React, Docker"
        )
    
    if required_skills and candidate_skills:
        # Parse skills
        required_set = set([s.strip() for s in required_skills.split(',')])
        candidate_set = set([s.strip() for s in candidate_skills.split(',')])
        
        # Calculate gaps
        matching_skills = required_set.intersection(candidate_set)
        missing_skills = required_set - candidate_set
        extra_skills = candidate_set - required_set
        
        # Display results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Matching Skills", len(matching_skills))
            
            if matching_skills:
                st.subheader("✅ Present")
                for skill in matching_skills:
                    st.markdown(f"✓ {skill}")
        
        with col2:
            st.metric("Missing Skills", len(missing_skills))
            
            if missing_skills:
                st.subheader("❌ Missing")
                for skill in missing_skills:
                    st.markdown(f"✗ {skill}")
        
        with col3:
            st.metric("Extra Skills", len(extra_skills))
            
            if extra_skills:
                st.subheader("➕ Additional")
                for skill in extra_skills:
                    st.markdown(f"+ {skill}")
        
        # Skill gap visualization
        st.subheader("📊 Skill Gap Visualization")
        
        # Create radar chart
        categories = ['Match', 'Gap', 'Extra']
        values = [len(matching_skills), len(missing_skills), len(extra_skills)]
        
        fig = go.Figure(data=[
            go.Bar(
                name='Skill Analysis',
                x=categories,
                y=values,
                marker_color=['#4CAF50', '#F44336', '#2196F3'],
                text=values,
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Skill Gap Analysis",
            yaxis_title="Number of Skills",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations
        st.subheader("💡 Recommendations")
        
        if len(missing_skills) == 0:
            st.success("🎉 Perfect match! The candidate has all required skills.")
        else:
            st.warning(f"⚠️ The candidate is missing {len(missing_skills)} skills. Consider training or looking for candidates with these skills.")
            
            # Training recommendations
            st.markdown("**Suggested Training:**")
            for skill in missing_skills:
                st.markdown(f"- {skill}: [Find courses](https://www.google.com/search?q=learn+{skill.replace(' ', '+')})")

if __name__ == "__main__":
    main()