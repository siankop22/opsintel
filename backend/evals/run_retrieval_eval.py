import json
from pathlib import Path

from app.db.database import SessionLocal
from app.retrieval.hybrid import hybrid_search
from app.retrieval.reranker import rerank


def main():
    eval_path = Path("evals/retrieval_queries.json")
    cases = json.loads(eval_path.read_text())

    session = SessionLocal()

    correct = 0

    try:
        for case in cases:
            query = case["query"]
            expected = case["expected_title"]

            documents = hybrid_search(session, query, limit=10)
            results = rerank(query, documents, limit=3)

            top_title = results[0]["title"] if results else None
            passed = top_title == expected

            if passed:
                correct += 1

            print(f"\nQuery: {query}")
            print(f"Expected: {expected}")
            print(f"Top result: {top_title}")
            print(f"Result: {'PASS' if passed else 'FAIL'}")

        accuracy = correct / len(cases)

        print("\n----------------------------")
        print(f"Top-1 Accuracy: {correct}/{len(cases)} = {accuracy:.1%}")

    finally:
        session.close()


if __name__ == "__main__":
    main()
