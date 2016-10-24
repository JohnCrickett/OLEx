#import MySQLdb
import os
import tornado.ioloop
import tornado.web
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
# define("mysql_host", default="127.0.0.1:3306", help="blog database host")
# define("mysql_database", default="app", help="app database name")
# define("mysql_user", default="app", help="app database user")
# define("mysql_password", default="apppws", help="app database password")


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/form.html", title="OLEx App")


    def post(self):
        self.write("Your URL is: " + self.get_argument('url', ''))


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