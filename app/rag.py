from app.llm import ask_llm


def rag_query(db, query: str):
    # 1. Recuperar contexto relevante
    docs = db.similarity_search(query, k=3)

    context = "\n".join([doc.page_content for doc in docs])

    # 2. Construir prompt
    prompt = f"""
You are a precise assistant.

Use ONLY the context below to answer.
If the answer is not in the context, say "I don't know".


Context:
{context}

Question:
{query}

Answer:
"""

    # 3. Llamar al LLM
    response = ask_llm(prompt)

    return response