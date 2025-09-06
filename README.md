# 📄 Resume Buddy
Resume Buddy is a full-stack application that helps users upload, analyze, and optimize resumes.  
It consists of a **Frontend** (React + Vite) and a **Backend** (FastAPI with Python).

---

## 🚀 Features
- Upload a resume, job description and extract content.
- Send extracted data to an AI model for analysis.
- Clean separation of frontend and backend for easy development.
- Configurable via environment variables.

---

## 📂 Project Structure
```
ResumeBuddy/
|-- Frontend/ #React + Vite
|-- Backend/ #FastAPI 
|-- README.md #Docs
```

---

## ⚙️ Requirements

### Global
- pip (for Python packages)
- npm (for frontend)

### Frontend
Inside the `Frontend/` folder:
```bash
cd Frontend
npm install
```

### Backend
Inside the `Backend/` folder:
```bash
cd Backend
pip install -r requirements.txt
```

### Environment Variable 
You need .env files in both Frontend and Backend folders.

### Frontend (`Frontend/.env`)
```env
VITE_BASE_URL=
```

### Backend (`Backend/.env`)
```env
OPENAI_API_KEY=your_openai_api_key_here
MAX_OPENAI_TOKENS= Set max tokens here defaults to 800
ALLOWED_ORIGINS= For cors
OPENAI_MODEL=
PROMPT_SYSTEM= This is a system prompt (More info below)
PROMPT_ATS_USER_TEMPLATE= This is a user prompt (More info below)
```
## 📝 Prompt System

Resume Buddy uses a **two-part prompt system** to analyze résumés against job descriptions:

1. **System Prompt**  
   Defines strict rules for the AI:  
   - Use only the provided résumé text and job description.  
   - Never invent or infer facts.  
   - Quote evidence directly from the résumé.  
   - Output clean Markdown in a consistent structure.  
   - Keep the response concise.  

2. **User Prompt Template**  
   Instructs the AI on what inputs to process and what steps to follow.  
   - Provide the candidate’s résumé text.  
   - Provide the job description text.  
   - AI will validate inputs and generate a Requirements Map, Missing/Weak Keywords, Recommended Edits, Match Score, and ATS Score.

3. **Using Variables in Prompts**
    - When calling the Resume Buddy prompt, you must replace the placeholders with your **actual input text**:
    - `{resume_text}` → the full plain-text résumé of the candidate.  
    - `{job_description}` → the full plain-text job description.

---

### Running the APP

**Start Backend**
```Bash
  cd Backend
  uvicorn app.main:app --reload

```

**Start Frontend**
```Bash
  cd Frontend
  npm run dev
```

