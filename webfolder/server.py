from webnode.node import Node
from webnode.renderer import Renderer
from webnode.utils import to_wsgi_app
from wsgiref.simple_server import make_server


class Server:

    def __init__(self, port=8000):
        self._port = port
        self._root = Node("")

        index_node = Node("index", self._root)
        index_node.get(index)

    def start(self):
        app = to_wsgi_app(self._root)
        server = make_server('', self._port, app)
        print("Serving on port {}...".format(self._port))
        server.serve_forever()


def index(**kwargs):
    return Renderer.render('index', **kwargs), 'text/html', '200 OK'


if __name__ == "__main__":
    import webnode

    webnode.config.update({
        'template_dir': '../templates'
    })
    Server().start()
