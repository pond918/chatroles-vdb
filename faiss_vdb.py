from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import os
"""
for development only.
"""

db_path = './data'

embeddings = HuggingFaceEmbeddings(model_name='all-mpnet-base-v2')
db = FAISS.load_local(db_path, embeddings) if os.path.exists(
    db_path) else FAISS.from_texts([''], embeddings)


def upsert(text, meta):
    """
    Args:
            text: string
            meta: dict, must contain id.
    """
    db.aadd_texts([text], metadatas=[meta], ids=[meta['id']])
    db.save_local(db_path)


def search(text, size=4):
    docs = db.similarity_search(text, size)
    data = [doc.metadata for doc in docs if ('id' in doc.metadata)]
    return data
