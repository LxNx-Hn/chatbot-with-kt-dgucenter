import hashlib
import re

import numpy as np

from config.constants import EMBEDDING_MODEL
from config.settings import KEYWORD_EMBEDDING_DIMENSIONS, RETRIEVAL_PROVIDER


class SentenceTransformerEmbeddingModel:
    def __init__(self):
        from sentence_transformers import SentenceTransformer

        self.embedder = SentenceTransformer(EMBEDDING_MODEL)

    def encode(self, texts, convert_to_numpy=True, show_progress_bar=False):
        return self.embedder.encode(
            texts,
            convert_to_numpy=convert_to_numpy,
            show_progress_bar=show_progress_bar,
        )


class KeywordEmbeddingModel:
    def __init__(self):
        self.dimensions = KEYWORD_EMBEDDING_DIMENSIONS

    def encode(self, texts, convert_to_numpy=True, show_progress_bar=False):
        if isinstance(texts, str):
            return self._encode_one(texts)

        encoded = [self._encode_one(text) for text in texts]
        if not encoded:
            return np.empty((0, self.dimensions), dtype=np.float32)
        return np.vstack(encoded)

    def _encode_one(self, text):
        vector = np.zeros(self.dimensions, dtype=np.float32)
        for token in self._tokens(str(text)):
            index = self._stable_index(token)
            vector[index] += 1.0

        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        return vector

    def _tokens(self, text):
        tokens = []
        for token in re.findall(r"[0-9A-Za-z가-힣]+", text.lower()):
            tokens.append(token)
            if len(token) >= 3:
                tokens.extend(token[i : i + 2] for i in range(len(token) - 1))
        return tokens

    def _stable_index(self, token):
        digest = hashlib.blake2b(token.encode("utf-8"), digest_size=4).digest()
        return int.from_bytes(digest, "big") % self.dimensions


class EmbeddingModel:
    def __init__(self):
        if RETRIEVAL_PROVIDER == "keyword":
            self.provider = KeywordEmbeddingModel()
        elif RETRIEVAL_PROVIDER == "embedding":
            self.provider = SentenceTransformerEmbeddingModel()
        else:
            raise RuntimeError(f"지원하지 않는 RETRIEVAL_PROVIDER 값입니다: {RETRIEVAL_PROVIDER}")

    def encode(self, texts, convert_to_numpy=True, show_progress_bar=False):
        return self.provider.encode(
            texts,
            convert_to_numpy=convert_to_numpy,
            show_progress_bar=show_progress_bar,
        )


# 전역 인스턴스 (기존 호환성 유지)
embedding_instance = EmbeddingModel()
