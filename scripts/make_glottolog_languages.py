"""Module for mapping ISO 639-3 to Glottolog languages and language names.
The contents of ``cltk/languages/glottolog.py`` were created by this.
"""

import csv
import os
import typing
from collections import OrderedDict, defaultdict

from cltk.utils.data_types import Language


def make_iso_glotto_map():
    """Generate above dict of ISO code to Glottolog data. Writes
    file to ``~/Downloads/cltk_langs.dict``. Download file ``languoid.csv`` at:
    `<https://glottolog.org/meta/downloads>`_.
    """
    # Get ISO langs marked historical or ancient
    # ['Id', 'Part2B', 'Part2T', 'Part1', 'Scope',
    # 'Language_Type', 'Ref_Name', 'Comment']
    iso_fp = os.path.expanduser(
        "~/Downloads/iso-639-3_Code_Tables_20190408/iso-639-3_20190408.tab"
    )
    iso_name_h = dict()  # is historical type
    iso_name_a = dict()  # is ancient type
    with open(iso_fp) as file_open:
        csv_reader = csv.reader(file_open, delimiter="\t")
        for row in csv_reader:
            if row[5] == "H":
                iso_code = row[0]
                iso_name = row[6]
                iso_name_h[iso_code] = iso_name
            if row[5] == "A":
                iso_code = row[0]
                iso_name = row[6]
                iso_name_a[iso_code] = iso_name
    print("ISO 639-3 properties:")
    print("\tAncient:", len(iso_name_a))
    print("\tHistorical:", len(iso_name_h))
    print("\tTotal:", len(iso_name_a) + len(iso_name_h))
    print("")

    # Get Glottolog langs that have been marked as ancient or historical in ISO
    # ['id,family_id,parent_id,description,bookkeeping,level,
    # latitude,longitude,iso639P3code,description,
    # markup_description,child_family_count,
    # child_language_count,child_dialect_count,
    # country_ids']
    glottolog_csv = os.path.expanduser(
        "~/Downloads/glottolog_languoid.csv/languoid.csv"
    )
    glottolog_dict = defaultdict(Language)
    with open(glottolog_csv) as file_open:
        csv_reader = csv.reader(file_open, delimiter=",")
        for row in csv_reader:
            if row[8] in iso_name_a.keys():
                lang_type = "a"
                del iso_name_a[row[8]]
            elif row[8] in iso_name_h.keys():
                lang_type = "h"
                del iso_name_h[row[8]]
            else:
                continue
            glottolog_id = row[0]
            glottolog_family_id = row[1]
            glottolog_parent_id = row[2]
            glottolog_name = row[3]
            glottolog_level = row[5]
            try:
                glottolog_lat = float(row[6])
            except ValueError:
                glottolog_lat = 0.0
            try:
                glottolog_long = float(row[7])
            except ValueError:
                glottolog_long = 0.0
            glottolog_iso639p3code = row[8]
            lang_object = Language(
                name=glottolog_name,
                glottolog_id=glottolog_id,
                latitude=glottolog_lat,
                longitude=glottolog_long,
                dates=list(),
                family_id=glottolog_family_id,
                parent_id=glottolog_parent_id,
                level=glottolog_level,
                iso639P3code=glottolog_iso639p3code,
                type=lang_type,
            )
            glottolog_dict[glottolog_iso639p3code] = lang_object

    print("Remaining 'ancient' ISO languages not in Glottolog", len(iso_name_a))
    print("Remaining 'historical' ISO languages not in Glottolog", len(iso_name_h))

    # Add those in ISO but not in Language
    for iso_code, iso_name in iso_name_a.items():
        lang_object = Language(
            name=iso_name,
            glottolog_id="",
            latitude=0.0,
            longitude=0.0,
            dates=list(),
            family_id="",
            parent_id="",
            level="",
            iso639P3code=iso_code,
            type="a",
        )
        glottolog_dict[iso_code] = lang_object
    for iso_code, iso_name in iso_name_h.items():
        lang_object = Language(
            name=iso_name,
            glottolog_id="",
            latitude=0.0,
            longitude=0.0,
            dates=list(),
            family_id="",
            parent_id="",
            level="",
            iso639P3code=iso_code,
            type="h",
        )
        glottolog_dict[iso_code] = lang_object
    print("Total languages in final op_output (ISO & Glottolog):", len(glottolog_dict))

    # sort alpha
    lang_keys_sorted = sorted(glottolog_dict)
    glottolog_dict_ordered = OrderedDict()
    for lang in lang_keys_sorted:
        glottolog_dict_ordered[lang] = glottolog_dict[lang]

    # now write as string to txt file, in order to copy-paste into this file
    txt_fp = os.path.expanduser("~/Downloads/cltk_langs.dict")
    with open(txt_fp, "w") as file_open:
        file_open.write(str(glottolog_dict_ordered))
    print("Wrote file to:", txt_fp)


if __name__ == "__main__":
    make_iso_glotto_map()
