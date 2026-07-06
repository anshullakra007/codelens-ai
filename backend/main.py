import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
# Make sure to run 'export GEMINI_API_KEY="your-key"' in your terminal
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI(title="CodeLens AI API")

# Enable CORS so our frontend can talk to the backend safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeReviewRequest(BaseModel):
    code: str
    language: str

SYSTEM_PROMPT = """
You are an expert elite systems architect and code auditor. Your job is to analyze the provided code snippet and return a strict JSON response evaluating it.
You must identify algorithmic bottlenecks, time/space complexities, edge cases, or potential memory/resource leaks.

Your response MUST follow this exact JSON schema structure, with absolutely no markdown formatting or wrapper text outside the JSON:
{
  "time_complexity": "e.g., O(N^2)",
  "space_complexity": "e.g., O(1)",
  "issues": [
    {
      "type": "Performance" or "Security" or "Style",
      "description": "Detailed explanation of the issue found.",
      "suggestion": "How to fix it."
    }
  ],
  "optimized_code": "The completely rewritten, fully optimized and clean version of the input code."
}
"""

@app.post("/api/review")
async def review_code(request: CodeReviewRequest):
    if not os.getenv("GEMINI_API_KEY"):
        raise HTTPException(status_code=500, detail="Gemini API Key not configured on server.")
        
    try:
        # Utilizing gemini-1.5-flash-latest for lightning fast turnarounds
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash-latest",
            generation_config={"response_mime_type": "application/json"}
        )
        
        user_content = f"Language: {request.language}\n\nCode Snippet:\n{request.code}"
        
        response = model.generate_content([SYSTEM_PROMPT, user_content])
        
        # Parse output string into valid JSON to ensure client gets pristine structure
        result_json = json.loads(response.text)
        return result_json

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Model failed to return valid JSON schema.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def serve_frontend():
    frontend_path = os.path.join(os.path.dirname(__file__), "../frontend/index.html")
    if not os.path.exists(frontend_path):
        return {"error": "File not found", "path": os.path.abspath(frontend_path), "cwd": os.getcwd(), "file": __file__}
    return FileResponse(frontend_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
