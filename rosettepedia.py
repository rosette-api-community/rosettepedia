#!/usr/bin/env python3

"""Augment Rosette API entity extraction results with information from
Wikipedia."""

import csv
import json
import os
import sys
import urllib
import warnings

from operator import methodcaller
from getpass import getpass
from iso639 import Iso639
from functools import lru_cache

from rosette.api import API, DocumentParameters
import wptools
import mwparserfromhell

DEFAULT_ROSETTE_API_URL = 'https://api.rosette.com/rest/v1/'

def dump(obj):
    """Dump dict-like object to a file as JSON"""
    print(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', file=sys.stdout)

def request(content, endpoint, api, language=None, uri=False, **kwargs):
    """Request Rosette API results for the given content and endpoint.

    This method gets the requested results from the Rosette API as JSON.  If
    api's output parameter has been set to "rosette" then the JSON will consist
    of an A(nnotated) D(ata) M(odel) or ADM.  An ADM is a Python dict
    representing document content, annotations of the document content,
    and document metadata.
    
    content:  path or URI of a document for the Rosette API to process
    endpoint: a Rosette API endpoint string (e.g., 'entities')
              (see https://developer.rosette.com/features-and-functions)
    api:      a rosette.api.API instance
              (e.g., API(user_key=<key>, service_url=<url>))
    language: an optional ISO 639-2 T language code
              (the Rosette API will automatically detect the language of the
              content by default)
    uri:      specify that the content is to be treated as a URI and the
              the document content is to be extracted from the URI
    kwargs:   additional keyword arguments
              (e.g., if endpoint is 'morphology' you can specify facet='lemmas';
              see https://developer.rosette.com/features-and-functions for
              complete documentation)
    """
    parameters = DocumentParameters()
    if uri:
        parameters['contentUri'] = content
    else:
        parameters['content'] = content
    parameters['language'] = language
    adm = methodcaller(endpoint, parameters, **kwargs)(api)
    return adm

def get_content(content, uri=False):
    """Load content from file or stdin"""
    if content is None:
        content = sys.stdin.read()
    elif os.path.isfile(content):
        with open(content, mode='r') as f:
            content = f.read()
    # Rosette API may balk at non-Latin characters in a URI so we can get urllib
    # to %-escape the URI for us
    if uri:
        unquoted = urllib.parse.unquote(content)
        content = urllib.parse.quote(unquoted, '/:')
    return content

def dump_content(content, filename):
    """Dump content to file or stdout"""
    if filename is None:
        print(content, file=sys.stdout)
    else:
        with open(filename, mode='w') as f:
            print(content, file=f)

def warn(message):
    """Show a warning message to the user"""
    warnings.warn(message, category=RuntimeWarning, stacklevel=2)

def get_infobox(page):
    """Parse out the first Infobox for the page as a dict."""
    templates = mwparserfromhell.parse(page.data["wikitext"]).filter_templates()
    infobox = {}
    for template in templates:
        if template.name.strip_code().startswith('Infobox'):
            infobox = {
                str(p.name).strip(): p.value.strip_code().strip()
                for p in template.params if p.value.strip_code().strip()
            }
    return infobox

@lru_cache(maxsize=None)
def fetch_wikipedia(qid, lang, normalized):
    """Look up the Wikipedia page for the given QID and language"""
    print(
        'fetching "{}" Infobox/Wikidata for entity: {} ({}) ...'.format(
            lang,
            qid,
            normalized
        ),
        file=sys.stderr
    )
    try:
        page = wptools.page(wikibase=qid, lang=lang, silent=True).get()
        return {
            'infobox': get_infobox(page),
            'wikidata': page.data["wikidata"],
            'title': page.data["title"],
            'url': 'https://{}.wikipedia.org/wiki/{}'.format(lang, page.data["title"])
        }
    except LookupError:
        print(
            'No page exists for {} on {}.wikipedia.org'.format(qid, lang),
            file=sys.stderr
        )
    # If the lookup fails, just return an empty dict
    return {}

def augment(results, wikipedia_language, verbose):
    """Augment the entities with Wikipedia Infobox/Wikidata for the given
    language for each entity that was resolved to Wikidata with a QID.
    
    That is, for each entity extracted by Rosette API, if the entity's 
    'entityId' attribute is of the form r'^Q\d+', then a new 'wikipedia' 
    extended attribute will be added to the entity.
    
    E.g.,:
    
    results = request(
        'https://en.wikipedia.org/wiki/Count_von_Count',
        'entities',
        API(user_key=<key>, service_url=<api_url>),
        uri=True
    )
    augment(results, 'eng', False)
    results['entities'][13] -> {
        'count': 2,
        'entityId': 'Q12345',
        'mention': 'Count von Count',
        'normalized': 'Count von Count',
        'type': 'PERSON',
        'wikipedia': {
            'infobox': {
                'alias': 'The CountCount',
                'first': 'November 27, 1972',
                'gender': 'Male',
                'image': '200px',
                'name': 'Count von Count',
                'portrayer': 'Jerry Nelson (1972–2012)Matt Vogel (2013–present)',
                'series': 'Sesame Street',
                'species': 'Muppet vampire'
            },
            'title': 'Count_von_Count',
            'url': 'https://en.wikipedia.org/wiki/Count_von_Count',
            'wikidata': {
                'IMDB': 'ch0000709',
                'instance': ['fictional character', 'vampire']
            }
        }
    }
    """
    if verbose:
        entities = results['attributes']['entities']['items']
    else:
        entities = results['entities']
    if not any(e['entityId'].startswith('Q') for e in entities):
        warn('Document has no entities resolved to Wikidata!')
    # Get the ISO 639-1 two-letter language code used by Wikipedia
    # (Rosette API uses ISO 639-2/T three-letter language codes so we map them 
    # to ISO 639-1.)
    lang = Iso639()[wikipedia_language]['639-1']
    # Loop over entities that were resolved to a Wikidata QID and
    # augment them with Wikidata and Infobox information where available
    for entity in entities:
        id_ = entity['entityId']
        if id_.startswith('Q'):
            normalized = entity.get('normalized')
            entity['wikipedia'] = fetch_wikipedia(id_, lang, normalized)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=__doc__
    )
    parser.add_argument(
        '-i', '--input',
        help=(
            'Path to a file containing input data (if not specified data is '
            'read from stdin)'
        ),
        default=None
    )
    parser.add_argument(
        '-u',
        '--content-uri',
        action='store_true',
        help='Specify that the input is a URI (otherwise load text from file)'
    )
    parser.add_argument(
        '-k', '--key',
        help='Rosette API Key',
        default=None
    )
    parser.add_argument(
        '-a', '--api-url',
        help='Alternative Rosette API URL',
        default=DEFAULT_ROSETTE_API_URL
    )
    parser.add_argument(
        '-l', '--language',
        help=(
            'A three-letter (ISO 639-2 T) code that will override automatic '
            'language detection'
        ),
        default=None
    )
    parser.add_argument(
        '-w', '--wikipedia-language',
        required=True,
        help=(
            'A three-letter (ISO 639-2 T) code that determines which Wikipedia '
            'language to use for looking up Infobox information if available'
        )
    )
    parser.add_argument(
        '-v', '--verbose', '--adm',
        action='store_true',
        help=(
            'Output verbosely (i.e., get the full Annotated Data Model (ADM) '
            'as JSON)'
        )
    )
    args = parser.parse_args()
    # Get the user's Rosette API key
    key = (
        os.environ.get('ROSETTE_USER_KEY') or
        args.key or
        getpass(prompt='Enter your Rosette API key: ')
    )
    # Instantiate the Rosette API
    api = API(user_key=key, service_url=args.api_url)
    if args.verbose:
        api.setUrlParameter('output', 'rosette')
    content = get_content(args.input, args.content_uri)
    print('Extracting entities via Rosette API ...', file=sys.stderr)
    adm = request(
        content,
        'entities',
        api,
        language=args.language,
        uri=args.content_uri
    )
    print('Done!', file=sys.stderr)
    print('Augmenting entities via MediaWiki API ...', file=sys.stderr)
    augment(adm, args.wikipedia_language, args.verbose)
    print('Done!', file=sys.stderr)
    dump(adm)
