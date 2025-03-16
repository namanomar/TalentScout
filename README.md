# TalentScout Hiring Assistant Chatbot

## 🚀 Project Overview
The **TalentScout Hiring Assistant Chatbot** is an AI-powered recruitment assistant designed to streamline the hiring process. It allows candidates to upload resumes, extracts key details, and conducts an interactive technical interview based on the candidate's tech stack. The chatbot leverages **Google Gemini AI** for generating tailored technical questions and follow-ups, ensuring an engaging and personalized assessment experience.

## 🛠 Installation Instructions
Follow these steps to set up the project locally:

### 1️⃣ Prerequisites
- Python 3.8+
- Virtual environment (recommended)
- API Key for **Google Gemini AI**

### 2️⃣ Clone the Repository
```sh
 git clone https://github.com/namanomar/TalentScout.git
 cd TalentScout
```

### 3️⃣ Set Up Virtual Environment
```sh
 python -m venv venv
 source venv/bin/activate   # On macOS/Linux
 venv\Scripts\activate      # On Windows
```

### 4️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 5️⃣ Set Up Environment Variables
Create a `.env` file and add your **Google Gemini API Key**:
```env
GEMINI_API_KEY=your_api_key_here
```

### 6️⃣ Run the Application
```sh
streamlit run app.py
```

## 📖 Usage Guide
1. **Upload Resume:** Candidates upload a PDF resume.
2. **Resume Parsing:** Extracts name, email, phone, education, skills, and experience.
3. **Tech Stack Declaration:** Candidate specifies their strongest technologies.
4. **Technical Interview:**
   - The chatbot generates **3-5 AI-powered questions**.
   - Follows up based on responses.
   - Tracks interview progress in a side panel.
5. **Completion:** The chatbot summarizes responses, and a recruiter reviews them.

## ⚙️ Technical Details
### 🏗️ Tech Stack
- **Frontend:** Streamlit (UI)
- **Backend:** Python (Flask/Streamlit)
- **AI Model:** Google Gemini AI
- **NLP:** SpaCy, TextBlob
- **PDF Processing:** PyPDF2

### 🏛️ Architecture
- **Resume Parsing Module:** Extracts structured information from resumes.
- **Technical Question Generator:** Uses Gemini AI to create tailored questions.
- **Interactive Interview Flow:** Handles candidate responses and follow-ups.
- **Session Management:** Maintains conversation context using Streamlit session state.

## 🎯 Prompt Design
The prompts were designed to:
- Extract structured resume data efficiently.
- Generate **challenging and relevant** technical questions.
- Follow up naturally based on previous responses.
- Provide fallback responses for unexpected inputs.

## 🔥 Challenges & Solutions
### 🔴 **Handling Unstructured Resumes**
✅ Used **NLP models (SpaCy)** and regex-based extraction for better parsing accuracy.

### 🔴 **Generating Relevant Questions**
✅ Designed **context-aware prompts** for Gemini AI to generate tailored technical questions.

### 🔴 **Maintaining Conversation Flow**
✅ Used **session state** in Streamlit to store interview progress and responses dynamically.

## 📌 Future Enhancements
- 🏆 **Multiple AI Model Support** (GPT-4, Claude, Mistral, etc.)
- 📊 **Dashboard for Recruiters** (to view and analyze candidate responses)
- 🎙️ **Voice-Enabled Interviews**

---
**Developed with ❤️ by Naman Omar**