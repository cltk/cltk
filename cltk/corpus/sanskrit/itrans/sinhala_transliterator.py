__author__ = ["Nurendra Choudhary <nurendrachoudhary31@gmail.com>", "Anoop Kunchukuttan <anoop.kunchukuttan@gmail.com>"]
__license__ = "GPLv3"

class SinhalaDevanagariTransliterator(object): 
    """
        A Devanagari to Sinhala transliterator based on explicit Unicode Mapping
    """

    sinhala_devnag_map={
                u'\u0d82':u'\u0902', 
                u'\u0d83':u'\u0903',
                u'\u0d84':u'\u0904',
                u'\u0d85':u'\u0905',
                u'\u0d86':u'\u0906',
                u'\u0d87':u'\u090d',
                u'\u0d88':u'\u090d',
                u'\u0d89':u'\u0907',
                u'\u0d8a':u'\u0908',
                u'\u0d8b':u'\u0909',
                u'\u0d8c':u'\u090a',
                u'\u0d8d':u'\u090b',
                u'\u0d8f':u'\u090c',
                u'\u0d91':u'\u090e',
                u'\u0d92':u'\u090f',
                u'\u0d93':u'\u0910',
                u'\u0d94':u'\u0912',
                u'\u0d95':u'\u0913',
                u'\u0d96':u'\u0914',
                u'\u0d9a':u'\u0915',
                u'\u0d9b':u'\u0916',
                u'\u0d9c':u'\u0917',
                u'\u0d9d':u'\u0918',
                u'\u0d9e':u'\u0919',
                u'\u0d9f':u'\u0919',
                u'\u0da0':u'\u091a',
                u'\u0da1':u'\u091b',
                u'\u0da2':u'\u091c',
                u'\u0da3':u'\u091d',
                u'\u0da4':u'\u091e',
                u'\u0da5':u'\u091e',
                u'\u0da6':u'\u091e',
                u'\u0da7':u'\u091f',
                u'\u0da8':u'\u0920',
                u'\u0da9':u'\u0921',
                u'\u0daa':u'\u0922',
                u'\u0dab':u'\u0923',
                u'\u0dac':u'\u0923',
                u'\u0dad':u'\u0924',
                u'\u0dae':u'\u0925',
                u'\u0daf':u'\u0926',
                u'\u0db0':u'\u0927',
                u'\u0db1':u'\u0928',
                u'\u0db2':u'\u0928',
                u'\u0db3':u'\u0928',
                u'\u0db4':u'\u092a',
                u'\u0db5':u'\u092b',
                u'\u0db6':u'\u092c',
                u'\u0db7':u'\u092d',
                u'\u0db8':u'\u092e',
                u'\u0dba':u'\u092f',
                u'\u0dbb':u'\u0930',
                u'\u0dbd':u'\u0932',
                u'\u0dc5':u'\u0933',
                u'\u0dc0':u'\u0935',
                u'\u0dc1':u'\u0936',
                u'\u0dc2':u'\u0937',
                u'\u0dc3':u'\u0938',
                u'\u0dc4':u'\u0939',
                u'\u0dcf':u'\u093e',
                u'\u0dd0':u'\u0949',
                u'\u0dd1':u'\u0949',
                u'\u0dd2':u'\u093f',
                u'\u0dd3':u'\u0940',
                u'\u0dd4':u'\u0941',
                u'\u0dd6':u'\u0942',
                u'\u0dd8':u'\u0943',
                u'\u0dd9':u'\u0946',
                u'\u0dda':u'\u0947',
                u'\u0ddb':u'\u0948',
                u'\u0ddc':u'\u094a',
                u'\u0ddd':u'\u094b',
                u'\u0dde':u'\u094c',
                u'\u0dca':u'\u094d',
            }

    devnag_sinhala_map={
            u'\u0900':u'\u0d82', 
            u'\u0901':u'\u0d82',
            u'\u0902':u'\u0d82',
            u'\u0903':u'\u0d83',
            u'\u0904':u'\u0d84',
            u'\u0905':u'\u0d85',
            u'\u0906':u'\u0d86',
            u'\u0907':u'\u0d89',
            u'\u0908':u'\u0d8a',
            u'\u0909':u'\u0d8b',
            u'\u090a':u'\u0d8c',
            u'\u090b':u'\u0d8d',
            u'\u090c':u'\u0d8f',
            u'\u090d':u'\u0d88',
            u'\u090e':u'\u0d91',
            u'\u090f':u'\u0d92',
            u'\u0910':u'\u0d93',
            u'\u0912':u'\u0d94',
            u'\u0913':u'\u0d95',
            u'\u0914':u'\u0d96',
            u'\u0915':u'\u0d9a',
            u'\u0916':u'\u0d9b',
            u'\u0917':u'\u0d9c',
            u'\u0918':u'\u0d9d',
            u'\u0919':u'\u0d9e',
            u'\u091a':u'\u0da0',
            u'\u091b':u'\u0da1',
            u'\u091c':u'\u0da2',
            u'\u091d':u'\u0da3',
            u'\u091e':u'\u0da4',
            u'\u091f':u'\u0da7',
            u'\u0920':u'\u0da8',
            u'\u0921':u'\u0da9',
            u'\u0922':u'\u0daa',
            u'\u0923':u'\u0dab',
            u'\u0924':u'\u0dad',
            u'\u0925':u'\u0dae',
            u'\u0926':u'\u0daf',
            u'\u0927':u'\u0db0',
            u'\u0928':u'\u0db1',
            u'\u0929':u'\u0db1',
            u'\u092a':u'\u0db4',
            u'\u092b':u'\u0db5',
            u'\u092c':u'\u0db6',
            u'\u092d':u'\u0db7',
            u'\u092e':u'\u0db8',
            u'\u092f':u'\u0dba',
            u'\u0930':u'\u0dbb',
            u'\u0932':u'\u0dbd',
            u'\u0933':u'\u0dc5',
            u'\u0935':u'\u0dc0',
            u'\u0936':u'\u0dc1',
            u'\u0937':u'\u0dc2',
            u'\u0938':u'\u0dc3',
            u'\u0939':u'\u0dc4',
            u'\u093e':u'\u0dcf',
            u'\u0949':u'\u0dd1',
            u'\u093f':u'\u0dd2',
            u'\u0940':u'\u0dd3',
            u'\u0941':u'\u0dd4',
            u'\u0942':u'\u0dd6',
            u'\u0943':u'\u0dd8',
            u'\u0946':u'\u0dd9',
            u'\u0947':u'\u0dda',
            u'\u0948':u'\u0ddb',
            u'\u094a':u'\u0ddc',
            u'\u094b':u'\u0ddd',
            u'\u094c':u'\u0dde',
            u'\u094d':u'\u0dca',
            
        }

    @staticmethod
    def devanagari_to_sinhala(text):
        return u''.join([ SinhalaDevanagariTransliterator.devnag_sinhala_map.get(c,c) for c in text ])

    @staticmethod
    def sinhala_to_devanagari(text):
        return u''.join([ SinhalaDevanagariTransliterator.sinhala_devnag_map.get(c,c) for c in text ])

