"""Script for provisioning build server.

Use: `$ python cltk/utils/build_server.py`
"""

import os

from stanfordnlp.utils.resources import download  # type: ignore

if __name__ == '__main__':

    ud_models_for_cltk = ['grc_perseus', 'grc_proiel',
                          'la_ittb', 'la_perseus', 'la_proiel',
                          'cu_proiel',  # Old Church Slavonic
                          'fro_srcmf',  # Old French
                          ]

    for model in ud_models_for_cltk:
        download(download_label=model,
                 resource_dir=os.path.expanduser('~/stanfordnlp_resources/'),
                 confirm_if_exists=True,
                 force=True)
