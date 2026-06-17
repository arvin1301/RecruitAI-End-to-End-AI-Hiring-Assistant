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
#### 1. Resume Screening

   • Upload candidate resumes

   • Match resumes against job descriptions
  
   • Identify strengths and missing skills
  
   • Generate candidate score
  
   • AI-powered recommendation




#### 2. Candidate Search
   
   • Semantic candidate search

   • Natural language queries
  
   • Vector similarity search using Qdrant

Example:
Machine Learning Engineer with NLP experience




#### 3. AI Text Interview
   
   • Dynamic interview question generation

   • Role-based interview questions

   • Technical evaluation

   • Communication evaluation

   • Accuracy assessment



   
#### 4. AI Voice Interview

   • AI asks questions verbally

   • Candidate responds using microphone
   
   • Whisper Speech-to-Text transcription

   • Automatic answer evaluation


   
#### 5. AI Proctoring

Real-time candidate monitoring using:

   • OpenCV
   
   • YOLOv10

Current detections:

   • Multiple People
   
   • Mobile Phone Usage
   
   • Candidate Absence

Risk score generated automatically.



#### 6. Interview Report

Generates:

   • Text Interview Score
   
   • Voice Interview Score
   
   • Risk Score
   
   • Final Score
   
   • Recommendation


   
#### 7. HR Dashboard

Generates:

   • Hiring Recommendation

   • Salary Band
   
   • HR Summary
   
   • Joining Recommendation
   
   • Final Hiring Decision

   
 
 ### System Architecture

<img width="1024" height="1536" alt="e5508de3-4630-4eb7-bd75-5671bfd2be4easas" src="https://github.com/user-attachments/assets/5d035303-5b52-43ca-8ab1-1d3eb8e82225" />


  



                
### Application Pages

Page 1 – Resume Screening

What It Does

   • Upload Resume
   
   • Upload Job Description
   
   • Resume Evaluation
   
   • Skill Gap Analysis



   
#### Data Flow

<img width="1024" height="1536" alt="e89235e6-8485-4058-8099-7b2471324b9b" src="https://github.com/user-attachments/assets/570b0061-8f3b-41af-8b54-7e44bf88e7a8" />




#### Output

   • Resume Score
   
   • Strengths
   
   • Missing Skills
   
   • Recommendation





Page 2 – Candidate Search
What It Does

Recruiters can search candidates using natural language.

#### Data Flow

<img width="1122" height="1402" alt="5aa9a586-19db-4a20-a059-83668d0a9818" src="https://github.com/user-attachments/assets/d96d8c5f-8ce6-4cd4-8387-8473068879b2" />



#### Output

   • Candidate Profiles
   
   • Candidate Scores
   
   • Similarity Ranking



   
Page 3 – Interview Center

#### Text Interview

<img width="1122" height="1402" alt="87188a0f-e607-46ac-9d75-60ac8cead408" src="https://github.com/user-attachments/assets/fc3d90ee-ab6e-4a64-a956-4c2901e11774" />



#### Voice Interview

<img width="1122" height="1402" alt="41462430-25c4-40d2-9c9c-db6a26e72ae9" src="https://github.com/user-attachments/assets/d04ccb01-423f-4628-a31f-59cdc409a578" />



#### AI Proctoring


<img width="1122" height="1402" alt="e6ce7b28-f1e6-4877-9580-ceb540331cc4" src="https://github.com/user-attachments/assets/b1b45f5a-9674-4265-8c18-63eb43cd33cf" />



#### Output

   • Text Interview Score
   
   • Voice Interview Score
   
   • Risk Score



Page 4 – Interview Report

<img width="1024" height="1536" alt="3157710e-ba7b-4602-b1a6-77629f21befe" src="https://github.com/user-attachments/assets/033a5064-fb5b-43e9-a887-dbb28b9a6735" />




#### Output

   • Final Score
   
   • Technical Assessment
   
   • Communication Assessment
   
   • Risk Assessment
   
   • Recommendation


Page 5 – HR Dashboard


<img width="1122" height="1402" alt="99d9c260-67fb-402c-afbb-7079175bd62f" src="https://github.com/user-attachments/assets/61072894-efa7-41f9-923c-c868450c143a" />



### Output

   • Selected / Rejected
   
   • Salary Band
   
   • HR Summary
   
   • Joining Recommendation

   
## Multi-Agent Architecture

### RecruiterAgent

Responsible for:

  • Resume Evaluation
  
  • Skill Gap Analysis
  
  • Candidate Scoring

  
### QdrantAgent

Responsible for:

   • Candidate Storage
   
   • Semantic Search
   
   • Candidate Retrieval

   
