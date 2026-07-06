import streamlit as st
from pdfminer.high_level import extract_text
import re
from io import BytesIO

# Common skills database
COMMON_SKILLS = {
    "programming": [
        "python", "java", "javascript", "c++", "c#", "ruby", "go", "rust", "php", "swift",
        "kotlin", "typescript", "html", "css", "sql", "r", "matlab", "perl", "scala"
    ],
    "tools": [
        "git", "docker", "kubernetes", "aws", "azure", "gcp", "jenkins", "jira", "confluence",
        "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy", "matplotlib",
        "react", "angular", "vue", "node.js", "django", "flask", "spring", "postgresql",
        "mysql", "mongodb", "redis", "elasticsearch"
    ],
    "soft_skills": [
        "communication", "teamwork", "leadership", "problem solving", "critical thinking",
        "time management", "adaptability", "creativity", "collaboration", "organization"
    ]
}

# Job role recommendations based on skills
JOB_ROLES = {
    "Data Scientist": ["python", "sql", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch"],
    "Software Engineer": ["python", "java", "javascript", "git", "docker", "sql"],
    "Web Developer": ["html", "css", "javascript", "react", "angular", "node.js"],
    "DevOps Engineer": ["docker", "kubernetes", "aws", "azure", "git", "jenkins"],
    "Data Analyst": ["python", "sql", "pandas", "excel", "matplotlib"],
    "Machine Learning Engineer": ["python", "tensorflow", "pytorch", "scikit-learn", "sql"]
}

def extract_text_from_pdf(uploaded_file):
    """Extract text from uploaded PDF file"""
    text = extract_text(BytesIO(uploaded_file.read()))
    return text

def extract_skills(text):
    """Extract skills from resume text"""
    skills = {
        "programming": [],
        "tools": [],
        "soft_skills": []
    }
    
    text_lower = text.lower()
    
    for category, skill_list in COMMON_SKILLS.items():
        for skill in skill_list:
            # Check for skill as whole word
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                skills[category].append(skill.title())
    
    return skills

def recommend_job_roles(skills):
    """Recommend job roles based on extracted skills"""
    recommendations = []
    
    all_skills = [s.lower() for category in skills.values() for s in category]
    
    for role, required_skills in JOB_ROLES.items():
        matching_skills = [skill for skill in required_skills if skill in all_skills]
        match_percentage = len(matching_skills) / len(required_skills) * 100
        
        if match_percentage > 0:
            recommendations.append({
                "role": role,
                "matching_skills": matching_skills,
                "match_percentage": match_percentage
            })
    
    # Sort by match percentage
    recommendations.sort(key=lambda x: x["match_percentage"], reverse=True)
    return recommendations

def suggest_improvements(skills, recommendations):
    """Suggest skills to improve based on job recommendations"""
    suggestions = []
    
    if not recommendations:
        return suggestions
    
    top_role = recommendations[0]
    required_skills = JOB_ROLES[top_role["role"]]
    current_skills = [s.lower() for category in skills.values() for s in category]
    
    missing_skills = [skill for skill in required_skills if skill not in current_skills]
    
    for skill in missing_skills:
        suggestions.append({
            "skill": skill.title(),
            "for_role": top_role["role"]
        })
    
    return suggestions

def main():
    st.set_page_config(page_title="AI Resume Analyzer", page_icon="🧠", layout="wide")
    
    # Add custom CSS
    st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stProgress > div > div > div {
        background-color: #4CAF50;
    }
    .skill-badge {
        display: inline-block;
        background-color: #e3f2fd;
        color: #1976d2;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-weight: 500;
    }
    .tool-badge {
        display: inline-block;
        background-color: #fff3e0;
        color: #e65100;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-weight: 500;
    }
    .soft-badge {
        display: inline-block;
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-weight: 500;
    }
    .missing-badge {
        display: inline-block;
        background-color: #ffebee;
        color: #c62828;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🧠 AI-Based Resume Analyzer & Skill Gap Detector")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("📄 Upload Resume")
        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
        st.divider()
        st.markdown("### ✨ Key Features")
        st.markdown("""
        - 📄 PDF Resume Upload
        - 🧠 Skill Extraction
        - 🎯 Job Recommendations
        - 📈 Skill Gap Detection
        - 📊 Match Scores
        """)
    
    if uploaded_file is not None:
        with st.spinner("🔍 Analyzing your resume..."):
            # Extract text
            resume_text = extract_text_from_pdf(uploaded_file)
            
            # Extract skills
            skills = extract_skills(resume_text)
            
            # Recommend job roles
            job_recommendations = recommend_job_roles(skills)
            
            # Suggest improvements
            improvements = suggest_improvements(skills, job_recommendations)
        
        st.success("✅ Analysis complete!")
        
        # Display results
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📋 Extracted Skills")
            
            st.markdown("#### 💻 Programming Languages")
            if skills["programming"]:
                badges_html = " ".join([f'<span class="skill-badge">{s}</span>' for s in skills["programming"]])
                st.markdown(badges_html, unsafe_allow_html=True)
            else:
                st.info("No programming languages found")
            
            st.markdown("#### 🔧 Tools & Technologies")
            if skills["tools"]:
                badges_html = " ".join([f'<span class="tool-badge">{s}</span>' for s in skills["tools"]])
                st.markdown(badges_html, unsafe_allow_html=True)
            else:
                st.info("No tools/technologies found")
            
            st.markdown("#### 🤝 Soft Skills")
            if skills["soft_skills"]:
                badges_html = " ".join([f'<span class="soft-badge">{s}</span>' for s in skills["soft_skills"]])
                st.markdown(badges_html, unsafe_allow_html=True)
            else:
                st.info("No soft skills found")
        
        with col2:
            st.subheader("🎯 Job Role Recommendations")
            
            if job_recommendations:
                for idx, rec in enumerate(job_recommendations[:3], 1):
                    with st.container(border=True):
                        st.markdown(f"### {idx}. {rec['role']}")
                        st.progress(rec['match_percentage'] / 100)
                        col_match, col_skills = st.columns([1, 2])
                        with col_match:
                            st.metric(label="Match", value=f"{int(rec['match_percentage'])}%")
                        with col_skills:
                            st.write("**Matching Skills:**")
                            badges_html = " ".join([f'<span class="skill-badge">{s.title()}</span>' for s in rec['matching_skills']])
                            st.markdown(badges_html, unsafe_allow_html=True)
            else:
                st.info("No job recommendations found")
        
        st.divider()
        
        st.subheader("📈 Suggestions for Improvement")
        if improvements:
            st.write("Consider learning these skills for your top recommended role:")
            badges_html = " ".join([f'<span class="missing-badge">{imp["skill"]}</span>' for imp in improvements])
            st.markdown(badges_html, unsafe_allow_html=True)
        else:
            st.success("🎉 Great job! Your skills are well-aligned with the top recommended role!")
        
        st.divider()
        
        with st.expander("📄 View Extracted Resume Text"):
            st.text_area("", resume_text, height=300)
    
    else:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.info("👆 Please upload a PDF resume using the sidebar to start analyzing!")
            
            st.markdown("## 📊 How it works")
            st.markdown("""
            1. Upload your resume (PDF format)
            2. AI extracts your skills
            3. Get job role recommendations
            4. Identify skill gaps to improve
            """)

if __name__ == "__main__":
    main()
