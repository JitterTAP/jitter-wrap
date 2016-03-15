import argparse
import logging
import tornado.web
import tornado.ioloop
import tornado.websocket
import subprocess
import settings

class HealthCheckHandler(tornado.web.RequestHandler): # noqa
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    def get(self):
        self.write('ok')


class JitterWrapHandler(tornado.web.RequestHandler): # noqa
    def post(self):
        msg = self.request.body
        try:
            subprocess.call(msg.split(" "))
            self.set_status(200)
        except Exception as e:
            print e
            self.set_status(500)
            self.write("Exception %s" % e)




ROUTES = [
    (r'/health', HealthCheckHandler),
    (r'/jitterwrap', JitterWrapHandler, )
]


APPLICATION = tornado.web.Application(ROUTES)


def main():
    parser = argparse.ArgumentParser(description='Routing handle server')
    args = parser.parse_args()

    APPLICATION.listen(settings.PORT)
    logging.info('Serving on port: %d', settings.PORT)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
