from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=50)


class SearchResponse(BaseModel):
    query: str
    results: list[str]
    
    """
    
    we expect from client is
    {
  "query": "What is attention?",
  "top_k": 5
}
    
    """