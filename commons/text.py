#!/usr/bin/env python
# Some material is Copyright (c) 2006 Bermi Ferrer Martinez
# His BSD-style cicense does require notice reproduction, but i've dropped the
# license text (as in the original source) at the end of the file nonetheless

"""
Text processing utilities
"""

import re

def pluralize(word):
    '''Pluralizes English nouns.'''
    
    rules = [
        ['(?i)(quiz)$' , '\\1zes'],
        ['^(?i)(ox)$' , '\\1en'],
        ['(?i)([m|l])ouse$' , '\\1ice'],
        ['(?i)(matr|vert|ind)ix|ex$' , '\\1ices'],
        ['(?i)(x|ch|ss|sh)$' , '\\1es'],
        ['(?i)([^aeiouy]|qu)ies$' , '\\1y'],
        ['(?i)([^aeiouy]|qu)y$' , '\\1ies'],
        ['(?i)(hive)$' , '\\1s'],
        ['(?i)(?:([^f])fe|([lr])f)$' , '\\1\\2ves'],
        ['(?i)sis$' , 'ses'],
        ['(?i)([ti])um$' , '\\1a'],
        ['(?i)(buffal|tomat)o$' , '\\1oes'],
        ['(?i)(bu)s$' , '\\1ses'],
        ['(?i)(alias|status)' , '\\1es'],
        ['(?i)(octop|vir)us$' , '\\1i'],
        ['(?i)(ax|test)is$' , '\\1es'],
        ['(?i)s$' , 's'],
        ['(?i)$' , 's']
    ]
    
    uncountable_words = ['equipment', 'information', 'rice', 'money', 'species', 'series', 'fish', 'sheep']
    
    irregular_words = {
        'person' : 'people',
        'man' : 'men',
        'child' : 'children',
        'sex' : 'sexes',
        'move' : 'moves'
    }
    
    lower_cased_word = word.lower();
    
    for uncountable_word in uncountable_words:
        if lower_cased_word[-1*len(uncountable_word):] == uncountable_word :
            return word
    
    for irregular in irregular_words.keys():
        match = re.search('('+irregular+')$',word, re.IGNORECASE)
        if match:
            return re.sub('(?i)'+irregular+'$', match.expand('\\1')[0]+irregular_words[irregular][1:], word)
    
    for rule in range(len(rules)):
        match = re.search(rules[rule][0], word, re.IGNORECASE)
        if match :
            groups = match.groups()
            for k in range(0,len(groups)) :
                if groups[k] == None :
                    rules[rule][1] = rules[rule][1].replace('\\'+str(k+1), '')
                    
            return re.sub(rules[rule][0], rules[rule][1], word)
    
    return word


def singularize(word):
    '''
    Convert `word' to its singular form.
    '''
    
    rules = [
        ['(?i)(quiz)zes$' , '\\1'],
        ['(?i)(matr)ices$' , '\\1ix'],
        ['(?i)(vert|ind)ices$' , '\\1ex'],
        ['(?i)^(ox)en' , '\\1'],
        ['(?i)(alias|status)es$' , '\\1'],
        ['(?i)([octop|vir])i$' , '\\1us'],
        ['(?i)(cris|ax|test)es$' , '\\1is'],
        ['(?i)(shoe)s$' , '\\1'],
        ['(?i)(o)es$' , '\\1'],
        ['(?i)(bus)es$' , '\\1'],
        ['(?i)([m|l])ice$' , '\\1ouse'],
        ['(?i)(x|ch|ss|sh)es$' , '\\1'],
        ['(?i)(m)ovies$' , '\\1ovie'],
        ['(?i)(s)eries$' , '\\1eries'],
        ['(?i)([^aeiouy]|qu)ies$' , '\\1y'],
        ['(?i)([lr])ves$' , '\\1f'],
        ['(?i)(tive)s$' , '\\1'],
        ['(?i)(hive)s$' , '\\1'],
        ['(?i)([^f])ves$' , '\\1fe'],
        ['(?i)(^analy)ses$' , '\\1sis'],
        ['(?i)((a)naly|(b)a|(d)iagno|(p)arenthe|(p)rogno|(s)ynop|(t)he)ses$' , '\\1\\2sis'],
        ['(?i)([ti])a$' , '\\1um'],
        ['(?i)(n)ews$' , '\\1ews'],
        ['(?i)s$' , ''],
    ];

    uncountable_words = ['equipment', 'information', 'rice', 'money', 'species', 'series', 'fish', 'sheep','sms'];

    irregular_words = {
        'people'    : 'person',
        'men'       : 'man',
        'children'  : 'child',
        'sexes'     : 'sex',
        'moves'     : 'move'
    }

    lower_cased_word = word.lower();

    for uncountable_word in uncountable_words:
        if lower_cased_word[-1*len(uncountable_word):] == uncountable_word :
            return word
        
    for irregular in irregular_words.keys():
        match = re.search('('+irregular+')$',word, re.IGNORECASE)
        if match:
            return re.sub('(?i)'+irregular+'$', match.expand('\\1')[0]+irregular_words[irregular][1:], word)
        
    for rule in range(len(rules)):
        match = re.search(rules[rule][0], word, re.IGNORECASE)
        if match :
            groups = match.groups()
            for k in range(0,len(groups)) :
                if groups[k] == None :
                    rules[rule][1] = rules[rule][1].replace('\\'+str(k+1), '')
                    
            return re.sub(rules[rule][0], rules[rule][1], word)
    
    return word

