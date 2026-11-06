from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):
    embeddings = model.encode(chunks)

    return embeddings


if __name__ == "__main__":
    chunks = [
        "Python is a programming language.",
        "RAG combines retrieval with generation.",
        "Embeddings represent text as numerical vectors."
    ]

    embeddings = create_embeddings(chunks)

    print("Number of chunks:", len(chunks))
    print("Embedding shape:", embeddings.shape)
    print("First embedding:")
    print(embeddings[0])