from app.services.llm import ask_llm


def answer_with_context(question: str, documents: list[dict]) -> str:
    context = "\n\n".join(
        f"Title: {doc['title']}\nContent: {doc['content']}"
        for doc in documents
    )

    prompt = f"""
You are OpsIntel, an enterprise operations assistant.

Answer the question using only the provided context.
If the context is insufficient, say so clearly.

Question:
{question}

Context:
{context}
"""

    return ask_llm(prompt)
