"""`latin_library_corpus_types` - a mapping of corpus types into common periods, based largely on:
https://en.wikipedia.org/wiki/Latin_literature
and some personal choices, e.g.: the inscrutable Twelve Tables is placed in an 'early' latin
classification, while Plautus and Terence are in the Old latin section, some uncertain items are
binned into 'misc'. Pull requests to further sort this out are welcome!
"""

texts_to_remove_from_fileids = [
    'index.txt',
    'indices.txt'
]

# ontology map directories

corpus_directories_by_type = {
    'republican': [
        './caesar',
        './lucretius',
        './nepos',
        './cicero'
    ],
    'augustan': [
        './livy',
        './ovid',
        './horace',
        './vergil',
        './hyginus'
    ],
    'early_silver': [
        './martial',
        './juvenal',
        './tacitus',
        './lucan',
        './quintilian',
        './sen',
        './statius',
        './silius',
        './columella'
    ],
    'late_silver': [
        './suetonius',
        './gellius',
        './apuleius',
        './justin',
        './apicius',
        './fulgentius',
        './orosius'
    ],
    'old': [
        './plautus'
    ],
    'christian': [
        './ambrose',
        './abelard',
        './alcuin',
        './augustine',
        './bede',
        './bible',
        './cassiodorus',
        './commodianus',
        './gregorytours',
        './hugo',
        './isidore',
        './jerome',
        './prudentius',
        './tertullian',
        './kempis',
        './leothegreat'
    ],
    'medieval': [
        './boethiusdacia',
        './dante'
    ],
    'renaissance': [
    ],
    'neo_latin': [
        './addison',
        './bacon',
        './bultelius',
        './descartes',
        './erasmus',
        './galileo',
        './kepler',
        './may',
        './melanchthon',
        './xylander',
        './campion'
    ],
    #: uncategorized
    'misc':
        ['./alanus',
         './albertanus',
         './albertofaix',
         './aquinas',
         './ammianus',
         './arnobius',
         './capellanus',
         './cato',
         './claudian',
         './curtius',
         './eutropius',
         './frontinus',
         './gestafrancorum',
         './justinian',
         './lactantius',
         './martinbraga',
         './mirandola',
         './ottofreising',
         './pauldeacon',
         './sha',
         './theodosius',
         './voragine',
         './walter',
         './williamtyre'
         ],
    'early': []
}

#### by text


corpus_texts_by_type = {
    'republican': [
        'sall.1.txt',
        'sall.2.txt',
        'sall.cotta.txt',
        'sall.ep1.txt',
        'sall.ep2.txt',
        'sall.frag.txt',
        'sall.invectiva.txt',
        'sall.lep.txt',
        'sall.macer.txt',
        'sall.mithr.txt',
        'sall.phil.txt',
        'sall.pomp.txt',
        'varro.frag.txt',
        'varro.ll10.txt',
        'varro.ll5.txt',
        'varro.ll6.txt',
        'varro.ll7.txt',
        'varro.ll8.txt',
        'varro.ll9.txt',
        'varro.rr1.txt',
        'varro.rr2.txt',
        'varro.rr3.txt',
        'sulpicia.txt'
    ],
    'augustan': [
        'resgestae.txt',
        'resgestae1.txt',
        'manilius1.txt',
        'manilius2.txt',
        'manilius3.txt',
        'manilius4.txt',
        'manilius5.txt',
        'catullus.txt',
        'vitruvius1.txt',
        'vitruvius10.txt',
        'vitruvius2.txt',
        'vitruvius3.txt',
        'vitruvius4.txt',
        'vitruvius5.txt',
        'vitruvius6.txt',
        'vitruvius7.txt',
        'vitruvius8.txt',
        'vitruvius9.txt',
        'propertius1.txt',
        'tibullus1.txt',
        'tibullus2.txt',
        'tibullus3.txt'
    ],
    'early_silver': [
        'pliny.ep1.txt',
        'pliny.ep10.txt',
        'pliny.ep2.txt',
        'pliny.ep3.txt',
        'pliny.ep4.txt',
        'pliny.ep5.txt',
        'pliny.ep6.txt',
        'pliny.ep7.txt',
        'pliny.ep8.txt',
        'pliny.ep9.txt',
        'pliny.nh1.txt',
        'pliny.nh2.txt',
        'pliny.nh3.txt',
        'pliny.nh4.txt',
        'pliny.nh5.txt',
        'pliny.nhpr.txt',
        'pliny.panegyricus.txt',
        'petronius1.txt',
        'petroniusfrag.txt',
        'persius.txt',
        'phaedr1.txt',
        'phaedr2.txt',
        'phaedr3.txt',
        'phaedr4.txt',
        'phaedr5.txt',
        'phaedrapp.txt',
        'seneca.contr1.txt',
        'seneca.contr10.txt',
        'seneca.contr2.txt',
        'seneca.contr3.txt',
        'seneca.contr4.txt',
        'seneca.contr5.txt',
        'seneca.contr6.txt',
        'seneca.contr7.txt',
        'seneca.contr8.txt',
        'seneca.contr9.txt',
        'seneca.fragmenta.txt',
        'seneca.suasoriae.txt',
        'valeriusflaccus1.txt',
        'valeriusflaccus2.txt',
        'valeriusflaccus3.txt',
        'valeriusflaccus4.txt',
        'valeriusflaccus5.txt',
        'valeriusflaccus6.txt',
        'valeriusflaccus7.txt',
        'valeriusflaccus8.txt',
        'valmax1.txt',
        'valmax2.txt',
        'valmax3.txt',
        'valmax4.txt',
        'valmax5.txt',
        'valmax6.txt',
        'valmax7.txt',
        'valmax8.txt',
        'valmax9.txt',
        'vell1.txt',
        'vell2.txt'
    ],
    'late_silver': [
    ],
    'old': [
        'ter.adel.txt',
        'ter.andria.txt',
        'ter.eunuchus.txt',
        'ter.heauton.txt',
        'ter.hecyra.txt',
        'ter.phormio.txt',
        'andronicus.txt',
        'enn.txt'
    ],
    'early': [
        '12tables.txt'
    ],
    'medieval': [
        'anselmepistula.txt',
        'anselmproslogion.txt',
        'carm.bur.txt'
    ],
    'christian': [
        'anon.martyrio.txt',
        'benedict.txt',
        'berengar.txt',
        'bernardclairvaux.txt',
        'bernardcluny.txt',
        'bonaventura.itinerarium.txt',
        'creeds.txt',
        'decretum.txt',
        'diesirae.txt',
        'egeria.txt',
        'ennodius.txt',
        'eucherius.txt',
        'eugippius.txt',
        'greg.txt',
        'gregory.txt',
        'gregory7.txt',
        'hydatius.txt',
        'hymni.txt',
        'innocent.txt',
        'hydatius.txt',
        'junillus.txt',
        'lactantius.txt',
        'liberpontificalis.txt',
        'macarius.txt',
        'macarius1.txt',
        'novatian.txt',
        'papal.txt',
        'paulinus.poemata.txt',
        'perp.txt',
        'professio.txt',
        'prosperus.txt',
        'regula.txt',
        'sedulius.txt',
        'sulpiciusseverus.txt',
        'vorag.txt'
    ],
    'renaissance': [
        'petrarch.ep1.txt',
        'petrarch.numa.txt',
        'petrarch.rom.txt'
    ],
    'neo_latin': [
        'spinoza.ethica1.txt',
        'spinoza.ethica2.txt',
        'spinoza.ethica3.txt',
        'spinoza.ethica4.txt',
        'spinoza.ethica5.txt'
    ],
    'misc': []
}
