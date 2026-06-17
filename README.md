# RecruitAI-End-to-End-AI-Hiring-Assistant
# Overview

RecruitAI is an AI-powered recruitment platform that automates the complete hiring lifecycle using Large Language Models (LLMs), Speech AI, Computer Vision, Vector Databases, and Multi-Agent AI Architecture.

The platform helps recruiters streamline candidate screening, interviewing, evaluation, and hiring decisions while reducing manual effort and improving consistency.

### Problem Statement

Traditional recruitment processes involve:

Manual resume screening
Time-consuming candidate searches
Inconsistent interview evaluations
Human bias in decision-making
Lack of interview monitoring

RecruitAI addresses these challenges by automating the entire recruitment workflow using AI.


### Key Features
1. Resume Screening

   • Upload candidate resumes

   • Match resumes against job descriptions
  
   • Identify strengths and missing skills
  
   • Generate candidate score
  
   • AI-powered recommendation


2. Candidate Search
   
   • Semantic candidate search

   • Natural language queries
  
   • Vector similarity search using Qdrant

Example:
Machine Learning Engineer with NLP experience


3. AI Text Interview
   
   • Dynamic interview question generation

   • Role-based interview questions

   • Technical evaluation

   • Communication evaluation

   • Accuracy assessment

   
4. AI Voice Interview

   • AI asks questions verbally

   • Candidate responds using microphone
   
   • Whisper Speech-to-Text transcription

   • Automatic answer evaluation


   
5. AI Proctoring

Real-time candidate monitoring using:

   • OpenCV
   
   • YOLOv10

Current detections:

   • Multiple People
   
   • Mobile Phone Usage
   
   • Candidate Absence

Risk score generated automatically.



6. Interview Report

Generates:

   • Text Interview Score
   
   • Voice Interview Score
   
   • Risk Score
   
   • Final Score
   
   • Recommendation


   
7. HR Dashboard

Generates:

   • Hiring Recommendation

   • Salary Band
   
   • HR Summary
   
   • Joining Recommendation
   
   • Final Hiring Decision

   
 System Architecture

 
   Resume Upload
   
         │
         ▼
         
   Recruiter Agent
   
         │
         
         ▼
         
   Qdrant Vector Database
   
         │
         
         ▼
         
   Candidate Search
   
         │
         
         ▼
         
   Interview Agent
         │
         ├─────────────┐
         ▼             ▼
Text Round    Voice Round
                       │
                       ▼
                Whisper STT
                       │
                       ▼
                Evaluation
                       │
                       ▼
                Report Agent
                       ▲
                       │
               Proctoring Agent
                       │
               YOLOv10 + OpenCV
                       │
                       ▼
                  Risk Score
                       │
                       ▼
                   HR Agent
                       │
                       ▼
                Hiring Decision



                
📄 Application Pages
Page 1 – Resume Screening
What It Does
Upload Resume
Upload Job Description
Resume Evaluation
Skill Gap Analysis
Data Flow
Resume Upload
      ↓
AI Reads Resume
      ↓
Compare With Job Description
      ↓
Generate Score
      ↓
Store Candidate Profile
Output
Resume Score
Strengths
Missing Skills
Recommendation
Page 2 – Candidate Search
What It Does

Recruiters can search candidates using natural language.

Data Flow
Recruiter Search
      ↓
AI Understands Query
      ↓
Qdrant Search
      ↓
Matching Candidates
Output
Candidate Profiles
Candidate Scores
Similarity Ranking
Page 3 – Interview Center
Text Interview
Candidate Profile
      ↓
Question Generation
      ↓
Candidate Answers
      ↓
AI Evaluation
Voice Interview
AI Asks Question
      ↓
Candidate Speaks
      ↓
Whisper Converts Speech
      ↓
AI Evaluation
AI Proctoring
Webcam Feed
      ↓
YOLOv10 + OpenCV
      ↓
Suspicious Activity Detection
      ↓
Risk Score
Output
Text Interview Score
Voice Interview Score
Risk Score
Page 4 – Interview Report
Data Flow
Text Score
      ↓

Voice Score
      ↓

Risk Score
      ↓

Report Agent
      ↓

Final Interview Report
Output
Final Score
Technical Assessment
Communication Assessment
Risk Assessment
Recommendation
Page 5 – HR Dashboard
Data Flow
Interview Report
      ↓
HR Agent
      ↓
Hiring Analysis
      ↓
Final Decision
Output
Selected / Rejected
Salary Band
HR Summary
Joining Recommendation
🤖 Multi-Agent Architecture
RecruiterAgent

Responsible for:

Resume Evaluation
Skill Gap Analysis
Candidate Scoring
QdrantAgent

