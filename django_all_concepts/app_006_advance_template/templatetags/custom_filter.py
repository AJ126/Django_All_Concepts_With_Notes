from django import template

register = template.Library()

# create the below function to make first latter of value is upper case
def fist_one_letter_upper(value):
    result = value[0].upper() + value[1:]
    return result
register.filter('firstLettercapital', fist_one_letter_upper)

# Capitalize the first letter of every word
@register.filter(name='firstletterUpper')
def first_letter_capital_for_every_string(value):
    return value.title()
    # return ' '.join(word.capitalize() for word in value.split())