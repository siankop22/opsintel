import json
from pathlib import Path

from app.db.database import SessionLocal
from app.retrieval.vector_search import vector_search
from app.retrieval.keyword_search import keyword_search
from app.retrieval.hybrid import hybrid_search
from app.retrieval.reranker import rerank


def get_titles(results):
    titles = []

    for result in results:
        if isinstance(result, dict):
            titles.append(result["title"])
        else:
            titles.append(result.title)

    return titles


def main():
    eval_path = Path("evals/retrieval_queries.json")
    cases = json.loads(eval_path.read_text())

    methods = {
        "Vector": {"correct": 0, "rr": 0.0},
        "BM25": {"correct": 0, "rr": 0.0},
        "Hybrid": {"correct": 0, "rr": 0.0},
        "Hybrid + Reranker": {"correct": 0, "rr": 0.0},
    }

    session = SessionLocal()

    try:
        for case in cases:
            query = case["query"]
            expected = case["expected_title"]

            vector_results = vector_search(session, query, limit=3)
            bm25_results = keyword_search(session, query, limit=3)
            hybrid_results = hybrid_search(session, query, limit=3)
            reranked_results = rerank(query, hybrid_results, limit=3)

            results_by_method = {
                "Vector": get_titles(vector_results),
                "BM25": get_titles(bm25_results),
                "Hybrid": get_titles(hybrid_results),
                "Hybrid + Reranker": get_titles(reranked_results),
            }

            print(f"\nQuery: {query}")
            print(f"Expected: {expected}")

            for method, titles in results_by_method.items():
                top_title = titles[0] if titles else None

                if top_title == expected:
                    methods[method]["correct"] += 1

                if expected in titles:
                    rank = titles.index(expected) + 1
                    methods[method]["rr"] += 1 / rank

                marker = "PASS" if top_title == expected else "FAIL"
                print(f"{method:20} {marker:4} | Top: {top_title}")

        total = len(cases)

        print("\n============================================================")
        print("RETRIEVAL EVALUATION")
        print("============================================================")

        for method, metrics in methods.items():
            accuracy = metrics["correct"] / total
            mrr = metrics["rr"] / total

            print(
                f"{method:20} "
                f"Top-1: {metrics['correct']}/{total} ({accuracy:.1%}) | "
                f"MRR@3: {mrr:.3f}"
            )

    finally:
        session.close()


if __name__ == "__main__":
    main()
