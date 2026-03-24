https://assets/banner.png

⚡ Prompt Optimization Engine
AI-powered prompt engineering — automatically improve your prompts using evolutionary algorithms, reinforcement learning, and multi-dimensional response scoring. The engine generates, evaluates, and selects the best prompt variations in real-time.

Built by Abdullah Shafique
AI Engineer · FastAPI · Groq · Evolutionary Algorithms

https://img.shields.io/badge/Live%2520Demo-Visit%2520App-4f6ef7?style=for-the-badge&logo=vercel
 
https://img.shields.io/badge/GitHub-aadi--abdullah-181717?logo=github
 
https://img.shields.io/badge/LinkedIn-aadi--abdullah-0A66C2?logo=linkedin

Overview
Most prompt engineering is manual, subjective, and time-consuming. This one isn't.

The Prompt Optimization Engine automates the entire prompt improvement workflow using genetic algorithms and reinforcement learning. You provide a base prompt — it generates dozens of variations, scores each on clarity and specificity, selects the best performers, and iteratively refines them. The result is a provably better prompt, backed by measurable scores.

No guesswork. No endless tweaking. Just better prompts, automatically.

Live Demo: aadi-abdullah.github.io/prompt-optimization-engine

Demo
https://assets/demo.png

Try it live → aadi-abdullah.github.io/prompt-optimization-engine

How It Works
text
User inputs base prompt
      │
      ▼
[Prompt Analyzer]   ──  Word count, sentence structure, weak points identified
      │
      ▼
[Variation Engine]  ──  Multiple strategies applied:
                        • Evolutionary: mutation + crossover
                        • Reinforcement: guided rewrites
                        • Hybrid: combination of both
      │
      ▼
[Multi-Metric Scorer] ──  Each variation scored on:
                          • Clarity (readability, structure, role framing)
                          • Specificity (examples, constraints, format)
                          • Overall composite score
      │
      ▼
[Fitness Selection]  ──  Best variations selected for next generation
      │
      ▼
[Groq LLM]          ──  Optional AI-powered prompt improvement
      │
      ▼
[Final Result]      ──  Optimized prompt + improvement metrics
Features
Evolutionary Optimization — mutation and crossover operators generate diverse prompt variations

Reinforcement Learning — guided rewrites based on quality criteria and constraints

Multi-Dimensional Scoring — prompts evaluated on clarity, specificity, and overall effectiveness

Iterative Refinement — multiple optimization rounds for progressive improvement

AI-Powered Generation — optional Groq LLM integration for intelligent prompt rewriting

Real-Time Feedback — step-by-step progress visualization with status logs

Dark UI with Animations — professional, responsive design with smooth transitions

Copy to Clipboard — one-click copy of optimized prompts

Improvement Metrics — see exactly how much clarity and specificity improved

Tech Stack
Layer	Technology
Frontend	HTML5, CSS3, Vanilla JavaScript
Backend	FastAPI, Python 3.11
LLM	Groq — mixtral-8x7b-32768
Optimization	Custom evolutionary algorithms + RL
Scoring	Heuristic-based multi-metric evaluation
Backend Deploy	Railway
Frontend Deploy	GitHub Pages
Project Structure
text
prompt-optimization-engine/
│
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions workflow
│
├── backend/
│   ├── main.py                 # FastAPI app + endpoints
│   ├── requirements.txt        # Python dependencies
│   └── runtime.txt             # Python version (3.11)
│
├── assets/
│   ├── banner.png
│   ├── demo.png
│   └── architecture.png
│
├── index.html                  # Main application
├── styles.css                  # All styling + animations
├── app.js                      # Frontend logic + API integration
├── .gitignore
└── README.md
Live Deployment
The project is fully deployed and accessible:

Service	URL
Frontend	aadi-abdullah.github.io/prompt-optimization-engine
Backend API	prompt-optimization-engine.up.railway.app
API Documentation	prompt-optimization-engine.up.railway.app/docs
Health Check	prompt-optimization-engine.up.railway.app/api/health
Local Setup
Prerequisites
Python 3.11+

Free API key from Groq (optional, works without)

Installation
bash
# 1. Clone the repo
git clone https://github.com/aadi-abdullah/prompt-optimization-engine.git
cd prompt-optimization-engine

