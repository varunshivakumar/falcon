import falcon
from resources.api_index import ApiIndexResource
from resources.groups import GroupsResource
from resources.group import GroupResource
from resources.items import ItemsResource
from resources.item import ItemResource
from resources.group_items import GroupItemsResource
from resources.group_item import GroupItemResource
from resources.ContactQueryResource import ContactQueryResource
from resources.ContactResource import ContactResource

from utils.exceptions import handler
from middlewares.db_session import DbSessionManager
from db import Session
import pathlib
import whitenoise

APP_DIR = pathlib.Path(__file__).parent.absolute()
STATIC_CONTENT_DIR = str((pathlib.Path(APP_DIR)  / 'webapp-dist').absolute())

class StaticApp(whitenoise.WhiteNoise):
    def __call__(self, environ, start_response):
        path = whitenoise.base.decode_path_info(environ['PATH_INFO'])

        static_file = self._get_file(path)

        if static_file is None and not path.startswith('/api/'):
            static_file = self._get_file('/index.html')
            return self.serve(static_file, environ, start_response)
        elif static_file is None:
            return self.application(environ, start_response)
        else:
            return self.serve(static_file, environ, start_response)

    def _get_file(self, path):
        static_file = self.files.get(path)
        return static_file


def add_whitenoise(app):
    app = StaticApp(app, root=STATIC_CONTENT_DIR)
    app.index_file = 'index.html'
    return app


def get_app() -> falcon.API:
    app = falcon.API(middleware=[DbSessionManager(Session=Session)])

    app.add_route('/api', ApiIndexResource())
    app.add_route('/api/groups', GroupsResource())
    app.add_route('/api/groups/{id}', GroupResource())
    app.add_route('/api/items', ItemsResource())
    app.add_route('/api/items/{id}', ItemResource())
    app.add_route('/api/group/{group_id}/items', GroupItemsResource())
    app.add_route('/api/group/{group_id}/items/{item_id}', GroupItemResource())

    falcon_app = falcon.API()

    # This is safe because 'query' will never be an ID.
    falcon_app.add_route('/api/contact', ContactQueryResource())
    falcon_app.add_route('/api/contact/{contact_id}', ContactResource())


    app.add_error_handler(exception=Exception, handler=handler)

    app = add_whitenoise(app)
    return app


if __name__ == '__main__':
    from wsgiref import simple_server
    with simple_server.make_server('', 8000, get_app()) as httpd:
        httpd.serve_forever()
