import os
import json
import io
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
import pdfplumber
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path

# Explicitly load .env from the same directory as this script
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

app = FastAPI(title="AI Resume Screener")

# Initialize Groq client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)
    print(f"✅ Groq API key loaded successfully.")
else:
    raise ValueError(
        "GROQ_API_KEY not found. Make sure your .env file exists in the project folder "
        "and contains: GROQ_API_KEY=your_actual_key"
    )

# Serve index.html directly from root to avoid static directory setup
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/health")
async def health_check():
    return {"status": "ok", "model": "llama-3.3-70b-versatile"}

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        print(f"Error extracting text: {e}")
    return text

def build_prompt(jd: str, resume_text: str) -> str:
    prompt = f"""You are an expert technical recruiter analyzing a resume against a job description.
Your goal is to score the candidate's fit on a scale of 0 to 100 and identify key strengths and gaps.

Job Description:
{jd}

Resume:
{resume_text}

Analyze the resume against the job description. Respond ONLY with a valid JSON object matching this exact structure, with no extra formatting, markdown fences, or text outside the JSON:
{{
  "score": <integer between 0 and 100>,
  "strengths": "<short string summarizing 2-3 key matching skills/experiences>",
  "gaps": "<short string summarizing 1-2 missing skills or mismatches>",
  "recommendation": "<short string: 'Strong Fit', 'Moderate Fit', or 'Not Fit'>"
}}
"""
    return prompt

@app.post("/screen-resume")
async def screen_resume(jd: str = Form(...), file: UploadFile = File(...)):
    try:
        pdf_bytes = await file.read()
        resume_text = extract_text_from_pdf(pdf_bytes)
        
        if not resume_text.strip():
            return {
                "candidate_name": file.filename,
                "score": 0,
                "strengths": "None",
                "gaps": "Could not extract text from PDF",
                "recommendation": "Not Fit"
            }
            
        prompt = build_prompt(jd, resume_text)
        
        # Call Groq
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
        )
        
        output_text = response.choices[0].message.content.strip()

        # Strip potential markdown fences
        if output_text.startswith("```json"):
            output_text = output_text[7:]
        if output_text.startswith("```"):
            output_text = output_text[3:]
        if output_text.endswith("```"):
            output_text = output_text[:-3]
            
        output_text = output_text.strip()
        
        try:
            result = json.loads(output_text)
        except json.JSONDecodeError:
            print(f"Failed to parse JSON. Raw output: {output_text}")
            return {
                "candidate_name": file.filename,
                "score": 0,
                "strengths": "Error parsing output",
                "gaps": "API did not return valid JSON",
                "recommendation": "Error"
            }
            
        # Add candidate name (using filename, minus extension if easy)
        candidate_name = file.filename
        if candidate_name.lower().endswith('.pdf'):
            candidate_name = candidate_name[:-4]
            
        result["candidate_name"] = candidate_name
        return result
        
    except Exception as e:
        print(f"Error processing {file.filename}: {e}")
        return {
            "candidate_name": getattr(file, "filename", "Unknown"),
            "score": 0,
            "strengths": "Error",
            "gaps": str(e),
            "recommendation": "Error"
        }
