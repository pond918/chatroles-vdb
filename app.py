import gradio as gr
import json
import faiss_vdb as vdb

def upsert_role(roleId, data):
    """
    body: { meta, content }
    """
    text = json.dumps(data['content'])
    meta = data['meta']
    meta['id'] = roleId
    cnt = vdb.upsert(text, meta)

    return cnt


i_upsert = gr.Interface(fn=upsert_role, inputs=["text", "json"],
                       outputs="text")
# gradio_interface.launch()


def search_roles(content, size):
    if size is None: size = 4
    size = int(size)
    text = json.dumps(content)
    docs = vdb.search(text, size)
    return docs


i_search = gr.Interface(
    fn=search_roles,
    inputs=["json", "number"],
    outputs="json"
)


def embed_texts(texts):
    arr = [vdb.embed_text(t)[0].tolist() for t in texts]
    json_arr = json.dumps(arr)
    return json_arr

i_embed = gr.Interface(
    fn=embed_texts,
    inputs='json',
    outputs="json"
)

demo = gr.TabbedInterface([i_upsert, i_search, i_embed], [
                          "upsert role", "search roles", "embed text"])

if __name__ == "__main__":
    demo.launch()
