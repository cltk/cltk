Contributing code
=================

**Note: This document is just for getting started. Visit [**the wiki**](htt
ps://github.com/cltk/cltk/wiki)
for the full contributor's guide. Please be sure to read it carefully to make
the code review process go as smoothly as possible and maximize the
likelihood of your contribution being merged.**

How to contribute
-----------------

The preferred way to contribute to cltk is to fork the 
[main repository](http://github.com/cltk/cltk/) on
GitHub. To get started, you will need a working installation
of [Python 3.5](https://www.python.org/downloads/):

1. Fork the [project repository](http://github.com/cltk/cltk):
   click on the 'Fork' button near the top of the page. This creates
   a copy of the code under your account on Github.

2. Clone this copy to your local disk:

        $ git clone git://github.com/cltk/cltk.git
        $ cd cltk

3. Create a virtualenv and activate it:

   	$ pyvenv venv
	$ source venv/bin/activate

4. Install cltk from source:

   	$ python setup.py install
	
   If you have modified the cltk source you will have to rebuild the project
   with the same command.

5. Install cltk development dependencies:

   	$ pip install -r dev-requirements.txt
	
6. Run the test suite to ensure proper installation by running `nosetests -v`
   in the root directory. To install nose, run `pip install nose`.

7. If all tests pass, create a branch to hold your changes:

        $ git checkout -b my-feature

   and start making changes. Never work in the ``master`` branch!

8. Work on this copy on your computer using Git to do the version
   control. When you're done editing, do:

        $ git add modified_files
        $ git commit

   to record your changes in Git, then push them to GitHub with:

        $ git push -u origin my-feature

Finally, go to the web page of your fork of the cltk repo,
and click 'Pull request' to send your changes to the maintainers for
review.

(If any of the git above seems like magic to you, then look up the 
[Git documentation](http://git-scm.com/documentation) on the web.)
