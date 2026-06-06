from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import KnowledgeChunk, KnowledgeDocument
from app.rag.chunking import chunk_text
from app.rag.embeddings import LocalEmbeddingModel, cosine


class KnowledgeService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.embeddings = LocalEmbeddingModel()

    async def ingest(self, title: str, source: str, content: str) -> KnowledgeDocument:
        document = KnowledgeDocument(title=title, source=source)
        self.db.add(document)
        await self.db.flush()
        for idx, chunk in enumerate(chunk_text(content)):
            self.db.add(
                KnowledgeChunk(
                    document_id=document.id,
                    chunk_index=idx,
                    content=chunk,
                    embedding=self.embeddings.embed(chunk),
                )
            )
        await self.db.commit()
        await self.db.refresh(document, ["chunks"])
        return document

    async def search(self, query: str, limit: int = 5) -> list[dict]:
        query_embedding = self.embeddings.embed(query)
        rows = (await self.db.execute(select(KnowledgeChunk, KnowledgeDocument).join(KnowledgeDocument))).all()
        scored = []
        for chunk, doc in rows:
            scored.append(
                {
                    "document_id": doc.id,
                    "title": doc.title,
                    "content": chunk.content,
                    "score": round(cosine(query_embedding, chunk.embedding), 4),
                }
            )
        return sorted(scored, key=lambda item: item["score"], reverse=True)[:limit]

    async def context_for(self, objective: str) -> str:
        results = await self.search(objective, limit=3)
        return "\n\n".join(r["content"] for r in results if r["score"] > 0)
