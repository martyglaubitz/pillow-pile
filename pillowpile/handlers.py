import couch_client
import graph

import itertools
import json
import tornado.web
import typing
import uuid

OK_RANGE = range(200, 299)
LOCATION_RANGE = range(300, 399)
ITEM_EXISTS_RANGE = itertools.chain(OK_RANGE, LOCATION_RANGE)

class BaseHandler(tornado.web.RequestHandler):
    def get_path_components(self, path):
        return path.split('/')

    def get_client(self, db_name):
        if not db_name in self.clients:
            client = couch_client.Client(self.server_url, db_name, self.call_impl)
            self.clients[db_name] = client

        return self.clients[db_name]

    def finish_already_exists(self, message):
        self.set_status(409)
        self.finish({
            'error': 'already_exists',
            'message': message
        })

    def finish_not_found(self, message):
        self.set_status(404)
        self.finish({
            'error': 'not_found',
            'message': message
        })

    def finish_ok(self, message):
        self.set_status(200)
        self.finish({
            'message': message
        })

    def finish_with_original_response(self, response_code: int, response_body: dict):
        self.set_status(response_code)
        self.finish(response_body)

    def initialize(self, server_url: str, call_impl: typing.Callable):
        self.call_impl = call_impl
        self.clients = {}
        self.server_url = server_url

class DatabaseHandler(BaseHandler):

    async def delete(self, db_name):
        client = self.get_client(db_name)
        response_code, delete_db_response = await client.delete_db()
        self.finish_with_original_response(response_code, delete_db_response)

    async def get(self, db_name):
        client = self.get_client(db_name)
        code, graph_obj = await client.get_graph()
        if code not in ITEM_EXISTS_RANGE:
            self.finish_not_found('Database with name "' + db_name + '" does not exist')

        self.finish(graph_obj)

    async def put(self, db_name):
        client = self.get_client(db_name)
        response_code, create_db_response = await client.create_db()
        if response_code != 201:
            error = create_db_response['error']
            if error == 'file_exists':
                return self.finish_already_exists('Database with name "' + db_name + '" already exists.')

        # we can safwly ignore errors a this point, no problem if the graph already exists...
        response_code, _ = await client.create_graph()
        self.finish_with_original_response(201, {
            'ok': True,
            'message': 'Database with name "' + db_name + '" has been created.' 
        })


class MainHandler(BaseHandler):

    async def delete(self, db_name, path):
        path_components = self.get_path_components(path)
        client = self.get_client(db_name)

        response_code, graph_obj = await client.get_graph()
        if response_code == 404:
            return self.finish_not_found('Database with name "' + db_name + '" does not exist')

        doc_ref, _, _ = graph.get_document_entry_for_path(graph_obj, path_components)
        if not graph.delete_doc_node_from_graph(graph_obj, path_components):
            return self.finish_not_found('Document with path"' + path + '" does not exists.')

        response_code, delete_response = await client.delete_doc(graph_obj, doc_ref)
        self.finish_with_original_response(response_code, delete_response)    

    async def get(self, db_name, path):
        path_components = self.get_path_components(path)
        client = self.get_client(db_name)
        response_code, graph_obj = await client.get_graph()
        if response_code == 404:
            return self.finish_not_found('Database with name "' + db_name + '" does not exist')

        doc_ref, _, _ = graph.get_document_entry_for_path(graph_obj, path_components)
        if not doc_ref:
            return self.finish_not_found('Document with path"' + path + '" does not exists.')

        response_code, doc = await client.get_doc(doc_ref)
        if response_code == 404:
            return self.finish_not_found('Document with path"' + path + '" does not exists.')

        doc.pop('_id', None)
        doc.pop('_rev', None)

        self.finish(doc)


    async def put(self, db_name, path):
        request_body = json.loads(self.request.body)

        path_components = self.get_path_components(path)
        client = self.get_client(db_name)
        response_code, graph_obj = await client.get_graph()
        if response_code == 404:
            return self.finish_not_found('Database with name "' + db_name + '" does not exist')

        print(graph_obj)
        doc_ref, _, _ = graph.get_document_entry_for_path(graph_obj, path_components)
        if doc_ref and 'id' in doc_ref:
            response_code, update_response = await client.update_existing_doc(doc_ref, request_body)
            if response_code == 201:
                return self.finish_ok('Document with path"' + path + '" has been updated.')
            else:
                return self.finish_with_original_response(response_code, update_response)
                
        new_doc_uuid = str(uuid.uuid4())
        graph.create_doc_node_in_graph(graph_obj, path_components, new_doc_uuid)
        response_code, create_response = await client.create_doc(graph_obj, new_doc_uuid, request_body)
        self.finish_with_original_response(response_code, create_response)

