from requests import get
from bs4 import BeautifulSoup
from bs4.element import Comment


def log(message):
    print(message)


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def get_url(url):
    '''
    :param url: destination url
    :return: content of response
    '''
    try:
        response = get(url)
        if is_good_response(response):
            content = response.content
        else:
            log('url response is not good!')
            content = None

    except Exception as e:
        log('failed to retrieve the url, %s' % str(e))
        content = None

    return content


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(content):
    soup = BeautifulSoup(content, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)
