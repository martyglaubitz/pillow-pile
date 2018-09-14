import argparse
import handlers

import tornado.ioloop
import tornado.web


def make_app(args):
    return tornado.web.Application([
        (r"/", handlers.MainHandler, dict(cfg=args)),
    ], debug=args.debug)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start the pillowpile server.')
    parser.add_argument('--port', type=int, default=8080, help='The port the server should listen on')
    parser.add_argument('--debug', dest='debug', action='store_true', help='Run the server in debug (livereload) mode')
    parser.set_defaults(debug=False)
    args = parser.parse_args()  

    app = make_app(args)
    app.listen(args.port)
    tornado.ioloop.IOLoop.current().start()