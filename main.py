import tornado.ioloop
from web.index import make_app

app = make_app()

if __name__ == '__main__':
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
else:
    import tornado.wsgi
    app = tornado.wsgi.WSGIAdapter(app)
