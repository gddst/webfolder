from webnode.node import Node
from webnode.renderer import Renderer
from webnode.utils import to_wsgi_app
from wsgiref.simple_server import make_server
from pathlib import Path

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
    kwargs['dirpath'] = webnode.config.get('root', '.')
    kwargs['dirnames'] = []
    kwargs['filenames'] = []
    p = Path(kwargs['dirpath'])
    for x in p.iterdir():
        if x.is_dir():
            kwargs['dirnames'].append(x)
        else:
            kwargs['filenames'].append(x)

    return Renderer.render('index', **kwargs), 'text/html', '200 OK'


if __name__ == "__main__":
    import webnode
    import os
    import sys

    if len(sys.argv) < 2:
        os.exit(1)

    webnode.config.update({
        'template_dir': os.path.join('..', 'templates'),
        'locale_dir': os.path.join('..', 'resources', 'locale'),
        'root': sys.argv[1]
    })

    Server().start()
