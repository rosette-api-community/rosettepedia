#!/usr/bin/env python3
"""Resources for looking up language information based on ISO 639 standards."""

import csv

class Iso639(dict):
    """A subclass of dict for looking up information about natural languages.
    
    The language information is loaded from a TSV sourc file (by default 
    source='ISO-639.tsv').  The data in that file was taken from: 
    https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
    
    An instance of Iso639 is a dict that can be used to look up language
    information from a primary key.  This class is designed primarily for 
    keying on ISO 639-2/T three-letter codes, but it can be used for keying
    on other values.  The default key is '639-2/T', a three-letter code 
    standard.  However, if you want to look up languages based on a different 
    key you can supply it with the key parameter when you create a new Iso639 
    instance.
    
    You can see all the possible keys with:
    
    Iso639().keys -> [
        'Language family',
        'Language name',
        'Native name',
        '639-1',
        '639-2/T',
        '639-2/B',
        '639-3',
        '639-6',
        'Notes'
    ]
    
    Examples:
    
    If you want to get all info for German by its English name:
    
    Iso639('Language name')['German'] -> {
        '639-1': 'de',
        '639-2/B': 'ger',
        '639-2/T': 'deu',
        '639-3': 'deu',
        '639-6': 'deus',
        'Language family': 'Indo-European',
        'Language name': 'German',
        'Native name': 'Deutsch',
        'Notes': None
    }
    
    If you want to find the 639-1 two-letter code for German from its
    639-2/T three-letter code, 'deu':
    
    Iso639()['deu']['639-1'] -> 'de'
    
    To go the other direction from 639-1 to 639-2/T:
    
    Iso639('639-1')['de']['639-2/T'] -> 'deu'
    
    """
    def __init__(self, key='639-2/T', source='ISO-639.tsv'):
        self.source = source
        self.keys, self.languages = self.load()
        if not key in self.keys:
            raise ValueError('key must one of: {}'.format(repr(self.keys)))
        self.update({
            language.get(key): language for language in self.languages
            if language.get(key)
        })
    
    def load(self):
        with open(self.source, mode='r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            return reader.fieldnames, [row for row in reader]
