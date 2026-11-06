import faiss
import numpy as np


def create_vector_store(embeddings):
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    embeddings = np.array(embeddings).astype("float32")

    index.add(embeddings)

    return index


def search_vector_store(index, query_embedding, top_k=2):
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    return distances, indices
if __name__ == "__main__":

    embeddings = np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.9, 0.1, 0.0]
    ])

    index = create_vector_store(embeddings)

    query = np.array([[1.0, 0.0, 0.0]])

    distances, indices = search_vector_store(index, query)

    print("Distances:", distances)
    print("Indices:", indices)