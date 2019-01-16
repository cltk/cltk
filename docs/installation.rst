Installation
************
Please note that the CLTK is built, tested, and supported only on POSIX-compliant OS (namely, Linux, Mac and the BSDs).

With Pip
========


.. note::

   The CLTK is only officially supported with Python 3.7 on POSIX–compliant operating systems (Linux, Mac OS X, FreeBSD, etc.).

First, you'll need a working installation of `Python 3.7 <https://www.python.org/downloads/>`_, which now includes Pip. Create a virtual environment and activate it as follows:

.. code-block:: shell

   $ python3.7 -m venv venv

   $ source venv/bin/activate

Then, install the CLTK, which automatically includes all dependencies.

.. code-block:: shell

   $ pip install cltk

Second, you will need an installation of `Git <http://git-scm.com/downloads>`_, which the CLTK uses to download and update corpora, if you want to automatically import any of the `CLTK's corpora <https://github.com/cltk/>`_. Installation of Git will depend on your operating system.


.. tip::

   For a user–friendly interactive shell environment, try IPython, which may be invoked with ``ipython`` from the command line. You may install it with ``pip install ipython``.


Microsoft Windows
-----------------

.. warning:: CLTK on Windows is not officially supported, however we do encourage Windows 10 users to give the following a try. Others have reported success. If this should fail for you, please open an issue on GitHub.

Windows 10 features a beta of "Bash on Ubuntu on Windows", which creates a fully functional POSIX environment. For an introduction, `see Microsoft's docs here <https://msdn.microsoft.com/en-us/commandline/wsl/about>`_.

Once you have enabled Bash on Windows, installation and use is just the same as on Ubuntu. For instance, you do use the following:

.. code:: bash

   sudo apt update
   sudo apt install git
   sudo apt-get install python-setuptools
   sudo apt install python-virtualenv
   virtualenv -p python3 ~/venv
   source ~/venv/bin/activate
   pip3 install cltk

.. tip::

   Some fonts do not render Unicode well in the Bash Terminal. Try ``SimSub-ExtB`` or ``Courier New``.


Older releases
--------------
For reproduction of scholarship, the CLTK archives past versions of its software releases. \
To get an older release by version, say ``v0.1.32``, use:

.. code-block:: shell

   $ pip install cltk==0.1.32

If you do not know a release's version number but have its DOI \
(for instance, if you want to install version ``10.5281/zenodo.51144``), then you can \
`search Zenodo <https://zenodo.org/search?ln=en&p=10.5281%2Fzenodo.51144&action_search=>`_ \
and learn that this DOI corresponds to version v0.1.34.

The above will work for most researchers seeking to reproduce \
results. It will give you CLTK code identical to what \
the original researcher was using. However, it is possible that you will want \
to use the exact same CLTK dependencies the researcher was using, too. In \
this case, consult the `CLTK GitHub Releases page <https://github.com/cltk/cltk/releases>`_ \
and download a `.tar.gz` file of the desired version. Then, you may do the following:

.. code-block:: shell

   $ tar zxvf cltk-0.1.34.tar.gz
   $ cd cltk-0.1.34
   $ python3.6 -m venv venv
   $ source venv/bin/activate
   $ pip install -r requirements.txt

This will give you CLTK and immediate dependencies identical to your target codebase.

The CLTK's repositories are versioned, too, using Git. Should there have been changes \
to a target corpus, you may acquire your needed version by manually cloning the entire repo, \
then checking out the past version by commit log. For example, if you need commit \
``0ed43e025df276e95768038eb3692ba155cc78c9`` from the repo ``latin_text_perseus``:

.. code-block:: shell

   $ cd ~/cltk_data/latin/text/
   $ rm -rf text/latin_text_perseus/
   $ git clone https://github.com/cltk/latin_text_perseus.git
   $ cd latin_text_perseus/
   $ git checkout 0ed43e025df276e95768038eb3692ba155cc78c9


From source
===========
The `CLTK source is available at GitHub <https://github.com/cltk/cltk>`_. To build from source, clone the repository, make a virtual environment (as above), and run:

.. code-block:: shell

   $ pip install -U -r requirements.txt 
   $ python setup.py install

If you have modified the CLTK source, rebuild the project with this same command. If you make any changes, it is a good idea to run the test suite to ensure you did not introduce any breakage. Test with ``nose``:

.. code-block:: shell

   $ nosetests --with-doctest
