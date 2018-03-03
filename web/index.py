import tornado.web

import os

from utils.db import DB
from utils.hasher import validate_private_key
from utils.scraper import get_url, text_from_html
from utils.parser import get_words, create_dict_words
from app_setting import PUBLIC_KEY, TEMPLATE_DIR


def read_template(request, filename=None, content=''):
    body = open(os.path.join(TEMPLATE_DIR, 'body.html'), 'r').read()
    if has_permission_continue(request):
        links = ' <a href="/">Get Url</a> <a href="/get_result">Get Result</a> <a href="/logout"> logout </a> '
    else:
        links = ''

    if filename:
        content = open(os.path.join(TEMPLATE_DIR, filename), 'r').read()
    return body.format(links=links, content=content)


def has_permission_continue(request):
    return validate_private_key(request.get_cookie("key"))


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        if not has_permission_continue(self):
            self.write(read_template(self, 'welcome.html'))
        else:
            self.write(read_template(self,'get_site_address.html'))

    def post(self):
        key = self.get_argument('key', '')
        if validate_private_key(key):
            try:
                self.set_cookie('key', key)
            except:
                self.write(read_template(self, 'welcome.html'))
                self.write('your key not validated!')
            else:
                self.redirect('/get_url')
        else:
            self.write(read_template(self, 'welcome.html'))
            self.write('your key not validated!')


class GetUrl(tornado.web.RequestHandler):
    def get(self):
        self.write(read_template(self, 'get_site_address.html'))

    def post(self):

        if not has_permission_continue(self):
            self.redirect('/')

        url = self.get_argument('site-address', '')
        if url:
            try:
                content = get_url(url)
            except:
                self.write(read_template(self, 'get_site_address.html'))
                self.write('could not retrieve your url')
            else:
                if content:
                    text = text_from_html(content)
                    dict_of_words = create_dict_words(get_words(text))
                    for item in dict_of_words:
                        db = DB(private_key=self.get_cookie("key"), public_key=PUBLIC_KEY)
                        try:
                            db.update_db_word(item, dict_of_words[item])
                        except:
                            pass

                    self.write('database updated<a href="/get_result">get result</a>')
                else:
                    self.write(read_template(self, 'get_site_address.html'))
                    self.write('could not retrieve your url')
        else:
            self.write(read_template(self, 'get_site_address.html'))
            self.write('could not retrieve your url')


class GetResult(tornado.web.RequestHandler):
    def normalize_font(self, size, max_old, min_old):
        return (50 / (max_old-min_old) * (size -max_old)) + 60

    def get(self):
        if not has_permission_continue(self):
            self.redirect('/')
        output = ''
        output += '<table border=1>'
        output += '<tr><td>word</td><td>count</td></tr>'
        db = DB(private_key=self.get_cookie("key"), public_key=PUBLIC_KEY)
        result = db.get_top_100()
        for item in result:
            font_size = self.normalize_font(item[1], result[0][1], result[-1][1])
            output += '<tr style="font-size:%spx"><td>%s</td><td>%s</td></tr>' % (font_size, item[0].decode(), item[1])
        output += '</table>'
        self.write(read_template(self, '', content=output))


class LogOut(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie('key')
        self.redirect('/')


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/get_url", GetUrl),
        (r"/get_result", GetResult),
        (r"/logout", LogOut)
    ])
