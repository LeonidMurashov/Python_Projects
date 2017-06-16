import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import random
from tornado.options import define, options
import urllib.request  as urllib2

define("port", default=8888, help="run on the given port", type=int)

from pymongo import MongoClient

client = MongoClient("mongodb://l.murashov:04101576@ds155841.mlab.com:55841/hotdogs1576")
database = client["hotdogs1576"]
collection = database["hotdogs"]
hotdogs = list(collection.find())

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        hotdog = random.choice(hotdogs)
        good = False
        while(good):
            hotdog = random.choice(hotdogs)
            try:
                src = urllib2.urlopen(hotdog["link"])
                print(src)
                good = True
            except:
                pass
        self.render("index.html", hotdog=hotdog)


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", MainHandler),
    ], debug=True)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()