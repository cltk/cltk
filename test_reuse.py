from cltk.text_reuse.text_reuse import TextReuse

demo_prop_short = """
corniger Arcadii vacuam pastoris in aulam
dux aries saturas ipse reduxit oves;
dique deaeque omnes, quibus est tutela per agros,
praebebant vestri verba benigna foci:
'et leporem, quicumque venis, venaberis, hospes,
et si forte meo tramite quaeris avem:
et me Pana tibi comitem de rupe vocato,
sive petes calamo praemia, sive cane.'
at nunc desertis cessant sacraria lucis:
aurum omnes victa iam pietate colunt.
auro pulsa fides, auro venalia iura,
aurum lex sequitur, mox sine lege pudor.
"""

demo_verg_short = """
tuque o, cui prima frementem
fudit equum magno tellus percussa tridenti,
Neptune; et cultor nemorum, cui pinguia Ceae
ter centum niuei tondent dumeta iuuenci;
ipse nemus linquens patrium saltusque Lycaei
Pan, ouium custos, tua si tibi Maenala curae,
adsis, o Tegeaee, fauens, oleaeque Minerua
inuentrix, uncique puer monstrator aratri,
et teneram ab radice ferens, Siluane, cupressum:
dique deaeque omnes, studium quibus arua tueri,
munera vestra cano. et vos o agrestum praesentia
quique nouas alitis non ullo semine fruges
quique satis largum caelo demittitis imbrem.
"""

t = TextReuse(False, True)

comparisons_sliding_window = t.compare_sliding_window(demo_verg_short, demo_prop_short, 50, 20, True)

for comparison_row in comparisons_sliding_window:
    for comparison in comparison_row:
        if comparison.ratio > 0.5:
            print(comparison.str_a, comparison.str_b, comparison.ratio)
