<div align="center">
  <h1>👁️ CodeLens AI</h1>
  <p><strong>Your automated, hyper-optimized code review agent.</strong></p>
  
  <a href="https://codelens-ai-ixqc.onrender.com">View Live Demo</a>
</div>

## Overview
CodeLens AI is a modern, AI-powered developer tool that audits your code snippets for time and space complexity bottlenecks, catches bugs, and generates fully optimized solutions.

## Architecture
- **Backend:** FastAPI (Python 3) serving an integrated REST API.
- **AI Engine:** Google Gemini 3.5 Flash (via `google-genai` SDK) for lightning-fast analysis.
- **Frontend:** Responsive, dark-mode UI built with Tailwind CSS.
- **Deployment:** Containerized via Docker and deployed on Render.

## Features
- **Instant Complexity Analysis:** Identifies algorithmic bottlenecks with Big-O notation.
- **Categorized Issue Tracking:** Highlights Security, Performance, and Stylistic issues.
- **Code Optimization:** Returns a completely rewritten and clean version of your code.
- **Unified Deployment:** Frontend served directly from the FastAPI backend.

## Local Setup
```bash
# 1. Clone the repository
git clone https://github.com/anshullakra007/codelens-ai.git
cd codelens-ai/backend

# 2. Setup Virtual Environment
python3 -m venv venv
source venv/bin/activate

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Set Gemini API Key
export GEMINI_API_KEY="your_api_key_here"

# 5. Run Server
python main.py
```
*Visit `http://127.0.0.1:8000` to interact with the UI.*

## Benchmarking Suite
This repository includes an automated testing suite designed to validate the CodeLens AI engine against common imperfect coding patterns across various languages (Python, Java, C++). 

### Included Test Cases:
- **Time Complexity:** Identifies $O(N^2)$ bottlenecks (e.g. nested loops) and optimizes to $O(N \log N)$ or better.
- **Space Complexity:** Identifies unnecessary memory allocations (e.g. inefficient string concatenations).
- **Security:** Detects SQL Injections, buffer overflows, and unsafe variables.
- **Logic Bugs:** Catches edge cases like Out-Of-Bounds array access and Undefined Behavior (UB).
- **Stylistic Flaws:** Identifies un-pythonic approaches or unreadable abstractions.

### Running Benchmarks
To run the automated suite against the live production API:
```bash
cd backend
python3 benchmark_runner.py --target prod
```
