from gevent.wsgi import WSGIServer
from tornado.httpserver import HTTPServer
from SnowNLP_JS import app

http_server = WSGIServer(('10.68.68.116', 5000), app)
http_server.serve_forever()