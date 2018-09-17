import json
import tornado.httpclient
import typing
import urllib.parse

# Hide the notion of the tornado HTTP client from the code which interacts with couchdb
async def default_call(url: str, method: str = 'GET', body: dict = None, headers: dict = None):
    http_client = tornado.httpclient.AsyncHTTPClient()
    body_as_string = json.dumps(body) if type(body) is dict else None
    request = tornado.httpclient.HTTPRequest(url=url, method=method, body=body_as_string)
    response = await http_client.fetch(request, raise_error=False)
    return json.loads(response.body)

class Client():
    
    def __init__(self, server_url: str, db_name: str, call_impl: typing.Callable):
        self.server_url = server_url
        self.db_name = db_name
        self.call_impl = call_impl

    async def get_graph(self):
        return await self.call_impl(urllib.parse.urljoin(self.server_url, self.db_name + "/graph"))

    async def ensure_graph(self):
        response = await self.call_impl(urllib.parse.urljoin(self.server_url, self.db_name + "/graph"), method='PUT', body={})
        print(response)