# 2. Backend setup
cd backend
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Create .env file
echo "GROQ_API_KEY=your_key_here" > .env

# 4. Run backend
python main.py

# 5. In a new terminal, serve frontend from root
cd ..
python -m http.server 3000
Open http://localhost:3000

API Reference
Method	Endpoint	Description
GET	/	Root endpoint with API status
GET	/api/health	Health check + Groq availability
POST	/api/optimize	Optimize a prompt with chosen strategy
GET	/docs	Interactive API documentation
Request Body (POST /api/optimize)
json
{
  "prompt": "Explain machine learning to beginners",
  "strategy": "hybrid",
  "use_case": "general",
  "num_variations": 4,
  "num_rounds": 2,
  "creativity": 0.7
}
Response
json
{
  "variations": [
    {
      "text": "You are an expert educator. Explain machine learning to beginners using simple analogies...",
      "clarity": 92,
      "specificity": 88,
      "overall": 90,
      "techniques": ["Role framing", "AI Optimized", "Clarity boost"],
      "generation": 1
    }
  ],
  "original_scores": {
    "clarity": 65,
    "specificity": 58,
    "overall": 62
  },
  "best_prompt": "You are an expert educator...",
  "improvements": {
    "clarity": 27,
    "specificity": 30,
    "overall": 28
  }
}
Interactive docs available at /docs when running locally.

Optimization Strategies
Strategy	Description	Best For
Evolutionary	Uses mutation and crossover operators to generate variations	Structured prompts, technical content
Reinforcement	Applies guided rewrites based on quality criteria	Creative writing, open-ended tasks
Hybrid	Combines both approaches for maximum diversity	General purpose, balanced improvement
Scoring Metrics
Clarity Score (0-100)
Length & Structure — longer prompts with clear sections score higher

Clarity Keywords — presence of "specific", "clear", "concrete", "example"

Step-by-Step — explicit reasoning or structured approach

Role Framing — expert role assignment or persona definition

Specificity Score (0-100)
Constraints — word limits, format requirements, length restrictions

Examples — explicit examples or output format specifications

Numbers — presence of specific quantities or thresholds

Quality Criteria — defined evaluation metrics (accuracy, completeness)

Overall Score
Weighted combination: 45% Clarity + 45% Specificity + 10% randomness

Higher scores indicate more effective, usable prompts

Configuration
Variable	Description	Default
GROQ_API_KEY	Groq API key (optional)	—
GROQ_MODEL	LLM model name	mixtral-8x7b-32768
num_variations	Variations per round	2-8 (slider)
num_rounds	Optimization iterations	1-5 (slider)
creativity	Mutation rate	0.1-1.0 (slider)
Get Free API Keys
Service	Free Tier	Link
Groq	Generous daily limits (30 req/min)	console.groq.com
Note: The engine works without an API key using local techniques. Adding Groq enables AI-powered prompt generation.

Roadmap
Multi-model support (OpenAI, Anthropic, Gemini)

Custom scoring functions (user-defined criteria)

Prompt templates library

Export optimized prompts to JSON/CSV

Real-time streaming during optimization

A/B testing mode for prompt comparison

Fine-tuning based on user feedback

Optimization Techniques Library
The engine includes a rich set of prompt improvement techniques:

Evolutionary Mutations
Add context (audience specification)

Add specificity (concrete examples)

Add structure (sections, headers)

Add constraints (word limits, format)

Role framing (expert persona)

Step-by-step reasoning

Output format specification

Audience targeting

Reinforcement Rewrites
Clarity boost (unambiguous language)

Task decomposition (sub-task breakdown)

Few-shot framing (examples provided)

Negative constraints (what to avoid)

Quality criteria definition

About the Author
I'm an AI Engineer with a background in design — I spent 6 years as a professional graphic designer before transitioning into software engineering. That background shapes how I build: I optimise for systems that are both technically sound and genuinely usable.

🎓 Software Engineering — Riphah International University (GPA 3.99 / 4.0, 2024–2028)

🏅 AI Agent Developer Specialization — Vanderbilt University

🏅 Microsoft Python Development Specialization

🏅 Adobe Graphic Designer Specialization

Currently open to AI engineering internships and junior roles.

→ LinkedIn · GitHub · abdullahshafique2019@gmail.com

License
MIT — free to use, modify, and distribute.