import couch_client

import tornado.web
import typing

class MainHandler(tornado.web.RequestHandler):

    def get_path_components(self, path):
        return path.split('/')

    def db_name(self, path):
        path_parts = self.get_path_components(path)

        if path_parts:
            return path_parts[0]

        return None

    def get_client(self, db_name):
        if not db_name in self.clients:
            client = couch_client.Client(self.server_url, db_name, self.call_impl)
            self.clients[db_name] = client

        return self.clients[db_name]

    def initialize(self, server_url: str, call_impl: typing.Callable):
        self.call_impl = call_impl
        self.clients = {}
        self.server_url = server_url

    async def get(self, path):
        db_name = self.db_name(path)
        client = self.get_client(db_name)
        graph = await client.get_graph()
        self.finish(graph)



