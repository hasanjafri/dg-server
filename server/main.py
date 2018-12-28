from gino import Gino
from sanic import Sanic
from sanic.response import json, file_stream
from sanic_cors import CORS
import os

app = Sanic(__name__)
CORS(app)

db = Gino()

@app.route("/", methods=['GET', 'OPTIONS'])
def test_online(request):
    return json({'msg': "Hello W/ Cors!"})

@app.route('/favicon.ico')
def favicon(request):
    return file_stream(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6969)