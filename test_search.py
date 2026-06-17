from agents.qdrant_agent import QdrantAgent


def main():

    qdrant = QdrantAgent()

    results = qdrant.search_candidates(
        query="Machine Learning Engineer with NLP experience",
        limit=5
    )

    print("\nSearch Results:\n")

    for result in results:

        print("-" * 50)
        print(
            f"Similarity Score: {result['score']}"
        )
        print(result["candidate"])


if __name__ == "__main__":
    main()