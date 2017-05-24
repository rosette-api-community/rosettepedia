# Rosettepedia

This repository includes Python code demonstrating how to combine [Rosette API](https://developer.rosette.com/) entity-extraction results with results from the [MediaWiki API](https://www.mediawiki.org/wiki/API:Main_page) to provide additional information about entities based on information available in Wikipedia Infoboxes and Wikidata.

## Setup

### Installing Dependencies with Virtualenv
The script is written for Python 3.  If you are alright with installing external Python packages globally, you may skip this section.

You can install the dependencies using `virtualenv` so that you don't alter your global site packages.

The process for installing the dependencies using `virtualenv` is as follows for `bash` or similar shells:

Ensure your `virtualenv` is up to date.

    $ pip install -U virtualenv

**Note**: You may need to use `pip3` depending on your Python installation.

`cd` into the repository directory (where this `README.md` file is located) and create a Python 3 virtual environment with:

    $ python3 $(which virtualenv) .

Activate the virtual environment:

    $ source bin/activate

Once you've activated the virtual environment you can proceed to install the requirements safely without affecting your globabl site packages.

### Installing the Dependencies
You can install the dependencies via `pip` (or `pip3` depending on your installation of Python 3) as follows using the provided `requirements.txt`:

    $ pip install -r requirements.txt

## Running `rosettepedia.py`
You can use the script from the commandline as follows:

    ./rosettepedia.py -h
    usage: rosettepedia.py [-h] [-i INPUT] [-u] [-k KEY] [-a API_URL]
                           [-l LANGUAGE] -w WIKIPEDIA_LANGUAGE [-s]

    Augment Rosette API entity extraction results with information from Wikipedia.

    optional arguments:
      -h, --help            show this help message and exit
      -i INPUT, --input INPUT
                            Path to a file containing input data (if not specified
                            data is read from stdin) (default: None)
      -u, --content-uri     Specify that the input is a URI (otherwise load text
                            from file) (default: False)
      -k KEY, --key KEY     Rosette API Key (default: None)
      -a API_URL, --api-url API_URL
                            Alternative Rosette API URL (default:
                            https://api.rosette.com/rest/v1/)
      -l LANGUAGE, --language LANGUAGE
                            A three-letter (ISO 639-2 T) code that will override
                            automatic language detection (default: None)
      -w WIKIPEDIA_LANGUAGE, --wikipedia-language WIKIPEDIA_LANGUAGE
                            A three-letter (ISO 639-2 T) code that determines
                            which Wikipedia language to use for looking up Infobox
                            information if available (default: None)
      -s, --simple-output   Get simplified results (instead of full ADM results)
                            (default: False)


**Note**: If you prefer not to enter your Rosette API key every time you run the script you can set up an environment variable `$ROSETTE_USER_KEY`.

### Examples
The simplest way to use the script is to simply pipe in a string:

    $ echo "OPEC will meet in Vienna this week." | ./rosettepedia.py -w eng > opec.json
    Extracting entities via Rosette API ...
    Done!
    Augmenting entities via MediaWiki API ...
    fetching "en" Infobox/Wikidata for entity: Q7795 (OPEC) ...
    fetching "en" Infobox/Wikidata for entity: Q1741 (Vienna) ...
    Done!


We can inspect the results with [`jq`](https://stedolan.github.io/jq/):

    $ jq .entities opec.json 
    [
      {
        "type": "ORGANIZATION",
        "mention": "OPEC",
        "normalized": "OPEC",
        "count": 1,
        "entityId": "Q7795",
        "wikipedia": {
          "infobox": {
            "name": "Organization of the Petroleum Exporting Countries",
            "image_flag": "Flag of OPEC.svg",
            "image_map": "OPEC.svg",
            "org_type": "International cartel",
            "membership_type": "Membership",
            "admin_center_type": "Headquarters",
            "admin_center": "Vienna, Austria",
            "languages_type": "Official language",
            "languages": "English",
            "leader_title1": "Secretary General",
            "leader_name1": "Mohammed Barkindo",
            "established": "Baghdad, Iraq",
            "established_event1": "Statute",
            "established_date1": "10–14 September 1960",
            "established_event2": "In effect",
            "established_date2": "January 1961",
            "currency": "(US$ /bbl)"
          },
          "wikidata": {
            "website": "http://www.opec.org",
            "image": "OPEC-building-01.jpg",
            "instance": "international organization",
            "category": "Category:OPEC"
          },
          "title": "OPEC",
          "url": "https://en.wikipedia.org/wiki/OPEC"
        }
      },
      {
        "type": "LOCATION",
        "mention": "Vienna",
        "normalized": "Vienna",
        "count": 1,
        "entityId": "Q1741",
        "wikipedia": {
          "infobox": {
            "name": "Vienna",
            "native_name": "Wien",
            "settlement_type": "Capital city",
            "image_flag": "Flag of Wien.svg",
            "image_seal": "Vienna seal 1926.svg",
            "image_shield": "Wien 3 Wappen.svg",
            "shield_size": "80px",
            "image_map": "Wien in Austria.svg",
            "map_caption": "Location of Vienna in Austria",
            "subdivision_type": "Country",
            "subdivision_name": "Austria",
            "leader_party": "SPÖ",
            "leader_title": "Mayor and Governor",
            "leader_name": "Michael Häupl",
            "leader_title1": "Vice-Mayors and Vice-Governors",
            "area_magnitude": "2 chaiz",
            "area_total_km2": "414.65",
            "area_land_km2": "395.26",
            "area_water_km2": "19.39",
            "elevation_m": "151 (Lobau) – 542 (Hermannskogel)",
            "elevation_ft": "495–1778",
            "population_total": "1,867,960",
            "population_as_of": "1. January 2017",
            "population_density_km2": "4326.1",
            "population_metro": "2,600,000",
            "population_blank2_title": "Ethnicity",
            "population_blank2": "61.2% Austrian38.8% Other",
            "population_demonym": "Viennese, Wiener",
            "population_note": "Statistik Austria, VCÖ – Mobilität mit Zukunft",
            "postal_code_type": "Postal code",
            "postal_code": "1010–1423, 1600, 1601, 1810, 1901",
            "website": "www.wien.gv.at",
            "footnotes": "frameless|x30px",
            "blank1_name": "- GDP total (2014)http://ec.europa.eu/eurostat/documents/2995521/7192292/1-26022016-AP-EN.pdf/602b34e8-abba-439e-b555-4c3cb1dbbe6e",
            "blank1_info": "€82 billion/ US$110 billion",
            "blank2_name": "- GDP per capita(2014)http://ec.europa.eu/eurostat/documents/2995521/7192292/1-26022016-AP-EN.pdf/602b34e8-abba-439e-b555-4c3cb1dbbe6e",
            "blank2_info": "€47,300/ US$63,000XE.com average GBP/ USD ex. rate in 2014",
            "timezone": "CET",
            "utc_offset": "+1",
            "timezone_DST": "CEST",
            "utc_offset_DST": "+2",
            "blank_name": "Vehicle registration",
            "blank_info": "W"
          },
          "wikidata": {
            "image": "Collage von Wien.jpg",
            "coordinates": {
              "latitude": 48.20833,
              "longitude": 16.373064,
              "altitude": null,
              "precision": 1e-06,
              "globe": "http://www.wikidata.org/entity/Q2"
            },
            "website": "https://www.wien.gv.at/",
            "instance": [
              "city",
              "capital",
              "city with millions of inhabitants",
              "federal capital",
              "municipality of Austria",
              "place with town rights and privileges",
              "statuatory city of Austria",
              "state of Austria",
              "district of Austria",
              "metropolis",
              "tourist destination"
            ],
            "country": [
              "Austria",
              "First Republic of Austria",
              "Austria-Hungary",
              "Republic of German-Austria",
              "Austrian Empire",
              "Federal State of Austria",
              "Nazi Germany",
              "Habsburg Empire",
              "Archduchy of Austria",
              "Duchy of Austria",
              "March of Austria",
              "Duchy of Bavaria",
              "Allied-occupied Austria"
            ],
            "category": "Category:Vienna"
          },
          "title": "Vienna",
          "url": "https://en.wikipedia.org/wiki/Vienna"
        }
      }
    ]

Another way to use the script is to have Rosette API extract content from a web page by supplying a URL and using the `-u/--content-uri` option:

    $ ./rosettepedia.py -u -i 'https://ja.wikipedia.org/wiki/アメリカスカップ' -w jpn > アメリカスカップ.json
    Extracting entities via Rosette API ...
    ...
    Done!
    $ jq '.entities[]|select(.entityId == "Q29")' アメリカスカップ.json
    {
      "type": "LOCATION",
      "mention": "Español",
      "normalized": "Español",
      "count": 1,
      "entityId": "Q29",
      "wikipedia": {
        "infobox": {},
        "wikidata": {
          "coordinates": {
            "latitude": 40,
            "longitude": -3,
            "altitude": null,
            "precision": 1,
            "globe": "http://www.wikidata.org/entity/Q2"
          },
          "image": "Relief Map of Spain.png",
          "continent": [
            "ヨーロッパ",
            "アフリカ"
          ],
          "instance": [
            "主権国家",
            "国",
            "欧州連合加盟国",
            "国際連合加盟国",
            "欧州評議会加盟国"
          ],
          "category": "Category:スペイン",
          "country": "スペイン"
        },
        "title": "スペイン",
        "url": "https://ja.wikipedia.org/wiki/スペイン"
      }
    }

Since Rosette API resolves entities independent of language, you can get Wikipedia Infobox/Wikidata information in a different language from the document using the `-w/--wikipedia-language` option.  For example you can get German Wikipedia info for the entities extracted from a Japanese document:

    $ ./rosettepedia.py -u -i 'https://ja.wikipedia.org/wiki/アメリカスカップ' -w deu > アメリカスカップ.deu.json
    Extracting entities via Rosette API ...
    ...
    Done!
    $ jq '.entities[]|select(.entityId == "Q29")' アメリカスカップ.deu.json
    {
      "type": "LOCATION",
      "mention": "Español",
      "normalized": "Español",
      "count": 1,
      "entityId": "Q29",
      "wikipedia": {
        "infobox": {
          "NAME-AMTSSPRACHE": "Reino de España",
          "NAME-DEUTSCH": "Königreich Spanien",
          "BILD-FLAGGE": "Flag of Spain.svg",
          "ARTIKEL-FLAGGE": "Flagge Spaniens",
          "BILD-WAPPEN": "Escudo de España (mazonado).svg",
          "BILD-WAPPEN-BREITE": "120px",
          "ARTIKEL-WAPPEN": "Wappen Spaniens",
          "WAHLSPRUCH": "„Plus Ultra“lat., „Darüber hinaus“",
          "AMTSSPRACHE": "Spanisch\namtlich regional:\n Aragonesisch\n Aranesisch\n Asturisch\n Baskisch\n Galicisch\n Katalanisch",
          "HAUPTSTADT": "Madrid",
          "STAATSFORM": "parlamentarische Erbmonarchie",
          "REGIERUNGSSYSTEM": "parlamentarische Demokratie",
          "STAATSOBERHAUPT": "König Felipe VI.",
          "REGIERUNGSCHEF": "Regierungspräsident Mariano Rajoy",
          "FLÄCHE": "505.970Europäische Union (Eurostat): Spanien – Länderinfo, Stand 2014.",
          "EINWOHNER": "46.438.422 (1. Januar 2016)",
          "BEV-DICHTE": "92",
          "BEV-ZUNAHME": "–0,02% (2015–2016)",
          "BIP": "2011World Economic Outlook Database, April 2012 des Internationalen Währungsfonds\n $ 1.493 Milliarden (12.)\n $ 1.413 Milliarden (13.)\n $ 32.360 (27.)\n $ 30.626 (29.)",
          "BIP-ERWEITERT": "* Total (nominal)\n Total (KKP)\n BIP/Einw. (nominal)\n BIP/Einw. (KKP)",
          "HDI": "0,869 (27.) (2013)Human Development Report Office: Spain – Country Profile: Human Development Indicators, abgerufen am 26. Oktober 2014",
          "WÄHRUNG": "Euro (EUR)",
          "NATIONALHYMNE": "Marcha Real155x125px",
          "ZEITZONE": "UTC+1 MEZUTC+2 MESZ (März bis Oktober)Kanarische Inseln:UTC±0UTC+1 (März bis Oktober)",
          "KFZ-KENNZEICHEN": "E",
          "ISO 3166": "ES, ESP, 724",
          "INTERNET-TLD": ".es",
          "TELEFON-VORWAHL": "+34",
          "BILD-LAGE": "Spain in the European Union on the globe (Europe centered).svg",
          "BILD-LAGE-IMAGEMAP": "EuropaGlobus1"
        },
        "wikidata": {
          "coordinates": {
            "latitude": 40,
            "longitude": -3,
            "altitude": null,
            "precision": 1,
            "globe": "http://www.wikidata.org/entity/Q2"
          },
          "image": "Relief Map of Spain.png",
          "continent": [
            "Europa",
            "Afrika"
          ],
          "instance": [
            "souveräner Staat",
            "Land",
            "Mitgliedstaat der Europäischen Union",
            "Mitgliedstaat der Vereinten Nationen",
            "Mitglied des Europarats"
          ],
          "category": "Kategorie:Spanien",
          "country": "Spanien"
        },
        "title": "Spanien",
        "url": "https://de.wikipedia.org/wiki/Spanien"
      }
    }

Given the additional information provided by the `wikipedia` extended attributes, you can filter down to only those entities that satisfy certain properties.  For instance, you can query for only those entities that have geo-coordinates:

    $ jq '.entities[]|select(.wikipedia.wikidata|has("coordinates"))' アメリカスカップ.json
    ...
    {
      "type": "LOCATION",
      "mention": "JPN",
      "normalized": "JPN",
      "count": 1,
      "entityId": "Q17",
      "wikipedia": {
        "infobox": {},
        "wikidata": {
          "coordinates": {
            "latitude": 35,
            "longitude": 136,
            "altitude": null,
            "precision": 1,
            "globe": "http://www.wikidata.org/entity/Q2"
          },
          "instance": [
            "主権国家",
            "国",
            "島国",
            "国際連合加盟国"
          ],
          "continent": "アジア",
          "category": "Category:日本",
          "country": "日本"
        },
        "title": "日本",
        "url": "https://ja.wikipedia.org/wiki/日本"
      }
    }

Or find those entities that have a linked website:

    $ jq '.entities[]|select(.wikipedia.wikidata|has("website"))' アメリカスカップ.json
    ...
    {
      "type": "ORGANIZATION",
      "mention": "国際ルール",
      "normalized": "国際ルール",
      "count": 1,
      "entityId": "Q46199",
      "wikipedia": {
        "infobox": {
          "名称": "国際バスケットボール連盟",
          "略称": "FIBA",
          "設立": "1932年",
          "本部": "・ジュネーヴ",
          "会長": "ホラシオ・ムラトーレ",
          "事務総長": "パトリック・バウマン",
          "ウェブサイト": "http://www.fiba.com/"
        },
        "wikidata": {
          "website": "http://www.fiba.com/",
          "image": "FIBA headquarter.JPG",
          "category": null,
          "instance": "国際競技連盟"
        },
        "title": "国際バスケットボール連盟",
        "url": "https://ja.wikipedia.org/wiki/国際バスケットボール連盟"
      }
    }
    