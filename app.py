from collections import defaultdict
#import MySQLdb not available for python 3 in anaconda
import lxml.html
import operator
import os
from tornado.httpclient import AsyncHTTPClient
import tornado.ioloop
import tornado.web
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/form.html", title="OLEx App")

    @tornado.web.asynchronous
    def post(self):
        self.write("Your URL is: " + self.get_argument('url', ''))
        http_client = AsyncHTTPClient()
        http_client.fetch(self.get_argument('url', ''),
                          callback=self.on_fetch)


    def on_fetch(self, response):
        if response.error:
            print("Error:", response.error)
            self.render("templates/error.html", title="OLEx App", message = response.error)
        else:
            document = lxml.html.document_fromstring(response.body)
            wordmap = self.generate_wordmap(document.text_content())
            top100 = sorted(wordmap.items(), key=operator.itemgetter(1), reverse=True)[:100]

            self.render("templates/result.html", title="OLEx App", content = top100)


    def generate_wordmap(self, text):
        words = text.split()
        counts = defaultdict(int)
        for word in words:
            counts[word] += 1
        return counts





def make_app():
    settings = {'debug': True,
                'static_path': os.path.join(os.path.dirname(__file__), "static")
               }

    return tornado.web.Application([
        (r"/", MainHandler),
    ], **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()