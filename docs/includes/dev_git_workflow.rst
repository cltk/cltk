* ``$ git clone https://github.com/your-username/cltk.git)``
* ``$ cd cltk``
* ``$ git remote add upstream https://github.com/cltk/cltk.git``
* ``$ git branch fix-feature``
* ``$ git checkout fix-feature``
* Install: ``$ make install``
* Check changes in interactive Python shell: ``$ make shell``
* Run doctests locally: ``$ make testOnlyDocTests``
* ``$ make docs``. Check that the docs look good for any modules you changed: ``docs/_build/html/index.html``.
* ``$ git push origin fix-feature``
* Open pull request: `<https://github.com/your-username/cltk/pull/new/master>`_
* Wait for Travis CI to report build success for your PR: `<https://travis-ci.org/github/cltk/cltk/pull_requests>`_. Confirm code coverage and docs build OK, too.
* A maintainer will review your code and either request changes or accept.
* Once accepted, a maintainer will package a new version and publish it to PyPI (`Packaging`_).
* After the PR is accepted and version incremented, update your local repo:
   - ``$ git checkout master``
   - ``$ git pull upstream master``
   - ``$ git push origin master``
