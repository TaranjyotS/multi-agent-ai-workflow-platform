import asyncio
from pathlib import Path

from app.db.init_db import init_db
from app.db.session import AsyncSessionLocal
from app.services.knowledge_service import KnowledgeService


async def main() -> None:
    await init_db()
    content = Path("sample_data/enterprise_ai_policy.txt").read_text(encoding="utf-8")
    async with AsyncSessionLocal() as db:
        doc = await KnowledgeService(db).ingest("Enterprise AI Policy", "sample_data", content)
        print(f"Seeded document: {doc.id}")

if __name__ == "__main__":
    asyncio.run(main())
