import os

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

load_dotenv()


class QdrantAgent:

    def __init__(self):

        self.collection_name = os.getenv(
            "QDRANT_COLLECTION",
            "candidates"
        )

        # Local embedded Qdrant database
        self.client = QdrantClient(
            path="./data/qdrant_db"
        )

        # Embedding model
        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.create_collection()

    def create_collection(self):

        collections = self.client.get_collections()

        existing_collections = [
            collection.name
            for collection in collections.collections
        ]

        if self.collection_name not in existing_collections:

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE
                )
            )

            print(
                f"Collection '{self.collection_name}' created."
            )

    def generate_embedding(
        self,
        text: str
    ):

        embedding = self.embedding_model.encode(
            text
        )

        return embedding.tolist()

    def store_candidate(
        self,
        candidate_id: int,
        resume_text: str,
        candidate_data: dict
    ):

        embedding = self.generate_embedding(
            resume_text
        )

        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=candidate_id,
                    vector=embedding,
                    payload=candidate_data
                )
            ]
        )

        print(
            f"Candidate {candidate_id} stored successfully."
        )

    def search_candidates(
        self,
        query: str,
        limit: int = 5
    ):

        query_embedding = self.generate_embedding(
            query
        )

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=limit
        )

        output = []

        for point in results.points:

            output.append(
                {
                    "score": round(point.score, 3),
                    "candidate": point.payload
                }
            )

        return output