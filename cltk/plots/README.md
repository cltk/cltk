# Plots


## Lexical Dispersion Plot

```python
from cltk.plots import dispersionPlot
dispersionPlot.dispersionPlot(text, words, lang)
```

Parameters to be passed
* text: The text whose dispersion plot is to be drawn
* words: List of words. The distribution of these words in the given text is plotted 
* lang:  The ISO 639-1 Language Code of the language in which the text is based on

```python
from cltk.plots import dispersionPlot
text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras at maximus dui. Sed mauris ipsum, gravida id velit at, lobortis aliquam magna. Nam feugiat nibh eget cursus rutrum. Fusce eu euismod turpis, in posuere elit. In pellentesque massa sit amet sem posuere, vel viverra justo suscipit. Aenean nibh sem, imperdiet nec sem sit amet, maximus euismod velit. Ut vitae ex mauris. Donec laoreet lorem at diam viverra dapibus. Suspendisse elementum rhoncus commodo. Donec massa purus, dignissim maximus laoreet in, pharetra euismod nulla.Nunc eu libero lacus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Morbi eget tincidunt velit. Curabitur a libero vel felis maximus ultrices. Donec porta fringilla purus eget porttitor. In cursus lobortis sapien, sit amet euismod eros semper quis. Fusce luctus eleifend neque, gravida mollis massa fringilla sit amet. Nunc placerat, purus sit amet maximus sollicitudin, sapien sem suscipit elit, non aliquet nunc nisl in arcu.Quisque eu nisi interdum, pretium elit vel, dignissim est. Ut lobortis vehicula lectus, imperdiet tristique lorem pulvinar at. Phasellus leo justo, tempor at maximus a, vehicula et urna. Nunc blandit eros in dui venenatis placerat. Maecenas vehicula neque orci, at tempor elit vehicula et. Integer elementum, diam nec mattis porttitor, risus nibh vehicula quam, sit amet pellentesque quam ante commodo orci. Etiam sed dignissim tellus. Cras non ultrices velit, eget egestas justo. Ut rutrum condimentum lorem, ut auctor massa dictum eu. Morbi dictum eget eros sed varius. Nunc tristique mollis fermentum. Donec vel odio gravida, fringilla ante a, volutpat dolor. Vestibulum facilisis dictum magna id aliquam. Etiam ex ex, ultricies a dignissim vitae, sollicitudin nec orci. Nam eu augue et libero porttitor maximus volutpat a risus. Suspendisse eget mauris et mi tincidunt suscipit."

words = ["Lorem", "ipsum"]
dispersionPlot(text, words, "la")
```
