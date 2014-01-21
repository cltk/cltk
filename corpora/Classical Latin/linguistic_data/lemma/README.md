About the lemmatizer
====================

Original data taken from a dictionary-like morphological list from Perseus source, eg,

> amicitia, amicitiae, amicitiam, amicitiarum, ...

which has been reversed into a two-column list used to replace inflected forms, eg,

> amicitiae, amicitia<br>
> amicitiam, amicitia<br>
> amicitiarum, amicitia<br>

This replacement list does not use j or v, so I created the "j\_and\_v_converter" to standardize any text which contains these characters. Thus "jam virtus" becomes "iam virtus".

Two examples, "test\_operations/test\_2\_jv_replacing.py" and "test\_operations/test\_2\_lemmatizing.py", illustrate these replacers in action.

Perseus data licensed under the Mozilla Public License 1.1 (MPL 1.1) (<http://www.mozilla.org/MPL/1.1/>). See LICENSE.md for this.
