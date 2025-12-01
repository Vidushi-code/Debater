from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.orchestrator import MultiAgentSystem
import uvicorn

app = FastAPI(title="Debater AI API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize system
system = MultiAgentSystem()

class IdeaRequest(BaseModel):
    idea: str

@app.post("/classify")
async def classify_intent(request: IdeaRequest):
    try:
        intent = system.check_intent(request.idea)
        return {"type": intent}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat_mode(request: IdeaRequest):
    try:
        response = system.run_chat(request.idea)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze")
async def analyze_idea(request: IdeaRequest):
    try:
        # Force analysis path (orchestrator will still run check_intent internally if we call process_user_input,
        # but we can assume the frontend only calls this if intent is 'analysis' or user forced it).
        # However, process_user_input handles both. Let's keep using it but expect a dict.
        
        result = system.process_user_input(request.idea)
        
        if isinstance(result, str):
            # Fallback if it decided to chat anyway (shouldn't happen if frontend logic is correct, but good for safety)
            return {
                "type": "chat",
                "conversationalAgent": result
            }
        else:
            # Full analysis
            return {
                "type": "analysis",
                "researchAgent": result.get("research"),
                "goodAgent": result.get("positives"),
                "devilAgent": result.get("flaws"),
                "finalConclusion": result.get("final_response"),
                "conversationalAgent": result.get("conversational_response")
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("src.api:app", host="0.0.0.0", port=8001, reload=True)
