About the Classical Language Toolkit
====================================
The Ancient Greek and Latin languages have not benefited from comprehensive scientific study. The goals of the Classical Language Toolkit (CLTK)are to:

*   Compile analysis-friendly corpora
*   Gather and improve linguistic data required for natural language processing
*   Develop a free, open, stable, and modern platform for generating reproducible results

This project currently consists of a compiler for the corpora of the PHI5, PHI7, and TLG_E disks. The compiler outputs in plaintext JSON files. Much more functionality will be built into this project as it grows.

INSTALLATION
============
These instructions work on Debian and are adaptable to any POSIX system.

USE
===
The CLTK is developed in Python 3.3. To convert corpora into a single JSON file, use the following in your example. 
```python
from cltk.compiler import Compile

#c = Compile()
c = Compile('/home/kyle/cltk', '/home/kyle/Documents/corpora')
c.uppercase\_files()
c.dump\_txts\_phi7()
c.dump\_txts\_phi5()
c.dump\_txts\_tlg()
```

LICENSE
=======
The MIT License (MIT)

Copyright (c) 2013 Kyle P. Johnson
