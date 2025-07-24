from dotenv import load_dotenv
import os
import streamlit as st
from PyPDF2 import PdfReader
import io
import google.generativeai as genai  # ✅ FIXED: Correct import for Gemini

# Load environment variable
load_dotenv()
GEMINI_API_KEY = "AIzaSyDiXGDknOkCmhxqFBiV_4mIJCOUjF7wLVM" # ✅ Safer than hardcoding

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Use the Gemini model
model = genai.GenerativeModel('gemini-2.5-flash')  # ✅ Use valid model name (like gemini-pro)

# Page Config for better UX
st.set_page_config(
    page_title="ATS Resume Checker",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="auto"
)

# Custom Styling
st.markdown("""
    <style>
        .title-style {
            text-align: center;
            font-size: 2.5rem;
            color: #4285F4;
            font-weight: bold;
            margin-bottom: 0;
        }
        .sub-style {
            text-align: center;
            font-size: 1rem;
            color: #5f6368;
            margin-top: 0;
        }
        .stButton>button {
            background-color: #4285F4;
            color: white;
            border-radius: 8px;
            padding: 10px 24px;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="title-style">ATS Resume Checker</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-style">Get insights & suggestions based on your resume and job description</p>', unsafe_allow_html=True)

# Streamlit Inputs
with st.form("ats_form"):
    job_description = st.text_area("📄 Paste the Job Description", height=200, placeholder="Enter job details here...")
    upload_file = st.file_uploader("📎 Upload Your Resume (PDF or TXT)", type=["pdf", "txt"])
    submitted = st.form_submit_button("🚀 Analyze Resume")

# PDF/Text to String
def pdf_to_data(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text(upload_file):
    file_type = upload_file.type
    if file_type == "application/pdf":
        with io.BytesIO(upload_file.read()) as file_bytes:
            return pdf_to_data(file_bytes)
    elif file_type == "text/plain":
        return upload_file.read().decode("utf-8")
    return ""

# Gemini Resume Analysis
def ATS_Resume_Score_and_Suggestion(upload_file, job_description):
    resume_data = extract_text(upload_file)

    content = f"""
You are an expert in Resume Screening and ATS Optimization.

Analyze the following job description and resume, and provide:

1. **Match Score** (0–100): Rate how well the resume aligns with the job description.

2. **Missing Keywords/Skills**: List critical skills, tools, technologies, or terms mentioned in the job description but missing in the resume.

3. **Role Alignment**: Assess how well the resume reflects the responsibilities and qualifications required for the role.

4. **Suggestions for Improvement**: Clearly list actionable improvements (e.g., add specific tools, mention frameworks, quantify impact, improve role relevance).

Avoid all general closing statements like "This will improve your chances" or "By doing this, the candidate will be more successful." Stick strictly to the analysis.

---
**Job Description**:
{job_description}

---
**Resume**:
{resume_data}
    """

    try:
        response = model.generate_content(content)
        output = response.text
    except Exception as e:
        output = f"❌ Error generating response: {str(e)}"

    st.markdown("### 📝 Analysis Report")
    st.markdown(output)

# Run Analysis
if submitted and job_description and upload_file:
    with st.spinner("🔍 Analyzing your resume... Please wait."):
        ATS_Resume_Score_and_Suggestion(upload_file, job_description)
elif submitted:
    st.warning("⚠️ Please make sure both Job Description and Resume are provided.")
    # Footer with credit and Instagram link
st.markdown("""
    <hr style="margin-top: 3rem; margin-bottom: 1rem;">
    <div style="text-align:center;">
        <p style="color: #5f6368; font-size: 0.95rem;">
            Made with ❤️ by <strong>Umang Patel</strong><br>
            <a href="https://www.instagram.com/_umangggg__/" target="_blank" style="text-decoration: none; color: #4285F4;">
                📸 Follow on Instagram
            </a>
        </p>
    </div>
""", unsafe_allow_html=True)