### InterviewAgent

Responsible for:

   • Question Generation
   
   • Answer Evaluation
   
   • Interview Scoring
   
### VoiceAgent

Responsible for:

   • Audio Recording

   • Speech Processing
   
   • Transcript Generation


### TTSAgent

Responsible for:

   • Question Narration
   
   • Voice-Based Interview Experience


### ProctoringAgent

Responsible for:

   • Candidate Monitoring
   
   • Risk Analysis
   
   • Suspicious Activity Detection


   
### ReportAgent

Responsible for:

   • Score Aggregation
   
   • Final Interview Report Generation



### HRAgent

Responsible for:

   • Hiring Recommendation
   
   • Salary Suggestion
   
   • HR Summary



## Data Structures

### Resume Evaluation

<img width="1536" height="1024" alt="448adb3b-f734-4f59-9c1f-2ad1ea6567f2" src="https://github.com/user-attachments/assets/a5ac8851-a5a5-4452-92e0-787c9d3de955" />




## Tech Stack

#### Frontend

  • Streamlit


  
#### Backend

  • FastAPI


  #### AI & LLM
  
   • Groq
   
   • Llama Models
   
   • Whisper

   
#### Computer Vision

   • OpenCV
   
   • YOLOv10

   
#### Vector Database

   • Qdrant

   
#### Language

    • Python


    
## Project Structure


<img width="1402" height="1122" alt="4ee89e78-ac2d-4ac5-9111-49c5610c5215" src="https://github.com/user-attachments/assets/87479e91-6186-4cfe-9f5e-4f76d90a74a1" />




## Installation

### Clone Repository

git clone <repository-url>

cd AI-Recruitment-Agent


### Create Virtual Environment
#### Windows

python -m venv .venv

.venv\Scripts\activate

#### Linux / Mac

python3 -m venv .venv

source .venv/bin/activate


#### Install Dependencies

pip install -r requirements.txt

Generate requirements file:

pip freeze > requirements.txt


#### Create .env

GROQ_API_KEY=your_key

MODEL_NAME=llama-3.3-70b-versatile

QDRANT_URL=your_qdrant_url

QDRANT_API_KEY=your_qdrant_api_key


#### Run Streamlit
streamlit run app.py


#### Run FastAPI
uvicorn api.main:app --reload

Swagger Documentation:

http://127.0.0.1:8000/docs


## Demo vs Production

Important Note

The current version exposes:

   • Interview Report Page
   
   • HR Dashboard

for demonstration purposes.


In a production environment:



<img width="1536" height="1024" alt="06465353-b548-434e-8fa0-ec5fc8719897" src="https://github.com/user-attachments/assets/81e8cfa5-7f8f-4f12-ba12-6e3e256f4eca" />

Future versions will implement:

   • Authentication
   
   • Authorization
   
   • Role-Based Access Control (RBAC)
   
   • Candidate Portal
   
   • Recruiter Portal
   
   • HR Portal

to restrict access appropriately.

##  Future Scope

#### AI Interview Improvements

   • Dynamic Follow-Up Questions
   
   • Adaptive Interviews
   
   • Difficulty Levels (Easy, Medium, Hard, Expert)

   
#### Better LLM Support

   • GPT-4
   
   • Claude
   
   • Gemini
   
   • DeepSeek
   
   • Llama


   
#### Advanced AI Proctoring

   • Eye Tracking
   
   • Gaze Detection
   
   • Head Pose Estimation
   
   • Face Verification
   
   • Emotion Detection
   
   • Browser Tab Detection
   
   • Screen Monitoring

   
#### Communication Automation

   • Interview Invitations
   
   • Reminder Emails
   
   • Offer Letters
   
   • Rejection Emails
   
   • Onboarding Emails

   
#### Integrations
   • Zoom
   
   • Microsoft Teams
   
   • Google Meet
   
   • ATS Platforms (Workday, Greenhouse, Lever)


#### Analytics
   • Candidate Ranking
   
   • Hiring Trends
   
   • Skill Gap Analysis
   
   • Recruitment KPIs



### Screen record



https://github.com/user-attachments/assets/dda5fbe1-5dcd-49ce-b76a-b16c4fedeed2

https://github.com/user-attachments/assets/e2875523-30a4-4ff3-8086-975f74684114



### Author

PH ARVIND SHARMA

AI Engineer | Machine Learning Engineer | Data Scientist

Focused on:

   • Generative AI
   
   • Multi-Agent Systems
   
   • NLP
   
   • Computer Vision
   
   • Speech AI
   
   • MLOps
   
   • End-to-End AI Applications
