"""Example paragraphs of text to be reused within the codebase for testing or demonstrating code.

TODO: Get longer Akkadian text

>>> from cltk.languages.example_texts import get_example_text
>>> get_example_text("grc")[:66]
'ὅτι μὲν ὑμεῖς, ὦ ἄνδρες Ἀθηναῖοι, πεπόνθατε ὑπὸ τῶν ἐμῶν κατηγόρων'
>>> get_example_text("lat")[:67]
'Gallia est omnis divisa in partes tres, quarum unam incolunt Belgae'
>>> get_example_text("non")[:50]
'Gylfi konungr réð þar löndum er nú heitir Svíþjóð.'
"""

# pylint: disable=line-too-long

from cltk.core.exceptions import UnimplementedAlgorithmError
from cltk.languages.utils import get_lang

EXAMPLE_TEXTS = dict(
    # Akkadian
    akk="u2-wa-a-ru at-ta e2-kal2-la-ka _e2_-ka wu-e-er",
    # Old English, Beowulf
    ang="""Hwæt. We Gardena in geardagum,
þeodcyninga, þrym gefrunon,
hu ða æþelingas ellen fremedon.
Oft Scyld Scefing sceaþena þreatum,
monegum mægþum, meodosetla ofteah,
egsode eorlas. Syððan ærest wearð
feasceaft funden, he þæs frofre gebad,
weox under wolcnum, weorðmyndum þah,
oðþæt him æghwylc þara ymbsittendra
ofer hronrade hyran scolde,
gomban gyldan. þæt wæs god cyning.
""",
    # Arabic, Quran
    arb="كهيعص ﴿١﴾ ذِكْرُ رَحْمَتِ رَبِّكَ عَبْدَهُ زَكَرِيَّا ﴿٢﴾ إِذْ نَادَىٰ رَبَّهُ نِدَاءً خَفِيًّا ﴿٣﴾ قَالَ رَبِّ إِنِّي وَهَنَ الْعَظْمُ مِنِّي وَاشْتَعَلَ الرَّأْسُ شَيْبًا وَلَمْ أَكُن بِدُعَائِكَ رَبِّ شَقِيًّا ﴿٤﴾ وَإِنِّي خِفْتُ الْمَوَالِيَ مِن وَرَائِي وَكَانَتِ امْرَأَتِي عَاقِرًا فَهَبْ لِي مِن لَّدُنكَ وَلِيًّا ﴿٥﴾ يَرِثُنِي وَيَرِثُ مِنْ آلِ يَعْقُوبَ ۖ وَاجْعَلْهُ رَبِّ رَضِيًّا ﴿٦﴾ يَا زَكَرِيَّا إِنَّا نُبَشِّرُكَ بِغُلَامٍ اسْمُهُ يَحْيَىٰ لَمْ نَجْعَل لَّهُ مِن قَبْلُ سَمِيًّا ﴿٧﴾ قَالَ رَبِّ أَنَّىٰ يَكُونُ لِي غُلَامٌ وَكَانَتِ امْرَأَتِي عَاقِرًا وَقَدْ بَلَغْتُ مِنَ الْكِبَرِ عِتِيًّا ﴿٨﴾ قَالَ كَذَٰلِكَ قَالَ رَبُّكَ هُوَ عَلَيَّ هَيِّنٌ وَقَدْ خَلَقْتُكَ مِن قَبْلُ وَلَمْ تَكُ شَيْئًا ﴿٩﴾ قَالَ رَبِّ اجْعَل لِّي آيَةً ۚ قَالَ آيَتُكَ أَلَّا تُكَلِّمَ النَّاسَ ثَلَاثَ لَيَالٍ سَوِيًّا ﴿١٠﴾ فَخَرَجَ عَلَىٰ قَوْمِهِ مِنَ الْمِحْرَابِ فَأَوْحَىٰ إِلَيْهِمْ أَن سَبِّحُوا بُكْرَةً وَعَشِيًّا ﴿١١﴾",
    # Aramaic, John 1.1-4 with full western vocalization
    arc="ܒ݁ܪܺܫܺܝܬ݂ ܐܺܝܬ݂ܰܘܗ݈ܝ ܗ݈ܘܳܐ ܡܶܠܬ݂ܳܐ ܘܗܽܘ ܡܶܠܬ݂ܳܐ ܐܺܝܬ݂ܰܘܗ݈ܝ ܗ݈ܘܳܐ ܠܘܳܬ݂ ܐܰܠܳܗܳܐ ܘܰܐܠܳܗܳܐ ܐܺܝܬ݂ܰܘܗ݈ܝ ܗ݈ܘܳܐ ܗܽܘ ܡܶܠܬ݂ܳܐ܂ ܗܳܢܳܐ ܐܺܝܬ݂ܰܘܗ݈ܝ ܗ݈ܘܳܐ ܒ݁ܪܺܫܺܝܬ݂ ܠܘܳܬ݂ ܐܰܠܳܗܳܐ܂ ܟ݁ܽܠ ܒ݁ܺܐܝܕ݂ܶܗ ܗܘܳܐ ܘܒ݂ܶܠܥܳܕ݂ܰܘܗ݈ܝ ܐܳܦ݂ܠܳܐ ܚܕ݂ܳܐ ܗܘܳܬ݂ ܡܶܕ݁ܶܡ ܕ݁ܰܗܘܳܐ܂ ܒ݁ܶܗ ܚܰܝܶܐ ܗܘܳܐ ܘܚܰܝܶܐ ܐܺܝܬ݂ܰܝܗܽܘܢ ܢܽܘܗܪܳܐ ܕ݁ܰܒ݂ܢܰܝܢܳܫܳܐ܂",
    # Old Church Slavonic, Lord's Prayer
    chu="""отьчє нашь·
ижє ѥси на нєбєсѣхъ:
да свѧтитъ сѧ имѧ твоѥ·
да придєтъ цѣсар҄ьствиѥ твоѥ·
да бѫдєтъ волꙗ твоꙗ
ꙗко на нєбєси и на ꙁємл҄и:
хлѣбъ нашь насѫщьнꙑи
даждь намъ дьньсь·
и отъпоусти намъ длъгꙑ нашѧ
ꙗко и мꙑ отъпоущаѥмъ
длъжьникомъ нашимъ·
и нє въвєди насъ въ искоушєниѥ·
нъ иꙁбави нꙑ отъ нєприꙗꙁни:
ꙗко твоѥ ѥстъ цѣсар҄ьствиѥ
и сила и слава въ вѣкꙑ вѣкомъ
аминь.""",
    # Coptic, Besa Letters, On Vigilance
    cop="ⲧ︤ⲛ︥ⲇⲟⲅⲙⲁⲧⲓ ⲍⲉϩ︤ⲙ︥ⲡⲕⲟ ⲥⲙⲟⲥⲛ̄ⲑⲉⲛ̄ ⲛⲉⲧⲟⲛ︤ϩ︥· ⲙ̄ⲡⲣ̄ϫⲱϩⲟⲩ ⲧⲉⲙ̄ⲡⲣ̄ϫⲓϯⲡⲉ. ⲟⲩⲧⲉⲙ̄ⲡⲣ̄ϩⲱ⳯ ⲉϩⲟⲩⲛ·ⲉⲧⲉ ⲡⲁⲓ̈ⲡⲉϫⲉⲁⲛ ⲉⲓ̂ⲉⲃⲟⲗϩ︤ⲛ︥ⲛ̄ ⲛⲟⲃⲉⲙ̄ⲡⲕⲟ ⲥⲙⲟⲥⲉⲁⲛⲕⲁ ⲁⲩⲛ̄ⲥⲱⲛ·ⲁϩⲣⲟ⳯ ⲟⲛⲉⲛⲕⲧⲟ̂ⲙ̄ ⲙⲟⲛⲉⲛϭⲗⲟⲙ ⲗ︤ⲙ︥ϩⲣⲁⲓ̈ⲛ̄ϩⲏ ⲧⲟⲩ·ϩⲙ̄ⲡⲁⲓ̈ ⲟⲛ⳿ⲉⲛⲧⲁϥϫⲟⲟⲥ ϫⲉⲙ̄ⲡⲓⲟⲩⲟ ⲉⲓϣⲅⲁⲣⲛⲉⲧⲉ ⲧ︤ⲛ︥ⲟ̂ⲛ̄ⲕⲁⲕⲉ ⲡⲉ·ⲧⲉⲛⲟⲩ ⲇⲉⲛ̄ⲟⲩⲟⲉⲓⲛ ϩ︤ⲙ︥ⲡϫⲟⲉⲓⲥ·",
    # Middle English, Chaucer, The Knight's Tale 1
    enm="""Whilom, as olde stories tellen us,
Ther was a duc that highte theseus;
Of atthenes he was lord and governour,
And in his tyme swich a conquerour,
That gretter was ther noon under the sonne.
Ful many a riche contree hadde he wonne;
What with his wysdom and his chivalrie,
He conquered al the regne of femenye,
That whilom was ycleped scithia,
And weddede the queene ypolita,
And broghte hire hoom with hym in his contree
With muchel glorie and greet solempnytee,
And eek hir yonge suster emelye.
And thus with victorie and with melodye
Lete I this noble duc to atthenes ryde,
And al his hoost in armes hym bisyde.""",
    # Middle French, Montaigne, Les Essais, "De la Parsimonie des Anciens"
    frm="Attilius Regulus, general de l'armée Romaine en Afrique, au milieu de sa gloire et de ses victoires contre les Carthaginois, escrivit à la chose publique qu'un valet de labourage qu'il avoit laissé seul au gouvernement de son bien, qui estoit en tout sept arpents de terre, s'en estoit enfuy, ayant desrobé ses utils de labourage, et demandoit congé pour s'en retourner et y pourvoir, de peur que sa femme et ses enfans n'en eussent à souffrir: le Senat pourveut à commettre un autre à la conduite de ses biens et luy fist restablir ce qui luy avoit esté desrobé, et ordonna que sa femme et enfans seroient nourris aux despens du public. Le vieux Caton, revenant d'Espaigne Consul, vendit son cheval de service pour espargner l'argent qu'il eut couté à le ramener par mer en Italie; et, estant au gouvernement de Sardaigne, faisoit ses visitations à pied, n'ayant avec luy autre suite qu'un officier de la chose publique, qui luy portoit sa robbe, et un vase à faire des sacrifices; et le plus souvent il pourtoit sa male luy mesme. ",
    # Old French, Li Lay del Trot, 1
    fro="""Une aventure vos voil dire
Molt bien rimee tire a tire;
Com il avint vos conterai,
Ne ja ne vos en mentirai.
L’aventure fu molt estraigne,
Si avint jadis en Bretaigne
A .I. molt riche chevalier,
Hardi et coragous et fier;
De la Table Reonde estoit
Le roi Artu, que bien savoit
.I. bon chevalier honorer
Et riches dons sovent doner.
Li chevaliers ot non Lorois,
Si ert del castel de Morois,
S’ot .Vc. livrees de terre,
Miex seant ne peüsciés querre.
Et si ot molt bele maison,
Close de haut mur environ,
Et si ot molt parfont fossés
Trestot de novel regetés.
Et desos le castel aprés
Avoit rivieres et forés
Ou li chevaliers vout aler
Sovent por son cors deporter.""",
    # Middle High German, das Nibelungenlied
    gmh="""Uns ist in alten
mæren wunders vil geseit
von heleden lobebæren
von grozer arebeit
von frevde und hochgeciten
von weinen und klagen
von kvner recken striten
muget ir nu wunder horen sagen
    """,
    # Old High German, Hildebrandslied
    goh="""Ik gihorta ðat seggen
ðat sih urhettun ænon muotin
Hiltibrant enti Haðubrant untar heriun tuem
sunufatarungo iro saro rihtun
garutun se iro guðhamun gurtun sih iro suert ana
helidos ubar hringa do sie to dero hiltiu ritun""",
    # Gothic, Matthaeus 5.16-18
    got="swa liuhtjai liuhaþ izwar in andwairþja manne, ei gasaiƕaina izwara goda waurstwa jah hauhjaina attan izwarana þana in himinam. ni hugjaiþ ei qemjau gatairan witoþ aiþþau praufetuns; ni qam gatairan, ak usfulljan. amen auk qiþa izwis: und þatei usleiþiþ himins jah airþa, jota ains aiþþau ains striks ni usleiþiþ af witoda, unte allata wairþiþ.",
    # Ancient Greek, Plato, Apology (17)
    grc="ὅτι μὲν ὑμεῖς, ὦ ἄνδρες Ἀθηναῖοι, πεπόνθατε ὑπὸ τῶν ἐμῶν κατηγόρων, οὐκ οἶδα: ἐγὼ δ᾽ οὖν καὶ αὐτὸς ὑπ᾽ αὐτῶν ὀλίγου ἐμαυτοῦ ἐπελαθόμην, οὕτω πιθανῶς ἔλεγον. καίτοι ἀληθές γε ὡς ἔπος εἰπεῖν οὐδὲν εἰρήκασιν. μάλιστα δὲ αὐτῶν ἓν ἐθαύμασα τῶν πολλῶν ὧν ἐψεύσαντο, τοῦτο ἐν ᾧ ἔλεγον ὡς χρῆν ὑμᾶς εὐλαβεῖσθαι μὴ ὑπ᾽ ἐμοῦ ἐξαπατηθῆτε ὡς δεινοῦ ὄντος λέγειν. τὸ γὰρ μὴ αἰσχυνθῆναι ὅτι αὐτίκα ὑπ᾽ ἐμοῦ ἐξελεγχθήσονται ἔργῳ, ἐπειδὰν μηδ᾽ ὁπωστιοῦν φαίνωμαι δεινὸς λέγειν, τοῦτό μοι ἔδοξεν αὐτῶν ἀναισχυντότατον εἶναι, εἰ μὴ ἄρα δεινὸν καλοῦσιν οὗτοι λέγειν τὸν τἀληθῆ λέγοντα: εἰ μὲν γὰρ τοῦτο λέγουσιν, ὁμολογοίην ἂν ἔγωγε οὐ κατὰ τούτους εἶναι ῥήτωρ. οὗτοι μὲν οὖν, ὥσπερ ἐγὼ λέγω, ἤ τι ἢ οὐδὲν ἀληθὲς εἰρήκασιν, ὑμεῖς δέ μου ἀκούσεσθε πᾶσαν τὴν ἀλήθειαν—οὐ μέντοι μὰ Δία, ὦ ἄνδρες Ἀθηναῖοι, κεκαλλιεπημένους γε λόγους, ὥσπερ οἱ τούτων, ῥήμασί τε καὶ ὀνόμασιν οὐδὲ κεκοσμημένους, ἀλλ᾽ ἀκούσεσθε εἰκῇ λεγόμενα τοῖς ἐπιτυχοῦσιν ὀνόμασιν—πιστεύω γὰρ δίκαια εἶναι ἃ λέγω—καὶ μηδεὶς ὑμῶν προσδοκησάτω ἄλλως: οὐδὲ γὰρ ἂν δήπου πρέποι, ὦ ἄνδρες, τῇδε τῇ ἡλικίᾳ ὥσπερ μειρακίῳ πλάττοντι λόγους εἰς ὑμᾶς εἰσιέναι. καὶ μέντοι καὶ πάνυ, ὦ ἄνδρες Ἀθηναῖοι, τοῦτο ὑμῶν δέομαι καὶ παρίεμαι: ἐὰν διὰ τῶν αὐτῶν λόγων ἀκούητέ μου ἀπολογουμένου δι᾽ ὧνπερ εἴωθα λέγειν καὶ ἐν ἀγορᾷ ἐπὶ τῶν τραπεζῶν, ἵνα ὑμῶν πολλοὶ ἀκηκόασι, καὶ ἄλλοθι, μήτε θαυμάζειν μήτε θορυβεῖν τούτου ἕνεκα. ἔχει γὰρ οὑτωσί. νῦν ἐγὼ πρῶτον ἐπὶ δικαστήριον ἀναβέβηκα, ἔτη γεγονὼς ἑβδομήκοντα: ἀτεχνῶς οὖν ξένως ἔχω τῆς ἐνθάδε λέξεως. ὥσπερ οὖν ἄν, εἰ τῷ ὄντι ξένος ἐτύγχανον ὤν, συνεγιγνώσκετε δήπου ἄν μοι εἰ ἐν ἐκείνῃ τῇ φωνῇ τε καὶ τῷ τρόπῳ  ἔλεγον ἐν οἷσπερ ἐτεθράμμην, καὶ δὴ καὶ νῦν τοῦτο ὑμῶν δέομαι δίκαιον, ὥς γέ μοι δοκῶ, τὸν μὲν τρόπον τῆς λέξεως ἐᾶν—ἴσως μὲν γὰρ χείρων, ἴσως δὲ βελτίων ἂν εἴη—αὐτὸ δὲ τοῦτο σκοπεῖν καὶ τούτῳ τὸν νοῦν προσέχειν, εἰ δίκαια λέγω ἢ μή: δικαστοῦ μὲν γὰρ αὕτη ἀρετή, ῥήτορος δὲ τἀληθῆ λέγειν.",
    # Tulsidas, Ramcharitmanas
    hin="मैं पुनि निज गुर सन सुनी कथा सो सूकरखेत । समुझी नहिं तस बालपन तब अति रहेउँ अचेत ॥",
    # Hebrew, Job 1
    hbo="אִ֛ישׁ הָיָ֥ה בְאֶֽרֶץ־ע֖וּץ אִיּ֣וֹב שְׁמ֑וֹ וְהָיָ֣ה ׀ הָאִ֣ישׁ הַה֗וּא תָּ֧ם וְיָשָׁ֛ר וִירֵ֥א אֱלֹהִ֖ים וְסָ֥ר מֵרָֽע׃ וַיִּוָּ֥לְדוּ ל֛וֹ שִׁבְעָ֥ה בָנִ֖ים וְשָׁל֥וֹשׁ בָּנֽוֹת׃ וַיְהִ֣י מִ֠קְנֵהוּ שִֽׁבְעַ֨ת אַלְפֵי־צֹ֜אן וּשְׁלֹ֧שֶׁת אַלְפֵ֣י גְמַלִּ֗ים וַחֲמֵ֨שׁ מֵא֤וֹת צֶֽמֶד־בָּקָר֙ וַחֲמֵ֣שׁ מֵא֣וֹת אֲתוֹנ֔וֹת וַעֲבֻדָּ֖ה רַבָּ֣ה מְאֹ֑ד וַיְהִי֙ הָאִ֣ישׁ הַה֔וּא גָּד֖וֹל מִכָּל־בְּנֵי־קֶֽדֶם׃ וְהָלְכ֤וּ בָנָיו֙ וְעָשׂ֣וּ מִשְׁתֶּ֔ה בֵּ֖ית אִ֣ישׁ יוֹמ֑וֹ וְשָׁלְח֗וּ וְקָרְאוּ֙ לִשְׁלֹ֣שֶׁת אחיתיהם אַחְיֽוֹתֵיהֶ֔ם לֶאֱכֹ֥ל וְלִשְׁתּ֖וֹת עִמָּהֶֽם׃ וַיְהִ֡י כִּ֣י הִקִּיפֽוּ֩ יְמֵ֨י הַמִּשְׁתֶּ֜ה וַיִּשְׁלַ֧ח אִיּ֣וֹב וַֽיְקַדְּשֵׁ֗ם וְהִשְׁכִּ֣ים בַּבֹּקֶר֮ וְהֶעֱלָ֣ה עֹלוֹת֮ מִסְפַּ֣ר כֻּלָּם֒ כִּ֚י אָמַ֣ר אִיּ֔וֹב אוּלַי֙ חָטְא֣וּ בָנַ֔י וּבֵרֲכ֥וּ אֱלֹהִ֖ים בִּלְבָבָ֑ם כָּ֛כָה יַעֲשֶׂ֥ה אִיּ֖וֹב כָּל־הַיָּמִֽים׃ (פ) וַיְהִ֣י הַיּ֔וֹם וַיָּבֹ֙אוּ֙ בְּנֵ֣י הָאֱלֹהִ֔ים לְהִתְיַצֵּ֖ב עַל־יְהוָ֑ה וַיָּב֥וֹא גַֽם־הַשָּׂטָ֖ן בְּתוֹכָֽם׃ וַיֹּ֧אמֶר יְהוָ֛ה אֶל־הַשָּׂטָ֖ן מֵאַ֣יִן תָּבֹ֑א וַיַּ֨עַן הַשָּׂטָ֤ן אֶת־יְהוָה֙ וַיֹּאמַ֔ר מִשּׁ֣וּט בָּאָ֔רֶץ וּמֵֽהִתְהַלֵּ֖ךְ בָּֽהּ׃ וַיֹּ֤אמֶר יְהוָה֙ אֶל־הַשָּׂטָ֔ן הֲשַׂ֥מְתָּ לִבְּךָ֖ עַל־עַבְדִּ֣י אִיּ֑וֹב כִּ֣י אֵ֤ין כָּמֹ֙הוּ֙ בָּאָ֔רֶץ אִ֣ישׁ תָּ֧ם וְיָשָׁ֛ר יְרֵ֥א אֱלֹהִ֖ים וְסָ֥ר מֵרָֽע׃ וַיַּ֧עַן הַשָּׂטָ֛ן אֶת־יְהוָ֖ה וַיֹּאמַ֑ר הַֽחִנָּ֔ם יָרֵ֥א אִיּ֖וֹב אֱלֹהִֽים׃ הֲלֹֽא־את אַ֠תָּה שַׂ֣כְתָּ בַעֲד֧וֹ וּבְעַד־בֵּית֛וֹ וּבְעַ֥ד כָּל־אֲשֶׁר־ל֖וֹ מִסָּבִ֑יב מַעֲשֵׂ֤ה יָדָיו֙ בֵּרַ֔כְתָּ וּמִקְנֵ֖הוּ פָּרַ֥ץ בָּאָֽרֶץ׃ וְאוּלָם֙ שְֽׁלַֽח־נָ֣א יָֽדְךָ֔ וְגַ֖ע בְּכָל־אֲשֶׁר־ל֑וֹ אִם־לֹ֥א עַל־פָּנֶ֖יךָ יְבָרֲכֶֽךָּ׃ וַיֹּ֨אמֶר יְהוָ֜ה אֶל־הַשָּׂטָ֗ן הִנֵּ֤ה כָל־אֲשֶׁר־לוֹ֙ בְּיָדֶ֔ךָ רַ֣ק אֵלָ֔יו אַל־תִּשְׁלַ֖ח יָדֶ֑ךָ וַיֵּצֵא֙ הַשָּׂטָ֔ן מֵעִ֖ם פְּנֵ֥י יְהוָֽה׃ וַיְהִ֖י הַיּ֑וֹם וּבָנָ֨יו וּבְנֹתָ֤יו אֹֽכְלִים֙ וְשֹׁתִ֣ים יַ֔יִן בְּבֵ֖ית אֲחִיהֶ֥ם הַבְּכֽוֹר׃ וּמַלְאָ֛ךְ בָּ֥א אֶל־אִיּ֖וֹב וַיֹּאמַ֑ר הַבָּקָר֙ הָי֣וּ חֹֽרְשׁ֔וֹת וְהָאֲתֹנ֖וֹת רֹע֥וֹת עַל־יְדֵיהֶֽם׃ וַתִּפֹּ֤ל שְׁבָא֙ וַתִּקָּחֵ֔ם וְאֶת־הַנְּעָרִ֖ים הִכּ֣וּ לְפִי־חָ֑רֶב וָֽאִמָּ֨לְטָ֧ה רַק־אֲנִ֛י לְבַדִּ֖י לְהַגִּ֥יד לָֽךְ׃ ע֣וֹד ׀ זֶ֣ה מְדַבֵּ֗ר וְזֶה֮ בָּ֣א וַיֹּאמַר֒ אֵ֣שׁ אֱלֹהִ֗ים נָֽפְלָה֙ מִן־הַשָּׁמַ֔יִם וַתִּבְעַ֥ר בַּצֹּ֛אן וּבַנְּעָרִ֖ים וַתֹּאכְלֵ֑ם וָאִמָּ֨לְטָ֧ה רַק־אֲנִ֛י לְבַדִּ֖י לְהַגִּ֥יד לָֽךְ׃ ע֣וֹד ׀ זֶ֣ה מְדַבֵּ֗ר וְזֶה֮ בָּ֣א וַיֹּאמַר֒ כַּשְׂדִּ֞ים שָׂ֣מוּ ׀ שְׁלֹשָׁ֣ה רָאשִׁ֗ים וַֽיִּפְשְׁט֤וּ עַל־הַגְּמַלִּים֙ וַיִּקָּח֔וּם וְאֶת־הַנְּעָרִ֖ים הִכּ֣וּ לְפִי־חָ֑רֶב וָאִמָּ֨לְטָ֧ה רַק־אֲנִ֛י לְבַדִּ֖י לְהַגִּ֥יד לָֽךְ׃ עַ֚ד זֶ֣ה מְדַבֵּ֔ר וְזֶ֖ה בָּ֣א וַיֹּאמַ֑ר בָּנֶ֨יךָ וּבְנוֹתֶ֤יךָ אֹֽכְלִים֙ וְשֹׁתִ֣ים יַ֔יִן בְּבֵ֖ית אֲחִיהֶ֥ם הַבְּכֽוֹר׃ וְהִנֵּה֩ ר֨וּחַ גְּדוֹלָ֜ה בָּ֣אָה ׀ מֵעֵ֣בֶר הַמִּדְבָּ֗ר וַיִּגַּע֙ בְּאַרְבַּע֙ פִּנּ֣וֹת הַבַּ֔יִת וַיִּפֹּ֥ל עַל־הַנְּעָרִ֖ים וַיָּמ֑וּתוּ וָאִמָּ֨לְטָ֧ה רַק־אֲנִ֛י לְבַדִּ֖י לְהַגִּ֥יד לָֽךְ׃ וַיָּ֤קָם אִיּוֹב֙ וַיִּקְרַ֣ע אֶת־מְעִל֔וֹ וַיָּ֖גָז אֶת־רֹאשׁ֑וֹ וַיִּפֹּ֥ל אַ֖רְצָה וַיִּשְׁתָּֽחוּ׃ וַיֹּאמֶר֩ עָרֹ֨ם יצתי יָצָ֜אתִי מִבֶּ֣טֶן אִמִּ֗י וְעָרֹם֙ אָשׁ֣וּב שָׁ֔מָה יְהוָ֣ה נָתַ֔ן וַיהוָ֖ה לָקָ֑ח יְהִ֛י שֵׁ֥ם יְהוָ֖ה מְבֹרָֽךְ׃ בְּכָל־זֹ֖את לֹא־חָטָ֣א אִיּ֑וֹב וְלֹא־נָתַ֥ן תִּפְלָ֖ה לֵאלֹהִֽים׃",
    # Latin, Caesar, De bello Gallico (1.1)
    lat="Gallia est omnis divisa in partes tres, quarum unam incolunt Belgae, aliam Aquitani, tertiam qui ipsorum lingua Celtae, nostra Galli appellantur. Hi omnes lingua, institutis, legibus inter se differunt. Gallos ab Aquitanis Garumna flumen, a Belgis Matrona et Sequana dividit. Horum omnium fortissimi sunt Belgae, propterea quod a cultu atque humanitate provinciae longissime absunt, minimeque ad eos mercatores saepe commeant atque ea quae ad effeminandos animos pertinent important, proximique sunt Germanis, qui trans Rhenum incolunt, quibuscum continenter bellum gerunt. Qua de causa Helvetii quoque reliquos Gallos virtute praecedunt, quod fere cotidianis proeliis cum Germanis contendunt, cum aut suis finibus eos prohibent aut ipsi in eorum finibus bellum gerunt. Eorum una, pars, quam Gallos obtinere dictum est, initium capit a flumine Rhodano, continetur Garumna flumine, Oceano, finibus Belgarum, attingit etiam ab Sequanis et Helvetiis flumen Rhenum, vergit ad septentriones. Belgae ab extremis Galliae finibus oriuntur, pertinent ad inferiorem partem fluminis Rheni, spectant in septentrionem et orientem solem. Aquitania a Garumna flumine ad Pyrenaeos montes et eam partem Oceani quae est ad Hispaniam pertinet; spectat inter occasum solis et septentriones.",
    # Classical Chinese, Shiji, Annals of the Five Emperors
    lzh="黃帝者，少典之子，姓公孫，名曰軒轅。生而神靈，弱而能言，幼而徇齊，長而敦敏，成而聰明。軒轅之時，神農氏世衰。諸侯相侵伐，暴虐百姓，而神農氏弗能征。於是軒轅乃習用干戈，以征不享，諸侯咸來賓從。而蚩尤最為暴，莫能伐。炎帝欲侵陵諸侯，諸侯咸歸軒轅。軒轅乃修德振兵，治五氣，藝五種，撫萬民，度四方，教熊羆貔貅貙虎，以與炎帝戰於阪泉之野。三戰然後得其志。蚩尤作亂，不用帝命。於是黃帝乃徵師諸侯，與蚩尤戰於涿鹿之野，遂禽殺蚩尤。而諸侯咸尊軒轅為天子，代神農氏，是為黃帝。天下有不順者，黃帝從而征之，平者去之，披山通道，未嘗寧居。",
    # Old Norse, Prose Edda, Gylfaginning 1
    non="Gylfi konungr réð þar löndum er nú heitir Svíþjóð. Frá honum er þat sagt at hann gaf einni farandi konu at launum skemmtunar sinnar eitt plógsland í ríki sínu þat er fjórir öxn drægi upp dag ok nótt. En sú kona var ein af ása ætt, hon er nefnd Gefjun. Hon tók fjóra öxn norðan ór Jötunheimum, en þat váru synir jötuns nökkurs ok hennar, ok setti þá fyrir plóg, en plógrinn gekk svá breitt ok djúpt at upp leysti landit, ok drógu öxnirnir þat land út á hafit ok vestr ok námu staðar í sundi nökkuru. Þar setti Gefjun landit ok gaf nafn ok kallaði Selund. Ok þar sem landit hafði upp gengit var þar eftir vatn. Þat er nú Lögrinn kallaðr í Svíþjóð, ok liggja svá víkr í Leginum sem nes í Selundi.",
    # Guru Granth Sahib, ੧ਓ ਸਿਤ ਨਾਮੁ ਕਰਤਾ ਪੁਰਖੁ ਿਨਰਭਉ ਿਨਰਵੈਰੁ ਅਕਾਲ ਮੂਰਿਤ ਅਜੂਨੀ ਸੈਭ ੰ ਗੁਰ ਪਰ੍ਸਾਿਦ
    pan="ਆਿਦ ਸਚ ੁ ਜੁਗਾਿਦ ਸਚ ੁ ॥ ਹੈ ਭੀ ਸਚ ੁ ਨਾਨਕ ਹੋਸੀ ਭੀ ਸਚ ੁ ॥੧॥ ਸੋਚੈ ਸੋਿਚ ਨ ਹੋਵਈ ਜੇ ਸੋਚੀ ਲਖ ਵਾਰ ॥ ਚ ੁਪੈ ਚ ੁਪ ਨ ਹੋਵਈ ਜੇ ਲਾਇ ਰਹਾ ਿਲਵ ਤਾਰ ॥ ਭੁਿਖਆ ਭੁਖ ਨ ਉਤਰੀ ਜੇ ਬ ੰਨਾ ਪੁਰੀਆ ਭਾਰ ॥ ਸਹਸ ਿਸਆਣਪਾ ਲਖ ਹੋਿਹ ਤ ਇਕ ਨ ਚਲੈ ਨਾਿਲ ॥",
    # Pali, Milindapañha 32-33
    pli="Raajaa aaha 'ki.mlakkha.no, bhante naagasena, manasikaaro, ki.mlakkha.naa pa~n~naa'ti? 'Uuhanalakkha.no kho, mahaaraaja, manasikaaro, chedanalakkha.naa pa~n~naa'ti. 'Katha.m uuhanalakkha.no manasikaaro, katha.m chedanalakkha.naa pa~n~naa, opamma.m karohii'ti. 'Jaanaasi, tva.m mahaaraaja, yavalaavake'ti. 'Aama bhante, jaanaamii'ti. 'Katha.m, mahaaraaja, yavalaavakaa yava.m lunantii'ti? 'Vaamena, bhante, hatthena yavakalaapa.m gahetvaa dakkhi.nena hatthena daatta.m gahetvaa daattena chindantii'ti. 'Yathaa, mahaaraaja, yavalaavako vaamena hatthena yavakalaapa.m gahetvaa dakkhi.nena hatthena daatta.m gahetvaa yava.m chindati, evameva kho, mahaaraaja, yogaavacaro manasikaarena maanasa.m gahetvaa pa~n~naaya kilese chindati, eva.m kho, mahaaraaja, uuhanalakkha.no manasikaaro, eva.m chedanalakkha.naa pa~n~naa'ti. 'Kallosi, bhante naagasenaa'ti.",
    # Sanskrit, Isha Upanishad (Īśāvāsyopaniṣad)
    san="""ईशा वास्यम् इदं सर्वं यत् किञ्च जगत्यां जगत् ।
तेन त्यक्तेन भुञ्जीथा मा गृधः कस्य स्विद्धनम् ॥

कुर्वन्न् एवेह कर्माणि जिजीविषेच्छतं समाः ।
एवं त्वयि नान्यथेतोऽस्ति न कर्म लिप्यते नरे ॥

असुर्या नाम ते लोका अन्धेन तमसावृताः ।
तांस्ते प्रेत्याभिगच्छन्ति ये के चात्महनो जनाः ॥

अनेजद् एकं मनसो जवीयो नैनद्देवा आप्नुवन्पूर्वमर्षत् ।
तद्धावतोऽन्यानत्येति तिष्ठत् तस्मिन्न् अपो मातरिश्वा दधाति ॥

तद् एजति तन् नैजति तद् दूरे तद् व् अन्तिके ।
तद् अन्तर् अस्य सर्वस्य तद् उ सर्वस्यास्य बाह्यतः ॥

यस् तु सर्वाणि भूतान्य् आत्मन्य् एवानुपश्यति ।
सर्वभूतेषु चात्मानं ततो न विजुगुप्सते ॥""",
)


def get_example_text(iso_code: str) -> str:
    """Take in search term of usual language name and find ISO code.

    >>> from cltk.languages.example_texts import get_example_text
    >>> get_example_text("got")[:25]
    'swa liuhtjai liuhaþ izwar'
    >>> get_example_text("zkz")
    Traceback (most recent call last):
      ...
    cltk.core.exceptions.UnimplementedAlgorithmError: Example text unavailable for ISO 639-3 code 'zkz'.
    >>> get_example_text("xxx")
    Traceback (most recent call last):
      ...
    cltk.core.exceptions.UnknownLanguageError: Unknown ISO language code 'xxx'.
    """
    get_lang(iso_code=iso_code)
    try:
        return EXAMPLE_TEXTS[iso_code]
    except KeyError:
        raise UnimplementedAlgorithmError(
            f"Example text unavailable for ISO 639-3 code '{iso_code}'."
        )
