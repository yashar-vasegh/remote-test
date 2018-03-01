from string import punctuation

def clean_text(txt):
    txt = ''.join([i for i in txt if i not in punctuation])
    if len(txt) < 3:
        return None
    if txt.isdigit():
        return None
    return txt.lower()

def get_words(txt):
    return filter(None, [clean_text(i) for i in txt.split()])

def create_dict_words(list_of_words):
    result = dict()
    for item in list_of_words:
        try:
            result[item] += 1
        except KeyError:
            result[item] = 1
    return result
