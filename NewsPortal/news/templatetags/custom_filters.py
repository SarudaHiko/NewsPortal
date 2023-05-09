from django import template


register = template.Library()


UNWANTED_WORDS = ['редиска']  # список нежелательных слов
forbidden_words = ['']


@register.filter(name='censor')
def censor(text):
    for word in UNWANTED_WORDS:
        if word in text:
            text = text.replace(word[1:len(word)], f'{len(word) * "*"}')
            return text
        else:
            return text


@register.filter(name='censor_2')
def censor_2(text):
    for word in text:
        if word in forbidden_words:
            text = text.replace(word[1:-1], len(word[1:-1] * '*'))
            return text
        else:
            return text

