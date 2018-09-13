import configuration
import handlers

import tornado.ioloop
import tornado.web




def make_app(cfg: dict):
    return tornado.web.Application([
        (r"/", handlers.MainHandler, dict(cfg=cfg)),
    ])

if __name__ == "__main__":
    cfg = configuration.read()

    app = make_app(cfg)
    app.listen(cfg['port'])
    tornado.ioloop.IOLoop.current().start()