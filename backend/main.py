from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import httpx
import random
import json
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Prompt Optimization Engine API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class OptimizationRequest(BaseModel):
    prompt: str
    strategy: str
    use_case: str
    num_variations: int
    num_rounds: int
    creativity: float

class Variation(BaseModel):
    text: str
    clarity: int
    specificity: int
    overall: int
    techniques: List[str]
    generation: int

class OptimizationResponse(BaseModel):
    variations: List[Variation]
    original_scores: Dict[str, int]
    best_prompt: str
    improvements: Dict[str, int]

# GROQ API Config
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Optimization techniques
TECHNIQUES = {
    "evolutionary": {
        "mutations": [
            {"name": "Add context", "template": "Given that the audience is technical professionals, {prompt}"},
            {"name": "Add specificity", "template": "{prompt} Be specific and include concrete examples."},
            {"name": "Add structure", "template": "{prompt} Structure your response with clear sections: overview, details, and conclusion."},
            {"name": "Add constraints", "template": "{prompt} Keep the response under 500 words and use bullet points for key items."},
            {"name": "Role framing", "template": "You are an expert technical writer. {prompt}"},
            {"name": "Step-by-step", "template": "{prompt} Think step by step and explain your reasoning."},
            {"name": "Output format", "template": "{prompt} Format your response as a structured document with headers."},
            {"name": "Audience targeting", "template": "{prompt} Tailor the explanation for someone with intermediate knowledge."}
        ]
    },
    "reinforcement": {
        "rewrites": [
            {"name": "Clarity boost", "template": "{prompt} Use clear, unambiguous language and define any technical terms."},
            {"name": "Task decomposition", "template": "Break this task into sub-tasks: {prompt}"},
            {"name": "Few-shot framing", "template": "{prompt}\n\nHere is an example of the expected output format:\n[Example: A well-structured, detailed response that addresses all aspects of the query.]"},
            {"name": "Negative constraint", "template": "{prompt} Do NOT include filler words, vague statements, or unnecessary caveats."},
            {"name": "Quality criteria", "template": "{prompt} Your response will be evaluated on: accuracy, completeness, clarity, and actionability."}
        ]
    }
}

