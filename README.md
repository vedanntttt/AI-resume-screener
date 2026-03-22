# AI Resume Screener

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen)]([https://ai-resume-screener-wb84.onrender.com])

AI Resume Screener is a FastAPI-based web application that automatically screens resumes against a job description using Groq's Llama 3 model. It extracts text from PDF resumes and provides a match score, strengths, gaps, and a recommendation.

## Features

- **PDF Text Extraction**: Uses `pdfplumber` to accurately extract text from resume PDFs.
- **LLM-Powered Analysis**: Leverages Groq's `llama-3.3-70b-versatile` model for intelligent resume screening.
- **Automated Scoring**: Generates a fit score (0-100) based on the job description.
- **Key Insights**: Identifies candidate strengths and potential gaps.
- **Recommendations**: Categorizes candidates into "Strong Fit", "Moderate Fit", or "Not Fit".

## Tech Stack

- **Backend**: FastAPI (Python)
- **AI Model**: Groq (Llama 3.3 70B)
- **Extraction**: `pdfplumber`
- **Frontend**: HTML/Vanilla CSS (served directly from `index.html`)

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- A Groq API Key (Get it from [console.groq.com](https://console.groq.com/))

### 2. Installation
Clone the repository and install the dependencies:
```bash
git clone https://github.com/vedanntttt/AI-resume-screener.git
cd AI-resume-screener
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory and add your Groq API key:
```env
GROQ_API_KEY=your_actual_groq_api_key_here
```

## Running the Application

To start the server, run:
```bash
uvicorn main:app --reload
```
The application will be available at `http://127.0.0.1:8000`.

## File Structure

- `main.py`: Core FastAPI application and logic.
- `index.html`: Interactive web interface for uploading resumes and job descriptions.
- `extract.py`: Utility script for text extraction from various document formats.
- `requirements.txt`: List of Python dependencies.
- `.env`: (Ignored) Contains sensitive environment variables like API keys.
- `.gitignore`: Specifies files and folders to be ignored by Git.

## License

This project is licensed under the MIT License.
