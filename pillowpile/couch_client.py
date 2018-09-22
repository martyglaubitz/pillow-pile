import json
import tornado.httpclient
import typing
import urllib.parse

# Hide the notion of the tornado HTTP client from the code which interacts with couchdb
async def default_call(url: str, method: str = 'GET', body: dict = None, headers: dict = None):
    http_client = tornado.httpclient.AsyncHTTPClient()
    body_as_string = json.dumps(body) if type(body) is dict else None
    request = tornado.httpclient.HTTPRequest(url=url, method=method, body=body_as_string, headers=headers, allow_nonstandard_methods=True)
    response = await http_client.fetch(request, raise_error=False)
    response_parsed = json.loads(response.body) if response.body else None
    print(response)
    return response.code, response_parsed

class Client():
    
    def __init__(self, server_url: str, db_name: str, call_impl: typing.Callable):
        self.server_url = server_url
        self.db_name = db_name
        self.call_impl = call_impl

    async def create_db(self):
        return await self.call_impl(urllib.parse.urljoin(self.server_url, self.db_name), method='PUT')

    async def delete_db(self):
        return await self.call_impl(urllib.parse.urljoin(self.server_url, self.db_name), method='DELETE')

    async def delete_doc(self, updated_graph: dict, doc_ref: dict):
        await self.call_impl(urllib.parse.urljoin(self.server_url, self.db_name + '/graph'), method='PUT', body=updated_graph)
        response_code, doc = await self.get_doc(doc_ref)
        current_doc_rev = doc['_rev']
        return await self.call_impl(urllib.parse.urljoin(self.server_url, self.db_name + '/' + doc_ref['id']), 
            method='DELETE', headers={'If-Match': current_doc_rev})

    async def get_doc(self, doc_ref: dict):
        return await self.call_impl(urllib.parse.urljoin(self.server_url, self.db_name + '/' + doc_ref['id']))

    async def get_graph(self):
        return await self.call_impl(urllib.parse.urljoin(self.server_url, self.db_name + '/graph'))

    async def create_graph(self):
        return await self.call_impl(urllib.parse.urljoin(self.server_url, self.db_name + '/graph'), method='PUT', body={})

    async def update_existing_doc(self, doc_ref: dict, new_content: dict):
        response_code, current_doc = await self.get_doc(doc_ref)
        if response_code == 404:
            return response_code, current_doc

        current_doc_rev = current_doc['_rev']
        doc_id = doc_ref['id']
        return await self.call_impl(urllib.parse.urljoin(self.server_url, self.db_name + '/' + doc_id), 
            body=new_content, method='PUT', headers={'If-Match': current_doc_rev})

    async def create_doc(self, updated_graph: dict, new_doc_uuid: str, new_doc: dict):
        await self.call_impl(urllib.parse.urljoin(self.server_url, self.db_name + '/graph'), method='PUT', body=updated_graph)
        return await self.call_impl(urllib.parse.urljoin(self.server_url, self.db_name + '/' + new_doc_uuid), method='PUT', body=new_doc)
