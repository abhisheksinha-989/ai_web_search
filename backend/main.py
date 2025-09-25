from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import sys

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.research import get_research_answer

app = FastAPI(title="Research Assistant API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class ResearchRequest(BaseModel):
    query: str

# Response model
class ResearchResponse(BaseModel):
    summary: str
    sources: list
    word_count: int
    processing_time: float

@app.post("/api/research", response_model=ResearchResponse)
async def research_endpoint(request: ResearchRequest):
    """Endpoint for research queries"""
    try:
        summary, sources = get_research_answer(request.query)
        
        if not summary:
            raise HTTPException(status_code=500, detail="Failed to generate research report")
        
        word_count = len(summary.split())
        
        return ResearchResponse(
            summary=summary,
            sources=sources[:15],  # Return up to 15 sources
            word_count=word_count,
            processing_time=0  # Will be calculated in the research function
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Research failed: {str(e)}")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "Research Assistant API"}

# Serve frontend files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('frontend/index.html')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)