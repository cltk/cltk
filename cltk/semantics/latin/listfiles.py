from os import listdir
from os.path import isfile, join, expanduser

rel_path = join('~/tesserae/texts/la')
path = expanduser(rel_path)
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
onlyfiles = [join(path, f) for f in onlyfiles]