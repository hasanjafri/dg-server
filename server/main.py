from gino.ext.sanic import Gino
from sanic import Sanic
from sanic.response import json, file_stream
from sanic_cors import CORS
import os

from db.models import admin

app = Sanic(__name__)
CORS(app)

app.config.DB_PASSWORD = 'admin3'
app.config.DB_DATABASE = 'datagramDb'
db = Gino()
db.init_app(app)

@app.route("/", methods=['GET', 'OPTIONS'])
def test_online(request):
    return json({'msg': "Hello W/ Cors!"})

@app.route('/favicon.ico')
def favicon(request):
    return file_stream(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6969, debug=True)