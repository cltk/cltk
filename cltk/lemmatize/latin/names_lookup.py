from collections import ChainMap

PRAENOMINA = {'c.': 'gaius',
              'l.': 'lucius',
              'm.': 'marcus',
              'p.': 'publius',
              'q.': 'quintus',
              't.': 'titus',
              'ti.': 'tiberius',
              'sex.': 'sextus',
              'a.': 'aulus',
              'd.': 'decimus',
              'cn.': 'gnaeus',
              'sp.': 'spurius',
              'm\'.': 'manius',
              'ser.': 'servius',
              'ap.': 'appius',
              'n.': 'numerius',
              'v.': 'vibius',
              'k.': 'caeso',
              'mam.': ' mamercus',
              'post.': ' postumus',
              'f.': 'faustus',
              'oct.': ' octavus',
              'opet.': ' opiter',
              'paul.': ' paullus',
              'pro.': ' proculus',
              'sert.': ' sertor',
              'st.': 'statius',
              'sta.': ' statius',
              'v.': 'vibius',
              'vol.': ' volesus',
              'vop.': ' vopiscus'
              }

names = dict(ChainMap(PRAENOMINA))

