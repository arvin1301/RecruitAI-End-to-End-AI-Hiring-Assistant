from fastapi import APIRouter

from agents.qdrant_agent import (
    QdrantAgent
)

router = APIRouter()


@router.get("/")
def search_candidate(
    query: str
):

    qdrant = QdrantAgent()

    results = (
        qdrant.search_candidates(
            query=query,
            limit=5
        )
    )

    return results