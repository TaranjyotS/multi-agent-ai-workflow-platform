from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_api_key
from app.db.session import get_db
from app.schemas.knowledge import DocumentCreate, DocumentRead, SearchResponse
from app.services.knowledge_service import KnowledgeService

router = APIRouter(prefix="/knowledge", tags=["Knowledge"], dependencies=[Depends(verify_api_key)])

@router.post("/documents", response_model=DocumentRead)
async def ingest_document(payload: DocumentCreate, db: AsyncSession = Depends(get_db)) -> DocumentRead:
    doc = await KnowledgeService(db).ingest(payload.title, payload.source, payload.content)
    return DocumentRead(id=doc.id, title=doc.title, source=doc.source, chunk_count=len(doc.chunks))

@router.get("/search", response_model=SearchResponse)
async def search_knowledge(q: str = Query(min_length=2), limit: int = Query(default=5, ge=1, le=10), db: AsyncSession = Depends(get_db)) -> SearchResponse:
    results = await KnowledgeService(db).search(q, limit)
    return SearchResponse(query=q, results=results)
