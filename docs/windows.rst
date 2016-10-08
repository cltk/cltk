Installation Guide : Setting up CLTK in WSL, Experimental Support for Bash On Ubuntu On Windows
===============================================================================================

**Step 0:** `Setting up WSL on Windows 10`_

Installing required packages from ``apt-get``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    sudo apt update
    sudo apt install git
    sudo apt-get install python-setuptools 
    sudo apt install python-virtualenv

There are two ways to install CLTK using pip 

1. Installing Globally
~~~~~~~~~~~~~~~~~~~~~~
::

    [sudo] pip3 install cltk

2. Installing in a virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Creating environment

   .. code:: bash

       virtualenv -p python3 venv

-  Activating environment and installing CLTK

   .. code:: bash

       source venv/bin/activate
       pip3 install cltk

-  Deactivating environment

   .. code:: bash

       deactivate

**NOTE 1:** There are rendering issues with Unicode text in the Bash
Terminal. Fonts like ``SimSub-ExtB`` and ``Courier New`` render majority
of the `Unicode text`_ fine. Lot’s of other fonts such as ``Consolas``
and ``Lucida Console`` don’t. Try experimenting with different fonts in
the setting, see what works best for you. A better way, for now, would
be to use `ConEmu Windows Terminal`_ which rendered Unicode text much
better. 

|

**NOTE 2:** Support for Windows is currently experimental, since
the platform is still young. Also, contributing to CLTK on Windows would
bring unnecessary technical overhead, that’s why development on Windows
is strictly discouraged for the time being.

.. _Setting up WSL on Windows 10: http://www.howtogeek.com/249966/how-to-install-and-use-the-linux-bash-shell-on-windows-10/
.. _Unicode text: https://www.cl.cam.ac.uk/%7Emgk25/ucs/examples/UTF-8-demo.txt
.. _ConEmu Windows Terminal: https://conemu.github.io/
