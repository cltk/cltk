This list of stop words has been moved over from the now-defunct [Latin\_and\_Ancient\_Greek\_for\_NLTK](https://github.com/kylepjohnson/Latin_and_Ancient_Greek_for_NLTK/tree/master/stop). Its original source was the [Perseus Hopper source](http://sourceforge.net/projects/perseus-hopper), found at "/sgml/reading/build/stoplists", though this only contained acute accents on the ultima. There has thus been added grave accents to the ultima of each.


Perseus source is made available under the [Mozilla Public License 1.1 (MPL 1.1)](http://www.mozilla.org/MPL/1.1/).

The original file was that found in stops\_beta\_code\_lower.txt, which I have transformed into uppercase and Unicode. Note that the Unicode lists do not use the word-final sigma ('ς') and have, if applicable, acute accents.

TODO
----

- ~~See what 'ga^' is supposed to be on line 28 of the original Perseus file.~~ This has been removed from the unicode version.
- Add alternate versions of these words to the list, such as 'ἐξ' for 'ἐκ'.
- Eventually, an entirely new list of stopwords should be generated from the TLG corpus, including the most frequently found words in the entire Ancient Greek canon, as well as more specific lists according to date, genre, etc..
