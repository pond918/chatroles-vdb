from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import os

import numpy as np
"""
for development only.
"""

db_path = './data'

embeddings = HuggingFaceEmbeddings(model_name='all-mpnet-base-v2')
# TODO clear empty entry on load
db = FAISS.load_local(db_path, embeddings) if os.path.exists(
    db_path) else FAISS.from_texts([''], embeddings, metadatas=[{"none": 1}])


def upsert(text, meta):
    """
    Args:
            text: string
            meta: dict, must contain id.
    Returns:
            total docs count
    """
    id = clear_existing(meta['id'])
    db.add_texts([text], metadatas=[meta], ids=[id])
    db.save_local(db_path)

    return True


def total():
    return len(db.index_to_docstore_id)


def search(text, size=4, offset=0):
    docs = db.similarity_search(text, size)
    full = size <= len(docs)
    docs = docs[offset:]
    data, deled = [], 0
    for doc in docs:
        if 'id' in doc.metadata: data.append(doc.metadata)
        elif 'none' not in doc.metadata: deled = deled + 1
    if (full and deled > 0):
        data = data + search(text, size + deled, size)
    return data


# def FAISS_append_txt(text, meta, id, doc):
#     """ hack """
#     doc.page_content = text
#     doc.metadata = meta
#     emb = [db.embedding_function(text)]
#     vector = np.array(emb, dtype=np.float32)
#     if db._normalize_L2:
#         faiss = db.dependable_faiss_import()
#         faiss.normalize_L2(vector)
#     db.index.add(vector).update()
#     starting_len = len(self.index_to_docstore_id)
#     # TODO set db.index_to_docstore_id[old_idx] = ''

def clear_existing(id):
    while True:
        doc = db.docstore.search(id)
        if not doc or isinstance(doc, str):
            print('[VDB] insert new doc', id)
            return id

        # emb = embed_text(doc.page_content)
        # idx = db.index.assign(emb)
        # db.index.remove_ids()
        doc.metadata = {}  # clear meta to disable it
        doc.page_content = {}
        id = id + '#'


def embed_text(txt):
    emb = [db.embedding_function(txt)]
    vector = np.array(emb, dtype=np.float32)
    if db._normalize_L2:
        faiss = db.dependable_faiss_import()
        faiss.normalize_L2(vector)
    return vector
