import os
import random
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional

app = FastAPI(title="Prompt Optimization Engine API")

# CORS - Allow all origins for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
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

# Scoring Functions
def score_clarity(text: str) -> int:
    score = 50
    if len(text) > 50:
        score += 10
    if len(text) > 100:
        score += 5
    if any(word in text.lower() for word in ["specific", "clear", "concrete", "example"]):
        score += 10
    if any(word in text.lower() for word in ["step by step", "structure"]):
        score += 8
    if any(word in text.lower() for word in ["expert", "role", "you are"]):
        score += 7
    score += random.randint(0, 8)
    return min(98, max(30, score))

def score_specificity(text: str) -> int:
    score = 45
    if any(c.isdigit() for c in text):
        score += 8
    if any(word in text.lower() for word in ["example", "format", "structure"]):
        score += 10
    if any(word in text.lower() for word in ["bullet", "section", "header"]):
        score += 7
    if len(text) > 150:
        score += 8
    score += random.randint(0, 10)
    return min(97, max(25, score))

def score_overall(clarity: int, specificity: int) -> int:
    base = (clarity * 0.45 + specificity * 0.45)
    bonus = random.randint(0, 8)
    return min(99, max(30, int(base + bonus)))

def generate_variation(base: str, strategy: str, creativity: float, round_num: int) -> Variation:
    techniques = []
    text = base
    
    # Evolutionary mutations
    mutations = [
        "Be specific and include concrete examples.",
        "Structure your response with clear sections.",
        "You are an expert in this field.",
        "Think step by step and explain your reasoning.",
        "Keep the response under 500 words."
    ]
    
    # Reinforcement rewrites
    rewrites = [
        "Use clear, unambiguous language.",
        "Break this task into sub-tasks.",
        "Do NOT include filler words or vague statements."
    ]
    
    if strategy in ["evolutionary", "hybrid"] and random.random() < creativity:
        mutation = random.choice(mutations)
        text = f"{base} {mutation}"
        techniques.append(mutation[:20] + "...")
    
    if strategy in ["reinforcement", "hybrid"] and random.random() < creativity:
        rewrite = random.choice(rewrites)
        text = f"{base} {rewrite}"
        techniques.append(rewrite[:20] + "...")
    
    if not techniques:
        techniques = ["Basic optimization"]
    
    clarity = score_clarity(text)
    specificity = score_specificity(text)
    overall = score_overall(clarity, specificity)
    
    return Variation(
        text=text,
        clarity=clarity,
        specificity=specificity,
        overall=overall,
        techniques=techniques[:2],
        generation=round_num
    )

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Prompt Optimization Engine API is running!",
        "status": "online",
        "endpoints": ["/", "/api/health", "/api/optimize", "/docs"]
    }

# Health check
@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "groq_available": bool(os.getenv("GROQ_API_KEY", ""))
    }

# Optimize endpoint
@app.post("/api/optimize", response_model=OptimizationResponse)
async def optimize(request: OptimizationRequest):
    try:
        all_variations = []
        
        for round_num in range(1, request.num_rounds + 1):
            round_variations = []
            base = request.prompt if round_num == 1 else (all_variations[-1].text if all_variations else request.prompt)
            
            for _ in range(request.num_variations):
                var = generate_variation(base, request.strategy, request.creativity, round_num)
                round_variations.append(var)
            
            round_variations.sort(key=lambda x: x.overall, reverse=True)
            all_variations = round_variations
        
        # Original scores
        orig_clarity = score_clarity(request.prompt)
        orig_specificity = score_specificity(request.prompt)
        orig_overall = score_overall(orig_clarity, orig_specificity)
        
        # Mark best variation
        if all_variations:
            all_variations[0].techniques.append("★ BEST")
            best_prompt = all_variations[0].text
            improvements = {
                "clarity": all_variations[0].clarity - orig_clarity,
                "specificity": all_variations[0].specificity - orig_specificity,
                "overall": all_variations[0].overall - orig_overall
            }
        else:
            best_prompt = request.prompt
            improvements = {"clarity": 0, "specificity": 0, "overall": 0}
        
        return OptimizationResponse(
            variations=all_variations,
            original_scores={
                "clarity": orig_clarity,
                "specificity": orig_specificity,
                "overall": orig_overall
            },
            best_prompt=best_prompt,
            improvements=improvements
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# For local development
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)