SyntaxNet for CLTK
******************

Installation
============

Installation of SyntaxNet requires building from source. Currently,Tensorflow and SyntaxNet does not have support for Windows.For that, You will need to install:

* Python version 2.7
* pip(Python Package manager)
  * For Ubuntu, Obtain it using ``apt-get install python-pip``
* bazel:
 * Follow steps `here <https://bazel.build/versions/master/docs/install.html>`_ to install bazel.
* swig:
  * For Ubuntu, use ``apt-get install swig``.
* Install protocol buffers using command ``pip install -U protobuf==3.0.0b2``.
* Install NumPy using ``pip install numpy``.
* Install asciitree using ``pip install asciitree``.
* Install mock using ``pip install mock``.

Once the above steps are finished, you can now start building SyntaxNet on your machine using the following steps:

.. code-block::

   git clone --recursive https://github.com/tensorflow/models.git
  cd models/syntaxnet/tensorflow
  ./configure
  cd ..
  bazel test syntaxnet/... util/utf8/...
  # On Mac, run the following:
  bazel test --linkopt=-headerpad_max_install_names \
    syntaxnet/... util/utf8/...
    
Bazel should report all tests as passing. If all tests pass, You have successfully built SyntaxNet from source.

Once finished, you can download a collection of pretrained models for your target language. 
The language models are available here-``http://download.tensorflow.org/models/parsey_universal/<language>.zip`` 
where ``<language> is the language you wish to work on, Example- For Ancient Greek, you can download pretained models from 
``http://download.tensorflow.org/models/parsey_universal/Ancient_Greek.zip

Once you complete downloading the models and unzipping the models, you can run the models as:

.. code-block::

   MODEL_DIRECTORY=/where/you/unzipped/the/model/files
  cat sentences.txt | syntaxnet/models/parsey_universal/parse.sh \
    $MODEL_DIRECTORY > output.conll

The models are trained on Universal Dependencies datasets v1.3.
