"""Arabic corpora available for download."""

__author__ = 'Lakhdar Benzahia <lakhdar[.]benzahia[at]gmail[.]com>'

ARABIC_CORPORA = [
    {'name': 'arabic_text_perseus',
     'markup':'xml',
     'origin': 'https://github.com/cltk/arabic_text_perseus',
     'location': 'remote',
     'type': 'text',
     'RomanizationType': 'Buckwalter',
     },
     {'name': 'quranic-corpus',
      'markup':'xml',
      'origin': 'https://github.com/cltk/arabic_text_quranic_corpus',
      'location': 'remote',
      'type': 'text',
      'RomanizationType': 'none',
      },
      {'name': 'quranic-corpus-morphology',
       'origin': 'https://github.com/cltk/arabic_morphology_quranic-corpus',
       'location': 'remote',
       'type': 'text',
       'RomanizationType': 'Buckwalter',
       'script': 'Uthmani',
       },
]
