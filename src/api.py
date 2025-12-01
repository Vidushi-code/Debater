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

@app.post("/analyze")
async def analyze_idea(request: IdeaRequest):
    try:
        # Check intent first (using the orchestrator's logic indirectly via process_user_input)
        # Note: process_user_input now returns a dict (full context) OR a string (chat response)
        # We need to handle both cases.
        
        result = system.process_user_input(request.idea)
        
        if isinstance(result, str):
            # It was just a chat response (Router said NOT_READY)
            return {
                "type": "chat",
                "conversationalAgent": result
            }
        else:
            # It was a full analysis
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
