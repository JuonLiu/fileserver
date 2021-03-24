import os
import sys
from flask import Flask
from flask_cors import *
from werkzeug.middleware.proxy_fix import ProxyFix

path = os.path.abspath('.')
if 'src' in path:
    path = os.path.abspath('..')
if path not in sys.path:
    sys.path.append(path)

from src.get.views import get
from src.settings import DEBUG, SECRET_KEY
from src.upload.views import upload

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

CORS(app, supports_credentials=True)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024
app.secret_key = SECRET_KEY
app.register_blueprint(upload, url_prefix='/upload')
app.register_blueprint(get, url_prefix='/get')


@app.route('/test')
def test():
    return 'test2'


@app.route('/upload_qr', methods=['POST'])
def upload_qr():
    from src.upload.views import upload_qr
    return upload_qr()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8084, debug=DEBUG, use_reloader=True)