def conditionalPlural(numer_of_records, word) :
    '''Returns the plural form of a word if first parameter is greater than 1'''
    
    if numer_of_records > 1 :
        return pluralize(word)
    else :
        return word

def titleize(word, uppercase = '') :
    '''Converts an underscored or CamelCase word into a English sentence.
        The titleize function converts text like "WelcomePage",
        "welcome_page" or  "welcome page" to this "Welcome Page".
        If second parameter is set to 'first' it will only
        capitalize the first character of the title.'''

    if(uppercase == 'first'):
        return humanize(underscore(word)).capitalize()
    else :
        return humanize(underscore(word)).title()

def camelize(word):
    ''' Returns given word as CamelCased
    Converts a word like "send_email" to "SendEmail". It
    will remove non alphanumeric character from the word, so
    "who's online" will be converted to "WhoSOnline"'''
    return ''.join(w[0].upper() + w[1:] for w in re.sub('[^A-Z^a-z^0-9^:]+', ' ', word).split(' '))

def underscore(word) :
    ''' Converts a word "into_it_s_underscored_version"
    Convert any "CamelCased" or "ordinary Word" into an
    "underscored_word".
    This can be really useful for creating friendly URLs.'''
    
    return  re.sub('[^A-Z^a-z^0-9^\/]+','_', \
            re.sub('([a-z\d])([A-Z])','\\1_\\2', \
            re.sub('([A-Z]+)([A-Z][a-z])','\\1_\\2', re.sub('::', '/',word)))).lower()

def dasherize(word, reverse=False):
    """
    Converts hyphens to underscores.
    """
    replacements = ['-', '_']
    if reverse:
        replace.reverse()
    return word.replace(*replacements)

def humanize(word, uppercase = '') :
    '''Returns a human-readable string from word
    Returns a human-readable string from word, by replacing
    underscores with a space, and by upper-casing the initial
    character by default.
    If you need to uppercase all the words you just have to
    pass 'all' as a second parameter.'''
    
    if(uppercase == 'first'):
        return re.sub('_id$', '', word).replace('_',' ').capitalize()
    else :
        return re.sub('_id$', '', word).replace('_',' ').title()

def variablize(word) :
    '''Same as camelize but first char is lowercased
    Converts a word like "send_email" to "sendEmail". It
    will remove non alphanumeric character from the word, so
    "who's online" will be converted to "whoSOnline"'''
    word = camelize(word)
    return word[0].lower()+word[1:]

def ordinalize(number) :
    '''Converts number to its ordinal English form.
    This method converts 13 to 13th, 2 to 2nd ...'''
    tail = 'th'
    if number % 100 == 11 or number % 100 == 12 or number % 100 == 13:
        tail = 'th'
    elif number % 10 == 1 :
        tail = 'st'
    elif number % 10 == 2 :
        tail = 'nd'
    elif number % 10 == 3 :
        tail = 'rd'
    
    return str(number)+tail

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software to deal in this software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of this software, and to permit
# persons to whom this software is furnished to do so, subject to the following
# condition:
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THIS SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THIS SOFTWARE.