async def call_groq(prompt: str) -> str:
    """Call GROQ API to generate improved prompt variations"""
    if not GROQ_API_KEY:
        return None
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                GROQ_API_URL,
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "mixtral-8x7b-32768",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a prompt optimization expert. Improve the given prompt to be more clear, specific, and effective. Return ONLY the improved prompt, no explanation."
                        },
                        {
                            "role": "user",
                            "content": f"Improve this prompt: {prompt}"
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 500
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            return None
    except Exception as e:
        print(f"GROQ API error: {e}")
        return None

def score_clarity(text: str) -> int:
    """Score prompt clarity"""
    score = 50
    if len(text) > 50:
        score += 10
    if len(text) > 100:
        score += 5
    if any(word in text.lower() for word in ["specific", "clear", "concrete", "example"]):
        score += 10
    if any(word in text.lower() for word in ["step by step", "structure"]):
        score += 8
    if any(word in text.lower() for word in ["do not", "avoid"]):
        score += 5
    if any(word in text.lower() for word in ["expert", "role", "you are"]):
        score += 7
    if len(text.split('. ')) > 2:
        score += 5
    score += random.randint(0, 8)
    return min(98, max(30, score))

def score_specificity(text: str) -> int:
    """Score prompt specificity"""
    score = 45
    if any(c.isdigit() for c in text):
        score += 8
    if any(word in text.lower() for word in ["example", "format", "structure"]):
        score += 10
    if any(word in text.lower() for word in ["bullet", "section", "header"]):
        score += 7
    if any(word in text.lower() for word in ["under", "maximum", "minimum"]):
        score += 9
    if any(word in text.lower() for word in ["accuracy", "completeness", "actionable"]):
        score += 6
    if len(text) > 150:
        score += 8
    score += random.randint(0, 10)
    return min(97, max(25, score))

def score_overall(clarity: int, specificity: int) -> int:
    """Calculate overall score"""
    base = (clarity * 0.45 + specificity * 0.45)
    bonus = random.randint(0, 8)
    return min(99, max(30, int(base + bonus)))

async def generate_variation(base_prompt: str, strategy: str, creativity: float, round_num: int) -> Variation:
    """Generate a single prompt variation"""
    var_text = base_prompt
    applied_techniques = []
    
    # Try AI generation first
    if GROQ_API_KEY:
        ai_variation = await call_groq(base_prompt)
        if ai_variation:
            var_text = ai_variation
            applied_techniques.append("AI Optimized")
    
    # Apply techniques based on strategy
    if strategy in ["evolutionary", "hybrid"]:
        mutations = TECHNIQUES["evolutionary"]["mutations"]
        mutation = random.choice(mutations)
        var_text = mutation["template"].format(prompt=var_text)
        applied_techniques.append(mutation["name"])
        
        # Crossover for hybrid
        if strategy == "hybrid" and random.random() < creativity:
            var_text = crossover(var_text, base_prompt)
            applied_techniques.append("crossover")
    
    if strategy in ["reinforcement", "hybrid"]:
        rewrites = TECHNIQUES["reinforcement"]["rewrites"]
        rewrite = random.choice(rewrites)
        var_text = rewrite["template"].format(prompt=var_text)
        applied_techniques.append(rewrite["name"])
    
    # Remove duplicates and limit
    applied_techniques = list(dict.fromkeys(applied_techniques))[:3]
    
    # Score the variation
    clarity = score_clarity(var_text)
    specificity = score_specificity(var_text)
    overall = score_overall(clarity, specificity)
    
    return Variation(
        text=var_text,
        clarity=clarity,
        specificity=specificity,
        overall=overall,
        techniques=applied_techniques,
        generation=round_num
    )

def crossover(p1: str, p2: str) -> str:
    """Simple crossover between two prompts"""
    s1 = p1.split('. ')
    s2 = p2.split('. ')
    mixed = []
    max_len = max(len(s1), len(s2))
    for i in range(max_len):
        mixed.append(random.choice([s1[i] if i < len(s1) else "", s2[i] if i < len(s2) else ""]))
    return '. '.join([m for m in mixed if m])

@app.post("/api/optimize", response_model=OptimizationResponse)
async def optimize(request: OptimizationRequest):
    """Main optimization endpoint"""
    try:
        all_variations = []
        
        for round_num in range(1, request.num_rounds + 1):
            round_variations = []
            base = request.prompt if round_num == 1 else (all_variations[-1].text if all_variations else request.prompt)
            
            for _ in range(request.num_variations):
                var = await generate_variation(base, request.strategy, request.creativity, round_num)
                round_variations.append(var)
            
            round_variations.sort(key=lambda x: x.overall, reverse=True)
            all_variations = round_variations
        
        # Get original scores
        orig_clarity = score_clarity(request.prompt)
        orig_specificity = score_specificity(request.prompt)
        orig_overall = score_overall(orig_clarity, orig_specificity)
        
        # Mark best variation
        if all_variations:
            all_variations[0].techniques.append("★ BEST")
        
        best_prompt = all_variations[0].text if all_variations else request.prompt
        
        return OptimizationResponse(
            variations=all_variations,
            original_scores={
                "clarity": orig_clarity,
                "specificity": orig_specificity,
                "overall": orig_overall
            },
            best_prompt=best_prompt,
            improvements={
                "clarity": all_variations[0].clarity - orig_clarity if all_variations else 0,
                "specificity": all_variations[0].specificity - orig_specificity if all_variations else 0,
                "overall": all_variations[0].overall - orig_overall if all_variations else 0
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health():
    return {"status": "healthy", "groq_available": bool(GROQ_API_KEY)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)