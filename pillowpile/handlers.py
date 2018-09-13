import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, cfg: dict):
        self.cfg = cfg

    async def get(self):
        self.set_header('Content-Type', 'application/json')
        self.write(self.cfg)