from django import template


register = template.Library()

WORDS = ['редиска','плохой','дурак']

@register.filter()
def censor(value):
    if not isinstance(value, str):  
        raise ValueError("Значение не строка")  
    for word in WORDS:
        censored_word = word[0] + '*' * (len(word) - 1)  
        
        value = value.replace(word, censored_word)  
        value = value.replace(word.upper(), censored_word.upper())  
        value = value.replace(word.capitalize(), censored_word.capitalize())  

    return value 
        