import argparse
import couch_client
import handlers

import tornado.ioloop
import tornado.web


def make_app(couchdb_url: str, debug: bool):
    return tornado.web.Application([
        (r"/([a-zA-Z0-9]+)", handlers.DatabaseHandler, dict(server_url=couchdb_url, call_impl=couch_client.default_call)),
        (r"/([a-zA-Z0-9]+)/index", handlers.IndexHandler, dict(server_url=couchdb_url, call_impl=couch_client.default_call)),
        (r"/([a-zA-Z0-9]+)/(.*)", handlers.MainHandler, dict(server_url=couchdb_url, call_impl=couch_client.default_call)),
    ], debug=debug)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start the pillowpile server.')
    parser.add_argument('--couchdb_url', type=str, default='http://127.0.0.1:5984', help='Base url to the CouchDB server')
    parser.add_argument('--port', type=int, default=8080, help='The port the server should listen on')
    parser.add_argument('--debug', dest='debug', action='store_true', help='Run the server in debug (livereload) mode')
    parser.set_defaults(debug=False)
    args = parser.parse_args()  

    app = make_app(couchdb_url=args.couchdb_url, debug=args.debug)
    app.listen(args.port)
    tornado.ioloop.IOLoop.current().start()