import os
import re
import spacy
import streamlit as st
import PyPDF2
from dotenv import load_dotenv
import google.generativeai as genai
from spacy.matcher import Matcher

# Import custom resume parsing utilities
from module.resume_parser.utils import (
    extract_name, extract_text, extract_education,
    extract_email, extract_mobile_number, extract_skills
)

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load NLP model
nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)

def extract_text_from_pdf(uploaded_file):
    """Extracts text from an uploaded PDF file."""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = "".join(page.extract_text() or "" for page in pdf_reader.pages)
    return text.strip()

def generate_question(tech_stack, conversation_history, difficulty="easy"):
    """Generates a contextual technical question."""
    conversation_context = "\n".join([f"Q: {q}\nA: {a}" for q, a in conversation_history])
    prompt = f"""
    You are conducting a technical interview. Ask a {difficulty} technical question based on {tech_stack}.
    
    Previous conversation:
    {conversation_context}

    New question:
    """
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    
    return response.text.strip() if response.text else "No question generated."

def extract_experience_years_gemini(resume_text):
    """Extracts total years of experience using Gemini API."""
    prompt = f"""
    Extract the **total years of professional experience** from the following resume text, excluding internships and projects.
    **Resume Text:**
    {resume_text}
    """
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    
    try:
        extracted_years = re.search(r"\d+", response.text).group(0) if response.text else "0"
    except:
        extracted_years = "0"
    
    return extracted_years

# Streamlit UI
st.set_page_config(page_title="TalentScout Chatbot", layout="wide")
st.title("TalentScout Hiring Assistant")
st.sidebar.title("Candidate Information")

# Resume Upload
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"], key="resume")

if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)
    if not resume_text:
        st.error("Failed to extract text from PDF. Try a different file.")
    else:
        nlp_text = nlp(resume_text)
        noun_chunks = list(nlp_text.noun_chunks)
        
        name = extract_name(nlp_text, matcher)
        email = extract_email(resume_text)
        phone = extract_mobile_number(resume_text)
        skills = extract_skills(nlp_text, noun_chunks)
        education = extract_education(nlp_text)    
        years_of_experience = extract_experience_years_gemini(resume_text)
        
        # Sidebar: Candidate Info
        st.sidebar.write(f"**Full Name:** {name if name else 'N/A'}")
        st.sidebar.write(f"**Email:** {email[9:] if email else 'N/A'}")
        st.sidebar.write(f"**Phone:** {phone if phone else 'N/A'}")
        st.sidebar.write(f"**Experience:** {years_of_experience} years")
        st.sidebar.write(f"**Education:** {education if education else 'N/A'}")
        
        # Tech Stack Input
        tech_stack = st.text_area(
            "Enter your strongest tech stack:",
            ", ".join(skills) if skills else "",
            help="Example: Python, Django, PostgreSQL, Docker"
        )

        # Start Interview
        if st.button("Start Technical Interview") and tech_stack:
            if "interview" not in st.session_state:
                st.session_state.interview = {
                    "questions": [],
                    "responses": [],
                    "completed": False
                }
                first_question = generate_question(tech_stack, [])
                st.session_state.interview["questions"].append(first_question)
                st.session_state.current_question = first_question
            
        # Sidebar: Interview Progress
        if "interview" in st.session_state and st.session_state.interview["questions"]:
            st.sidebar.subheader("📌 Interview Progress")
            for idx, q in enumerate(st.session_state.interview["questions"]):
                st.sidebar.write(f"**Q{idx+1}:** {q}")
        
        # Main Interview Section
        if "current_question" in st.session_state and not st.session_state.interview["completed"]:
            st.subheader("Interview")
            st.write(st.session_state.current_question)
            user_response = st.text_area("Your response:", key="user_response")
            
            if st.button("Submit Response") and user_response:
                st.session_state.interview["responses"].append(user_response)
                

                if len(st.session_state.interview["questions"]) >= 5:
                    st.session_state.interview["completed"] = True
                    st.write("Interview completed! Thank you for participating.")
                else:
                    new_question = generate_question(
                        tech_stack,
                        list(zip(st.session_state.interview["questions"], st.session_state.interview["responses"]))
                    )
                    st.session_state.interview["questions"].append(new_question)
                    st.session_state.current_question = new_question
                    st.rerun()

        if st.session_state.get("interview", {}).get("completed"):
            st.success("Interview is complete! A recruiter will review your responses.")
