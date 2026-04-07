from sentence_transformers import CrossEncoder

reranker_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank_documents(question: str, documents: list[str], metadatas: list[dict], top_n: int = 3):
    if not documents:
        return []

    pairs = [[question, doc] for doc in documents]
    scores = reranker_model.predict(pairs)

    ranked_results = sorted(
        [
            {
                "text": doc,
                "metadata": metadata,
                "score": float(score)
            }
            for doc, metadata, score in zip(documents, metadatas, scores)
        ],
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked_results[:top_n]