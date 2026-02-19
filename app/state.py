from typing import List
from pydantic import BaseModel, Field

class AgentState(BaseModel):
    question: str
    
    documents: List[str] = []
    answer: str = ""
    
    failed_attempts: int = 0
    past_queries: List[str] = Field(default_factory=list)
    
    relevance_score: float = 0.0
    grounding_score: float = 0.0
    completeness_score: float = 0.0
    
    confidence: float = 0.0
