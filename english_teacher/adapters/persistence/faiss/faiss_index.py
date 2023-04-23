import faiss
import os
import numpy as np
from typing import List

embedding_ada_002_size = 1536
default_file_path = "index.faiss"


class FaissIndex:
    def __init__(
        self,
        index_filepath: str = default_file_path,
        embeddings_size: int = embedding_ada_002_size,
    ):
        self.index_filepath = index_filepath
        if os.path.exists(self.index_filepath):
            self.load_index()
        else:
            self.index = faiss.IndexFlatL2(embeddings_size)

    def add(self, embeddings: List[float]) -> int:
        np_embeddings = np.array(embeddings, dtype=np.float32).reshape(1, -1)
        new_embedding_id = self.index.ntotal
        self.index.add(np_embeddings)
        self.save_index()
        return new_embedding_id

    def add(self, embeddings: List[float]) -> int:
        np_embeddings = np.array(embeddings, dtype=np.float32).reshape(1, -1)
        new_embedding_id = self.index.ntotal
        self.index.add(np_embeddings)
        self.save_index()
        return new_embedding_id

    def search(
        self, query_embedding: List[float], k: int = 1, threshold: float = 0.1
    ) -> List[int]:
        np_query_embedding = np.array(query_embedding, dtype=np.float32).reshape(1, -1)
        distances, indices = self.index.search(np_query_embedding, k)
        indices = indices.flatten()
        distances = distances.flatten()
        indices = indices[distances < threshold]
        distances = distances[distances > threshold]
        return indices[:k].tolist()

    def save_index(self):
        faiss.write_index(self.index, self.index_filepath)

    def load_index(self):
        self.index = faiss.read_index(self.index_filepath)
