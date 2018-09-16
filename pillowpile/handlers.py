import couch_client

import tornado.web
import typing
import urllib.parse

class MainHandler(tornado.web.RequestHandler):

    def db_name(self):
        split_result = urllib.parse.urlsplit(self.request.uri)
        path_parts = split_result.path.split('/')

        if len(path_parts) >= 2:
            return path_parts[1]

        return None

    async def get_client(self):
        db_name = self.db_name()
        print('db: ' + db_name)

        if not db_name in self.clients:
            client = couch_client.Client(self.server_url, db_name, self.call_impl)
            self.clients[db_name] = client

        return self.clients[db_name]

    def initialize(self, server_url: str, call_impl: typing.Callable):
        self.call_impl = call_impl
        self.clients = {}
        self.server_url = server_url

    async def get(self):
        client = self.get_client()