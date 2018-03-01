import tornado.ioloop
import tornado.web

from utils.db import DB
from utils.hasher import create_key, decrypt
from utils.scraper import get_url, text_from_html
from utils.parser import get_words, create_dict_words
from app_setting import public_key

def read_template(filename):
    return open('templates/%s' % filename, 'r').read()

def validate_cookie(key):
    try:
        create_key(key, public_key=public_key)
    except Exception as e:
        return False
    return True

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        if not validate_cookie(self.get_cookie("key")):
            self.write(read_template('welcome.html'))
        else:
            self.write(read_template('get_site_address.html'))

    def post(self):
        key = self.get_argument('key', '')
        if validate_cookie(key):
            try:
                self.set_cookie('key', key)
            except:
                print('not validated')
                self.write(read_template('welcome.html'))
            else:
                self.write(read_template('get_site_address.html'))
        else:
            print('not validated')
            self.write(read_template('welcome.html'))

class GetUrl(tornado.web.RequestHandler):
    def post(self):
        url = self.get_argument('site-address', '')
        print(self.get_cookie("key"), public_key)
        if url:
            content = get_url(url)
            if content:
                text = text_from_html(content)
                dict_of_words = create_dict_words(get_words(text))
                for item in dict_of_words:
                    db = DB(private_key=self.get_cookie("key"), public_key=public_key)
                    try:
                        db.update_db_word(item,dict_of_words[item])
                    except:
                        pass

                self.write('database updated<a href="/get_result">get result</a>')
        else:
            self.write('not valid url')

class GetResult(tornado.web.RequestHandler):
    def normalize_font(self, size, max_old, min_old):
        return (50 / (max_old-min_old) * (size -max_old)) + 60

    def get(self):
        self.write(read_template('header.html'))
        self.write('<table>')
        self.write('<tr><td>word</td><td>count</td></tr>')
        db = DB(private_key=self.get_cookie("key"), public_key=public_key)
        result = db.get_top_100()
        for item in result:
            font_size = self.normalize_font(item[1], result[0][1], result[-1][1])
            self.write('<tr style="font-size:%spx"><td>%s</td><td>%s</td></tr>' %(font_size, item[0], item[1]))
        self.write('</table>')


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/get_url", GetUrl),
        (r"/get_result", GetResult),

    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()