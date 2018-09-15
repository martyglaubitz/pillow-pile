import json
import tornado.httpclient
import typing
import urllib.parse

async def ensure_graph_doc(server_url: str, db_name: str, load_graph_from_db: typing.Callable):
    check_result = await load_graph_from_db(server_url, db_name)

async def load_graph_from_db(server_url: str, db_name: str):
    http_client = tornado.httpclient.AsyncHTTPClient()
    graph_doc_url = urllib.parse.urljoin(server_url, db_name + "/graph")
    response = await http_client.fetch(graph_doc_url)
    return json.loads(response.body)