Responsible for:

Candidate Storage
Semantic Search
Candidate Retrieval
InterviewAgent

Responsible for:

Question Generation
Answer Evaluation
Interview Scoring
VoiceAgent

Responsible for:

Audio Recording
Speech Processing
Transcript Generation
TTSAgent

Responsible for:

Question Narration
Voice-Based Interview Experience
ProctoringAgent

Responsible for:

Candidate Monitoring
Risk Analysis
Suspicious Activity Detection
ReportAgent

Responsible for:

Score Aggregation
Final Interview Report Generation
HRAgent

Responsible for:

Hiring Recommendation
Salary Suggestion
HR Summary
📊 Data Structures
Resume Evaluation
{
  "resume_score": 85,
  "strengths": [
    "Machine Learning",
    "Deep Learning",
    "NLP"
  ],
  "missing_skills": [
    "FastAPI",
    "Vector Databases"
  ],
  "recommendation": "Proceed"
}
Interview Report
{
  "candidate_name": "PH ARVIND SHARMA",
  "text_score": 78,
  "voice_score": 82,
  "risk_score": 5,
  "final_score": 80,
  "recommendation": "Proceed"
}
HR Decision
{
  "candidate_name": "PH ARVIND SHARMA",
  "status": "Selected",
  "salary_band": "Mid-Senior Level",
  "joining_recommendation": "Recommended for Hiring"
}
🛠️ Tech Stack
Frontend
Streamlit
Backend
FastAPI
AI & LLM
Groq
Llama Models
Whisper
Computer Vision
OpenCV
YOLOv10
Vector Database
Qdrant
Language
Python
📂 Project Structure
AI-Recruitment-Agent/

├── app.py

├── pages/
│   ├── 1_Resume_Screening.py
│   ├── 2_Candidate_Search.py
│   ├── 3_Interview_Center.py
│   ├── 4_Interview_Report.py
│   └── 5_HR_Dashboard.py

├── agents/
│   ├── recruiter_agent.py
│   ├── qdrant_agent.py
│   ├── interview_agent.py
│   ├── voice_agent.py
│   ├── tts_agent.py
│   ├── proctoring_agent.py
│   ├── report_agent.py
│   └── hr_agent.py

├── data/
├── audio/
├── transcripts/
├── models/

└── .env
⚙️ Installation
Clone Repository
git clone <repository-url>

cd AI-Recruitment-Agent
Create Virtual Environment
Windows
python -m venv .venv

.venv\Scripts\activate
Linux / Mac
python3 -m venv .venv

source .venv/bin/activate
Install Dependencies
pip install -r requirements.txt

Generate requirements file:

pip freeze > requirements.txt
Create .env
GROQ_API_KEY=your_key

MODEL_NAME=llama-3.3-70b-versatile

QDRANT_URL=your_qdrant_url

QDRANT_API_KEY=your_qdrant_api_key
Run Streamlit
streamlit run app.py
Run FastAPI
uvicorn api.main:app --reload

Swagger Documentation:

http://127.0.0.1:8000/docs
🔒 Demo vs Production
Important Note

The current version exposes:

Interview Report Page
HR Dashboard

for demonstration purposes.

In a production environment:

Candidate Access
Resume Submission
      ↓
Interview
      ↓
Completion
Recruiter Access
Resume Screening
      ↓
Candidate Search
      ↓
Interview Report
HR Access
HR Dashboard
      ↓
Hiring Decision

Future versions will implement:

Authentication
Authorization
Role-Based Access Control (RBAC)
Candidate Portal
Recruiter Portal
HR Portal

to restrict access appropriately.

🚀 Future Scope
AI Interview Improvements
Dynamic Follow-Up Questions
Adaptive Interviews
Difficulty Levels (Easy, Medium, Hard, Expert)
Better LLM Support
GPT-4
Claude
Gemini
DeepSeek
Llama
Advanced AI Proctoring
Eye Tracking
Gaze Detection
Head Pose Estimation
Face Verification
Emotion Detection
Browser Tab Detection
Screen Monitoring
Communication Automation
Interview Invitations
Reminder Emails
Offer Letters
Rejection Emails
Onboarding Emails
Integrations
Zoom
Microsoft Teams
Google Meet
ATS Platforms (Workday, Greenhouse, Lever)
Analytics
Candidate Ranking
Hiring Trends
Skill Gap Analysis
Recruitment KPIs
👨‍💻 Author

PH ARVIND SHARMA

AI Engineer | Machine Learning Engineer | Data Scientist

Focused on:

Generative AI
Multi-Agent Systems
NLP
Computer Vision
Speech AI
MLOps
End-to-End AI Applications
