import json
from gevent import pywsgi
import faiss_vdb as vdb

from flask import (
    Flask,
    request
)

app = Flask(__name__)


@app.route('/api/roles', methods=['PATCH'])
def upsert_role():
    """
    body: { meta, content }
    """
    roleId = request.args.get('id')
    data = request.json

    text = json.dumps(data['content'])
    meta = data['meta']
    meta['id'] = roleId
    vdb.upsert(text, meta)

    return 'ok'


@app.route('/api/roles/search', methods=['GET'])
def search_roles():
    size = request.args.get('size')
    data = request.json
    text = json.dumps(data)
    docs = vdb.search(text, size)
    return docs


if __name__ == '__main__':
    # development
    # app.run(debug=True)

    # production
    server = pywsgi.WSGIServer(('0.0.0.0', 80), app)
    server.serve_forever()
