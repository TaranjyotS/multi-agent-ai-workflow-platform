from pydantic import BaseModel, Field


class DocumentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    source: str = "manual"
    content: str = Field(min_length=20)

class DocumentRead(BaseModel):
    id: str
    title: str
    source: str
    chunk_count: int

class SearchResult(BaseModel):
    document_id: str
    title: str
    content: str
    score: float

class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]
