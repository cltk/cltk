The Classical Language Toolkit
==============================

About 
-----
The Ancient Greek and Latin languages have not benefited from comprehensive scientific study. The goals of the Classical Language Toolkit (CLTK) are to:

*   Compile analysis-friendly corpora
*   Gather and improve linguistic data required for natural language processing
*   Develop a free, open, stable, and modern platform for generating reproducible research

This project currently consists of a compiler for the corpora of the PHI5, PHI7, and TLG_E disks. The compiler outputs into plaintext JSON files. The TLG's Beta Code is translated into Unicode. Much more functionality will be built into this project as it grows.

INSTALLATION
------------
[CLTK sources are available from PyPI](https://pypi.python.org/pypi/cltk) and installable with pip.

```bash
pip install cltk
```

USE
---
The CLTK is developed in Python 3.3.

To convert corpora into single JSON files, use the following in your example.

```python
from cltk.compiler import Compile

c - Compile()
c.dump_txts_phi7()
c.dump_txts_phi5()
c.dump_txts_tlg()
```

The above code looks for the original corpora in a script's current directory and outputs there, too. The <code>Compile()</code> class takes two optional parameters, being corpora directory and target directory for the JSON output. E.g,:

```python
from cltk.compiler import Compile

c = Compile('/home/kyle/Documents/corpora', '/home/kyle/project_dir')
```

Note that the disks need to be labelled as follow: PHI5, PHI7, and TLG_E.

FUTURE RELEASES
---------------
The Beta Code to Unicode translation needs improvement. This and reading of Beta Code strings within the PHI disks will come in v. 0.0.0.4.

LICENSE
-------
The MIT License (MIT)

Copyright (c) 2014 Kyle P. Johnson
