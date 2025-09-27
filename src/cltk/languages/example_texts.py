"""Example paragraphs of text to be reused within the codebase for testing or demonstrating code."""

# pylint: disable=line-too-long

from cltk.core.exceptions import UnimplementedAlgorithmError
from cltk.languages.glottolog import resolve_languoid

# from cltk.languages.utils import get_lang

EXAMPLE_TEXTS: dict[str, str] = {
    "akka1240": "u2-wa-a-ru at-ta e2-kal2-la-ka _e2_-ka wu-e-er",
    # Beowulf
    "olde1238": """Hwæt. We Gardena in geardagum,
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
    # Classical Arabic, Quran
    "clas1259": "كهيعص ﴿١﴾ ذِكْرُ رَحْمَتِ رَبِّكَ عَبْدَهُ زَكَرِيَّا ﴿٢﴾ إِذْ نَادَىٰ رَبَّهُ نِدَاءً خَفِيًّا ﴿٣﴾ قَالَ رَبِّ إِنِّي وَهَنَ الْعَظْمُ مِنِّي وَاشْتَعَلَ الرَّأْسُ شَيْبًا وَلَمْ أَكُن بِدُعَائِكَ رَبِّ شَقِيًّا ﴿٤﴾ وَإِنِّي خِفْتُ الْمَوَالِيَ مِن وَرَائِي وَكَانَتِ امْرَأَتِي عَاقِرًا فَهَبْ لِي مِن لَّدُنكَ وَلِيًّا ﴿٥﴾ يَرِثُنِي وَيَرِثُ مِنْ آلِ يَعْقُوبَ ۖ وَاجْعَلْهُ رَبِّ رَضِيًّا ﴿٦﴾ يَا زَكَرِيَّا إِنَّا نُبَشِّرُكَ بِغُلَامٍ اسْمُهُ يَحْيَىٰ لَمْ نَجْعَل لَّهُ مِن قَبْلُ سَمِيًّا ﴿٧﴾ قَالَ رَبِّ أَنَّىٰ يَكُونُ لِي غُلَامٌ وَكَانَتِ امْرَأَتِي عَاقِرًا وَقَدْ بَلَغْتُ مِنَ الْكِبَرِ عِتِيًّا ﴿٨﴾ قَالَ كَذَٰلِكَ قَالَ رَبُّكَ هُوَ عَلَيَّ هَيِّنٌ وَقَدْ خَلَقْتُكَ مِن قَبْلُ وَلَمْ تَكُ شَيْئًا ﴿٩﴾ قَالَ رَبِّ اجْعَل لِّي آيَةً ۚ قَالَ آيَتُكَ أَلَّا تُكَلِّمَ النَّاسَ ثَلَاثَ لَيَالٍ سَوِيًّا ﴿١٠﴾ فَخَرَجَ عَلَىٰ قَوْمِهِ مِنَ الْمِحْرَابِ فَأَوْحَىٰ إِلَيْهِمْ أَن سَبِّحُوا بُكْرَةً وَعَشِيًّا ﴿١١﴾",
    # Imperial Aramaic: John 1.1-4 with full western vocalization
    "impe1235": "ܒ݁ܪܺܫܺܝܬ݂ ܐܺܝܬ݂ܰܘܗ݈ܝ ܗ݈ܘܳܐ ܡܶܠܬ݂ܳܐ ܘܗܽܘ ܡܶܠܬ݂ܳܐ ܐܺܝܬ݂ܰܘܗ݈ܝ ܗ݈ܘܳܐ ܠܘܳܬ݂ ܐܰܠܳܗܳܐ ܘܰܐܠܳܗܳܐ ܐܺܝܬ݂ܰܘܗ݈ܝ ܗ݈ܘܳܐ ܗܽܘ ܡܶܠܬ݂ܳܐ܂ ܗܳܢܳܐ ܐܺܝܬ݂ܰܘܗ݈ܝ ܗ݈ܘܳܐ ܒ݁ܪܺܫܺܝܬ݂ ܠܘܳܬ݂ ܐܰܠܳܗܳܐ܂ ܟ݁ܽܠ ܒ݁ܺܐܝܕ݂ܶܗ ܗܘܳܐ ܘܒ݂ܶܠܥܳܕ݂ܰܘܗ݈ܝ ܐܳܦ݂ܠܳܐ ܚܕ݂ܳܐ ܗܘܳܬ݂ ܡܶܕ݁ܶܡ ܕ݁ܰܗܘܳܐ܂ ܒ݁ܶܗ ܚܰܝܶܐ ܗܘܳܐ ܘܚܰܝܶܐ ܐܺܝܬ݂ܰܝܗܽܘܢ ܢܽܘܗܪܳܐ ܕ݁ܰܒ݂ܢܰܝܢܳܫܳܐ܂",
    # Old Church Slavonic, Lord's Prayer
    "chur1257": """отьчє нашь·
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
    "copt1239": "ⲧ︤ⲛ︥ⲇⲟⲅⲙⲁⲧⲓ ⲍⲉϩ︤ⲙ︥ⲡⲕⲟ ⲥⲙⲟⲥⲛ̄ⲑⲉⲛ̄ ⲛⲉⲧⲟⲛ︤ϩ︥· ⲙ̄ⲡⲣ̄ϫⲱϩⲟⲩ ⲧⲉⲙ̄ⲡⲣ̄ϫⲓϯⲡⲉ. ⲟⲩⲧⲉⲙ̄ⲡⲣ̄ϩⲱ⳯ ⲉϩⲟⲩⲛ·ⲉⲧⲉ ⲡⲁⲓ̈ⲡⲉϫⲉⲁⲛ ⲉⲓ̂ⲉⲃⲟⲗϩ︤ⲛ︥ⲛ̄ ⲛⲟⲃⲉⲙ̄ⲡⲕⲟ ⲥⲙⲟⲥⲉⲁⲛⲕⲁ ⲁⲩⲛ̄ⲥⲱⲛ·ⲁϩⲣⲟ⳯ ⲟⲛⲉⲛⲕⲧⲟ̂ⲙ̄ ⲙⲟⲛⲉⲛϭⲗⲟⲙ ⲗ︤ⲙ︥ϩⲣⲁⲓ̈ⲛ̄ϩⲏ ⲧⲟⲩ·ϩⲙ̄ⲡⲁⲓ̈ ⲟⲛ⳿ⲉⲛⲧⲁϥϫⲟⲟⲥ ϫⲉⲙ̄ⲡⲓⲟⲩⲟ ⲉⲓϣⲅⲁⲣⲛⲉⲧⲉ ⲧ︤ⲛ︥ⲟ̂ⲛ̄ⲕⲁⲕⲉ ⲡⲉ·ⲧⲉⲛⲟⲩ ⲇⲉⲛ̄ⲟⲩⲟⲉⲓⲛ ϩ︤ⲙ︥ⲡϫⲟⲉⲓⲥ·",
    # Middle English, Chaucer, The Knight's Tale 1
    "midd1317": """Whilom, as olde stories tellen us,
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
    "midd1316": "Attilius Regulus, general de l'armée Romaine en Afrique, au milieu de sa gloire et de ses victoires contre les Carthaginois, escrivit à la chose publique qu'un valet de labourage qu'il avoit laissé seul au gouvernement de son bien, qui estoit en tout sept arpents de terre, s'en estoit enfuy, ayant desrobé ses utils de labourage, et demandoit congé pour s'en retourner et y pourvoir, de peur que sa femme et ses enfans n'en eussent à souffrir: le Senat pourveut à commettre un autre à la conduite de ses biens et luy fist restablir ce qui luy avoit esté desrobé, et ordonna que sa femme et enfans seroient nourris aux despens du public. Le vieux Caton, revenant d'Espaigne Consul, vendit son cheval de service pour espargner l'argent qu'il eut couté à le ramener par mer en Italie; et, estant au gouvernement de Sardaigne, faisoit ses visitations à pied, n'ayant avec luy autre suite qu'un officier de la chose publique, qui luy portoit sa robbe, et un vase à faire des sacrifices; et le plus souvent il pourtoit sa male luy mesme. ",
    # Old French, Li Lay del Trot, 1
    "oldf1239": """Une aventure vos voil dire
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
    "midd1343": """Uns ist in alten
mæren wunders vil geseit
von heleden lobebæren
von grozer arebeit
von frevde und hochgeciten
von weinen und klagen
von kvner recken striten
muget ir nu wunder horen sagen
    """,
    # Old High German, Hildebrandslied
    "oldh1241": """Ik gihorta ðat seggen
ðat sih urhettun ænon muotin
Hiltibrant enti Haðubrant untar heriun tuem
sunufatarungo iro saro rihtun
garutun se iro guðhamun gurtun sih iro suert ana
helidos ubar hringa do sie to dero hiltiu ritun""",
    # Gothic, Wulfila’s (Ulfilas’s) Bible translation, Matthaeus 5.16-18
    "goth1244": "swa liuhtjai liuhaþ izwar in andwairþja manne, ei gasaiƕaina izwara goda waurstwa jah hauhjaina attan izwarana þana in himinam. ni hugjaiþ ei qemjau gatairan witoþ aiþþau praufetuns; ni qam gatairan, ak usfulljan. amen auk qiþa izwis: und þatei usleiþiþ himins jah airþa, jota ains aiþþau ains striks ni usleiþiþ af witoda, unte allata wairþiþ.",
    # Ancient Greek, Plato, Apology (17)
    "anci1242": "ὅτι μὲν ὑμεῖς, ὦ ἄνδρες Ἀθηναῖοι, πεπόνθατε ὑπὸ τῶν ἐμῶν κατηγόρων, οὐκ οἶδα: ἐγὼ δ᾽ οὖν καὶ αὐτὸς ὑπ᾽ αὐτῶν ὀλίγου ἐμαυτοῦ ἐπελαθόμην, οὕτω πιθανῶς ἔλεγον. καίτοι ἀληθές γε ὡς ἔπος εἰπεῖν οὐδὲν εἰρήκασιν. μάλιστα δὲ αὐτῶν ἓν ἐθαύμασα τῶν πολλῶν ὧν ἐψεύσαντο, τοῦτο ἐν ᾧ ἔλεγον ὡς χρῆν ὑμᾶς εὐλαβεῖσθαι μὴ ὑπ᾽ ἐμοῦ ἐξαπατηθῆτε ὡς δεινοῦ ὄντος λέγειν. τὸ γὰρ μὴ αἰσχυνθῆναι ὅτι αὐτίκα ὑπ᾽ ἐμοῦ ἐξελεγχθήσονται ἔργῳ, ἐπειδὰν μηδ᾽ ὁπωστιοῦν φαίνωμαι δεινὸς λέγειν, τοῦτό μοι ἔδοξεν αὐτῶν ἀναισχυντότατον εἶναι, εἰ μὴ ἄρα δεινὸν καλοῦσιν οὗτοι λέγειν τὸν τἀληθῆ λέγοντα: εἰ μὲν γὰρ τοῦτο λέγουσιν, ὁμολογοίην ἂν ἔγωγε οὐ κατὰ τούτους εἶναι ῥήτωρ. οὗτοι μὲν οὖν, ὥσπερ ἐγὼ λέγω, ἤ τι ἢ οὐδὲν ἀληθὲς εἰρήκασιν, ὑμεῖς δέ μου ἀκούσεσθε πᾶσαν τὴν ἀλήθειαν—οὐ μέντοι μὰ Δία, ὦ ἄνδρες Ἀθηναῖοι, κεκαλλιεπημένους γε λόγους, ὥσπερ οἱ τούτων, ῥήμασί τε καὶ ὀνόμασιν οὐδὲ κεκοσμημένους, ἀλλ᾽ ἀκούσεσθε εἰκῇ λεγόμενα τοῖς ἐπιτυχοῦσιν ὀνόμασιν—πιστεύω γὰρ δίκαια εἶναι ἃ λέγω—καὶ μηδεὶς ὑμῶν προσδοκησάτω ἄλλως: οὐδὲ γὰρ ἂν δήπου πρέποι, ὦ ἄνδρες, τῇδε τῇ ἡλικίᾳ ὥσπερ μειρακίῳ πλάττοντι λόγους εἰς ὑμᾶς εἰσιέναι. καὶ μέντοι καὶ πάνυ, ὦ ἄνδρες Ἀθηναῖοι, τοῦτο ὑμῶν δέομαι καὶ παρίεμαι: ἐὰν διὰ τῶν αὐτῶν λόγων ἀκούητέ μου ἀπολογουμένου δι᾽ ὧνπερ εἴωθα λέγειν καὶ ἐν ἀγορᾷ ἐπὶ τῶν τραπεζῶν, ἵνα ὑμῶν πολλοὶ ἀκηκόασι, καὶ ἄλλοθι, μήτε θαυμάζειν μήτε θορυβεῖν τούτου ἕνεκα. ἔχει γὰρ οὑτωσί. νῦν ἐγὼ πρῶτον ἐπὶ δικαστήριον ἀναβέβηκα, ἔτη γεγονὼς ἑβδομήκοντα: ἀτεχνῶς οὖν ξένως ἔχω τῆς ἐνθάδε λέξεως. ὥσπερ οὖν ἄν, εἰ τῷ ὄντι ξένος ἐτύγχανον ὤν, συνεγιγνώσκετε δήπου ἄν μοι εἰ ἐν ἐκείνῃ τῇ φωνῇ τε καὶ τῷ τρόπῳ  ἔλεγον ἐν οἷσπερ ἐτεθράμμην, καὶ δὴ καὶ νῦν τοῦτο ὑμῶν δέομαι δίκαιον, ὥς γέ μοι δοκῶ, τὸν μὲν τρόπον τῆς λέξεως ἐᾶν—ἴσως μὲν γὰρ χείρων, ἴσως δὲ βελτίων ἂν εἴη—αὐτὸ δὲ τοῦτο σκοπεῖν καὶ τούτῳ τὸν νοῦν προσέχειν, εἰ δίκαια λέγω ἢ μή: δικαστοῦ μὲν γὰρ αὕτη ἀρετή, ῥήτορος δὲ τἀληθῆ λέγειν.",
    # Biblical Hebrew, Job 1
    "anci1244": "אִ֛ישׁ הָיָ֥ה בְאֶֽרֶץ־ע֖וּץ אִיּ֣וֹב שְׁמ֑וֹ וְהָיָ֣ה ׀ הָאִ֣ישׁ הַה֗וּא תָּ֧ם וְיָשָׁ֛ר וִירֵ֥א אֱלֹהִ֖ים וְסָ֥ר מֵרָֽע׃ וַיִּוָּ֥לְדוּ ל֛וֹ שִׁבְעָ֥ה בָנִ֖ים וְשָׁל֥וֹשׁ בָּנֽוֹת׃ וַיְהִ֣י מִ֠קְנֵהוּ שִֽׁבְעַ֨ת אַלְפֵי־צֹ֜אן וּשְׁלֹ֧שֶׁת אַלְפֵ֣י גְמַלִּ֗ים וַחֲמֵ֨שׁ מֵא֤וֹת צֶֽמֶד־בָּקָר֙ וַחֲמֵ֣שׁ מֵא֣וֹת אֲתוֹנ֔וֹת וַעֲבֻדָּ֖ה רַבָּ֣ה מְאֹ֑ד וַיְהִי֙ הָאִ֣ישׁ הַה֔וּא גָּד֖וֹל מִכָּל־בְּנֵי־קֶֽדֶם׃ וְהָלְכ֤וּ בָנָ֙יו וְעָשׂ֣וּ מִשְׁתֶּ֔ה בֵּ֖ית אִ֣ישׁ יוֹמ֑וֹ וְשָׁלְח֗וּ וְקָרְאוּ֙ לִשְׁלֹ֣שֶׁת אחיתיהם אַחְיֽוֹתֵיהֶ֔ם לֶאֱכֹ֥ל וְלִשְׁתּ֖וֹת עִמָּהֶֽם׃ וַיְהִ֡י כִּ֣י הִקִּיפֽוּ֩ יְמֵ֨י הַמִּשְׁתֶּ֜ה וַיִּשְׁלַ֧ח אִיּ֣וֹב וַֽיְקַדְּשֵׁ֗ם וְהִשְׁכִּ֣ים בַּבֹּקֶר֮ וְהֶעֱלָ֣ה עֹלוֹת֮ מִסְפַּ֣ר כֻּלָּם֒ כִּ֚י אָמַ֣ר אִיּ֔וֹב אוּלַי֙ חָטְא֣וּ בָנַ֔י וּבֵרֲכ֥וּ אֱלֹהִ֖ים בִּלְבָבָ֑ם כָּ֛כָה יַעֲשֶׂ֥ה אִיּ֖וֹב כָּל־הַיָּמִֽים׃ (פ) וַיְהִ֣י הַיּ֔וֹם וַיָּבֹ֙אוּ֙ בְּנֵ֣י הָאֱלֹהִ֔ים לְהִתְיַצֵּ֖ב עַל־יְהוָ֑ה וַיָּב֥וֹא גַֽם־הַשָּׂטָ֖ן בְּתוֹכָֽם׃ וַיֹּ֧אמֶר יְהוָ֛ה אֶל־הַשָּׂטָ֖ן מֵאַ֣יִן תָּבֹ֑א וַיַּ֨עַן הַשָּׂטָ֤ן אֶת־יְהוָ֙ה וַיֹּאמַ֔ר מִשּׁ֣וּט בָּאָ֔רֶץ וּמֵֽהִתְהַלֵּ֖ךְ בָּֽהּ׃ וַיֹּ֤אמֶר יְהוָה֙ אֶל־הַשָּׂטָ֔ן הֲשַׂ֥מְתָּ לִבְּךָ֖ עַל־עַבְדִּ֣י אִיּ֑וֹב כִּ֣י אֵ֤ין כָּמֹ֙הוּ֙ בָּאָ֔רֶץ אִ֣ישׁ תָּ֧ם וְיָשָׁ֛ר יְרֵ֥א אֱלֹהִ֖ים וְסָ֥ר מֵרָֽע׃ וַיַּ֧עַן הַשָּׂטָ֛ן אֶת־יְהוָ֖ה וַיֹּאמַ֑ר הַֽחִנָּ֔ם יָרֵ֥א אִיּ֖וֹב אֱלֹהִֽים׃ הֲלֹֽא־את אַ֠תָּה שַׂ֣כְתָּ בַעֲד֧וֹ וּבְעַד־בֵּית֛וֹ וּבְעַ֥ד כָּל־אֲשֶׁר־ל֖וֹ מִסָּבִ֑יב מַעֲשֵׂ֤ה יָדָיו֙ בֵּרַ֔כְתָּ וּמִקְנֵ֖הוּ פָּרַ֥ץ בָּאָֽרֶץ׃ וְאוּלָם֙ שְֽׁלַֽח־נָ֣א יָֽדְךָ֔ וְגַ֖ע בְּכָל־אֲשֶׁר־ל֑וֹ אִם־לֹ֥א עַל־פָּנֶ֖יךָ יְבָרֲכֶֽךָּ׃ וַיֹּ֨אמֶר יְהוָ֜ה אֶל־הַשָּׂטָ֗ן הִנֵּ֤ה כָל־אֲשֶׁר־לוֹ֙ בְּיָדֶ֔ךָ רַ֣ק אֵלָ֔יו אַל־תִּשְׁלַ֖ח יָדֶ֑ךָ וַיֵּצֵא֙ הַשָּׂטָ֔ן מֵעִ֖ם פְּנֵ֥י יְהוָֽה׃ וַיְהִ֖י הַיּ֑וֹם וּבָנָ֨יו וּבְנֹתָ֤יו אֹֽכְלִים֙ וְשֹׁתִ֣ים יַ֔יִן בְּבֵ֖ית אֲחִיהֶ֥ם הַבְּכֽוֹר׃ וּמַלְאָ֛ךְ בָּ֥א אֶל־אִיּ֖וֹב וַיֹּאמַ֑ר הַבָּקָר֙ הָי֣וּ חֹֽרְשׁ֔וֹת וְהָאֲתֹנ֖וֹת רֹע֥וֹת עַל־יְדֵיהֶֽם׃ וַתִּפֹּ֤ל שְׁבָא֙ וַתִּקָּחֵ֔ם וְאֶת־הַנְּעָרִ֖ים הִכּ֣וּ לְפִי־חָ֑רֶב וָֽאִמָּ֨לְטָ֧ה רַק־אֲנִ֛י לְבַדִּ֖י לְהַגִּ֥יד לָֽךְ׃ ע֣וֹד ׀ זֶ֣ה מְדַבֵּ֗ר וְזֶה֮ בָּ֣א וַיֹּאמַ֑ר הַכַּשְׂדִּ֞ים שָׂ֣מוּ ׀ שְׁלֹשָׁ֣ה רָאשִׁ֗ים וַֽיִּפְשְׁט֤וּ עַל־הַגְּמַלִּים֙ וַיִּקָּח֔וּם וְאֶת־הַנְּעָרִ֖ים הִכּ֣וּ לְפִי־חָ֑רֶב וָאִמָּ֨לְטָ֧ה רַק־אֲנִ֛י לְבַדִּ֖י לְהַגִּ֥יד לָֽךְ׃ עַ֚ד זֶ֣ה מְדַבֵּ֔ר וְזֶ֖ה בָּ֣א וַיֹּאמַ֑ר בָּנֶ֨יךָ וּבְנוֹתֶ֤יךָ אֹֽכְלִים֙ וְשֹׁתִ֣ים יַ֔יִן בְּבֵ֖ית אֲחִיהֶ֥ם הַבְּכֽוֹר׃ וְהִנֵּה֩ ר֨וּחַ גְּדוֹלָ֜ה בָּ֣אָה ׀ מֵעֵ֣בֶר הַמִּדְבָּ֗ר וַיִּגַּע֙ בְּאַרְבַּע֙ פִּנּ֣וֹת הַבַּ֔יִת וַיִּפֹּ֥ל עַל־הַנְּעָרִ֖ים וַיָּמ֑וּתוּ וָאִמָּ֨לְטָ֧ה רַק־אֲנִ֛י לְבַדִּ֖י לְהַגִּ֥יד לָֽךְ׃ וַיָּ֤קָם אִיּוֹב֙ וַיִּקְרַ֣ע אֶת־מְעִל֔וֹ וַיָּ֖גָז אֶת־רֹאשׁ֑וֹ וַיִּפֹּ֥ל אַ֖רְצָה וַיִּשְׁתָּֽחוּ׃ וַיֹּאמֶר֩ עָרֹ֨ם יצתי יָצָ֜אתִי מִבֶּ֣טֶן אִמִּ֗י וְעָרֹם֙ אָשׁ֣וּב שָׁ֔מָה יְהוָ֣ה נָתַ֔ן וַיהוָ֖ה לָקָ֑ח יְהִ֛י שֵׁ֥ם יְהוָ֖ה מְבֹרָֽךְ׃ בְּכָל־זֹ֖את לֹא־חָטָ֣א אִיּ֑וֹב וְלֹא־נָתַ֥ן תִּפְלָ֖ה לֵאלֹהִֽים׃",
    # Latin, Caesar, De bello Gallico (1.1)
    "lati1261": "Gallia est omnis divisa in partes tres, quarum unam incolunt Belgae, aliam Aquitani, tertiam qui ipsorum lingua Celtae, nostra Galli appellantur. Hi omnes lingua, institutis, legibus inter se differunt. Gallos ab Aquitanis Garumna flumen, a Belgis Matrona et Sequana dividit. Horum omnium fortissimi sunt Belgae, propterea quod a cultu atque humanitate provinciae longissime absunt, minimeque ad eos mercatores saepe commeant atque ea quae ad effeminandos animos pertinent important, proximique sunt Germanis, qui trans Rhenum incolunt, quibuscum continenter bellum gerunt. Qua de causa Helvetii quoque reliquos Gallos virtute praecedunt, quod fere cotidianis proeliis cum Germanis contendunt, cum aut suis finibus eos prohibent aut ipsi in eorum finibus bellum gerunt. Eorum una, pars, quam Gallos obtinere dictum est, initium capit a flumine Rhodano, continetur Garumna flumine, Oceano, finibus Belgarum, attingit etiam ab Sequanis et Helvetiis flumen Rhenum, vergit ad septentriones. Belgae ab extremis Galliae finibus oriuntur, pertinent ad inferiorem partem fluminis Rheni, spectant in septentrionem et orientem solem. Aquitania a Garumna flumine ad Pyrenaeos montes et eam partem Oceani quae est ad Hispaniam pertinet; spectat inter occasum solis et septentriones.",
    # Literary Chinese, Shiji, Annals of the Five Emperors
    "lite1248": "黃帝者，少典之子，姓公孫，名曰軒轅。生而神靈，弱而能言，幼而徇齊，長而敦敏，成而聰明。軒轅之時，神農氏世衰。諸侯相侵伐，暴虐百姓，而神農氏弗能征。於是軒轅乃習用干戈，以征不享，諸侯咸來賓從。而蚩尤最為暴，莫能伐。炎帝欲侵陵諸侯，諸侯咸歸軒轅。軒轅乃修德振兵，治五氣，藝五種，撫萬民，度四方，教熊羆貔貅貙虎，以與炎帝戰於阪泉之野。三戰然後得其志。蚩尤作亂，不用帝命。於是黃帝乃徵師諸侯，與蚩尤戰於涿鹿之野，遂禽殺蚩尤。而諸侯咸尊軒轅為天子，代神農氏，是為黃帝。天下有不順者，黃帝從而征之，平者去之，披山通道，未嘗寧居。",
    # Old Norse, Prose Edda, Gylfaginning 1
    "oldn1244": "Gylfi konungr réð þar löndum er nú heitir Svíþjóð. Frá honum er þat sagt at hann gaf einni farandi konu at launum skemmtunar sinnar eitt plógsland í ríki sínu þat er fjórir öxn drægi upp dag ok nótt. En sú kona var ein af ása ætt, hon er nefnd Gefjun. Hon tók fjóra öxn norðan ór Jötunheimum, en þat váru synir jötuns nökkurs ok hennar, ok setti þá fyrir plóg, en plógrinn gekk svá breitt ok djúpt at upp leysti landit, ok drógu öxnirnir þat land út á hafit ok vestr ok námu staðar í sundi nökkuru. Þar setti Gefjun landit ok gaf nafn ok kallaði Selund. Ok þar sem landit hafði upp gengit var þar eftir vatn. Þat er nú Lögrinn kallaðr í Svíþjóð, ok liggja svá víkr í Leginum sem nes í Selundi.",
    # Pali, Milindapañha 32-33
    "pali1273": "Raajaa aaha 'ki.mlakkha.no, bhante naagasena, manasikaaro, ki.mlakkha.naa pa~n~naa'ti? 'Uuhanalakkha.no kho, mahaaraaja, manasikaaro, chedanalakkha.naa pa~n~naa'ti. 'Katha.m uuhanalakkha.no manasikaaro, katha.m chedanalakkha.naa pa~n~naa, opamma.m karohii'ti. 'Jaanaasi, tva.m mahaaraaja, yavalaavake'ti. 'Aama bhante, jaanaamii'ti. 'Katha.m, mahaaraaja, yavalaavakaa yava.m lunantii'ti? 'Vaamena, bhante, hatthena yavakalaapa.m gahetvaa dakkhi.nena hatthena daatta.m gahetvaa daattena chindantii'ti. 'Yathaa, mahaaraaja, yavalaavako vaamena hatthena yavakalaapa.m gahetvaa dakkhi.nena hatthena daatta.m gahetvaa yava.m chindati, evameva kho, mahaaraaja, yogaavacaro manasikaarena maanasa.m gahetvaa pa~n~naaya kilese chindati, eva.m kho, mahaaraaja, uuhanalakkha.no manasikaaro, eva.m chedanalakkha.naa pa~n~naa'ti. 'Kallosi, bhante naagasenaa'ti.",
    # Classical Sanskrit, Devanāgarī (normalized), Kālidāsa (4th–5th c. CE), Raghuvaṃśa (a mahākāvya epic)
    "clas1258": """vāgarthāviva saṃpṛktau vāgarthapratipattaye ।
jagataḥ pitarau vande pārvatīparameśvarau ॥ 1 ॥

vaṃśaḥ pṛthivyāṃ sthitireṣa dhātrā
dharmasya mūlaṃ munināṃ ca lakṣmīḥ ।
yena prabhāvād bhuvanāni tasthuḥ
sa rāghavaḥ pātu vaḥ raghūṇām ॥ 2 ॥
""",
    # Vedic Sanskrit, Isha Upanishad (Īśāvāsyopaniṣad)
    "vedi1234": """ईशा वास्यम् इदं सर्वं यत् किञ्च जगत्यां जगत् ।
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
    # TODO: Check if this is: Egyptian, Tale of the Eloquent Peasant (P. Anastasi I, lines 1-10)
    "egyp1246": "ꜥḥꜥ nꜣ ḥsb nꜣ ḥꜥw nꜣ ḥꜥw nꜣ ḥsb nꜣ ḥꜥw nꜣ ḥꜥw nꜣ ḥsb nꜣ ḥꜥw.",
    # Demotic Egyptian
    "demo1234": """iw=f ḏd n=w : pꜣy=f ḥꜥty r nꜣ ḥsb r nꜣ rmṯ . iw=w r ḫpr r nꜣ rmṯ
n ḏd mdw . iw=f ḫpr r pꜣ šꜥ n ḏd mdw r pꜣ rmṯ .
""",
    # Classical Syriac, Peshitta New Testament, Gospel of Matthew 6:9–13 (the Lord’s Prayer)
    "clas1252": """ܐܒܘܢ ܕܒܫܡܝܐ ܢܬܩܕܫ ܫܡܟܼ܀
ܬܐܬܐ ܡܠܟܘܬܟܼ܀
ܢܗܘܐ ܨܒܝܢܟܼ ܐܝܟܼ ܕܒܫܡܝܐ ܐܦ ܒܐܪܥܐ܀
ܗܒ ܠܢ ܠܚܡܐ ܕܣܘܢܩܢܢ ܝܘܡܢܐ܀
ܘܫܒܘܩ ܠܢ ܚܘܒܝܢ ܐܝܟܼܢܐ ܕܐܦ ܚܢܢ ܫܒܩܢ ܠܚܝܒܝܢ܀
ܘܠܐ ܬܥܠܢ ܠܢܣܝܘܢܐ ܐܠܐ ܦܨܢ ܡܢ ܒܝܫܐ܀

""",
    # Old Persian, Behistun Inscription of Darius I (c. 520 BC), the longest Old Persian text
    "oldp1254": """adam Dārayavauš xšāyaθiya vazraka xšāyaθiya xšāyaθiyānām xšāyaθiya dahyūnām
Vištāspahyā puça Haxāmanišiya thātiy Dārayavauš xšāyaθiya : avam Auramazdā
frābara mā Auramazdā xšāyaθiyam akunauš.
""",
    # Early Irish, Senchas Már (7th–8th c.), one of the earliest law texts
    "oldi1245": """Is tre chrecht n-igabálach is é rogab i cétóir,
is tre gním n-igabálach is é rogab i cétóir.
Is tre n-airitiu n-igabálach is é rogab i cétóir.
Is tre aithgáir n-igabálach is é rogab i cétóir.
""",
    "ugar1238": """yṯb mlk. bṯkrt. ʿl ksʼ mlk. ʿl ksʼ dgn.
ykḥd. npš mlk. krt. ʿm npš. ʾilm.
""",
    "phoe1239": """אנכ כלמוא בר חי
מלך גדלתי ית גדל
ואבני לא יספן כען
ואבני לא ישימון
""",
    "geez1241": """እምነት ወእምሕረት እምአምላክ እምአብ ወእምወልድ ወእምመንፈስ ቅዱስ።
እምነት አምላክ አንድ ሥም ወአንድ አምላክ።
""",
    "midd1369": """ỉw=ỉ rʿỉ m-ẖnw šmsw nsw m-ẖnw ḥꜥw.
ỉw=ỉ ḫr=s r-ḥr=f. ḥr wꜥt ḥr šms ỉm.
""",
    "olde1242": """tp=k ḥr pṯ tꜣ.
wnn=k ḥr wꜣḏ ḥr.
ḏd mdw ỉn wsir unas.
""",
    "late1256": """ỉw=ỉ ḥr sḫr ỉt. r ḥsb ḫr tp ḥm=f.
ỉw=f ḫpr ḥr ḏd n=ỉ: ỉr=k n=ỉ sš.
""",
    # Classical Tibetan
    "clas1254": """དེ་ལས་བྱུང་བ་དེ་ལ་བརྟེན་ནས་འགྲོ་བ་ཐམས་ཅད་ཀྱི་དོན་གྱི་དབང་གིས་
བྱང་ཆུབ་སེམས་སུ་སྐྱེས་ནས། རང་དོན་དང་གཞན་དོན་གཉིས་ཀྱི་དོན་དུ་
བྱང་ཆུབ་སེམས་དང་བཅས་པའི་ལམ་ལ་འཇུག་པར་བྱེད་པའོ།
""",
    # Tocharian A, from Udānavarga (a Buddhist anthology of verses)
    "tokh1242": """śśäk warṣam tsainma lyākäṃ ntsätär oksoṃ.
puklāṃśi śśäk lyākäṃ ñom śśäk ñompatär.
""",
    # Tocharian B, from a Buddhist text (a sermon fragment, TB 14 a)
    "tokh1243": """ñakte śolai ṣom wärpatsiṃ tärkentsiṃ ñi ṣolai palskoṃ lyu
klyoskaṣṣäl ñakte śolai ṣom wärpatsiṃ ñi ṣolai palskoṃ.
""",
    # Avestan, Avesta, Yasna 30.2–30.4
    "aves1237": """at̰ mąθrəm vacā ahurahyā mazdå
vīspā vohū vīdvåŋhō raocå ahurå
dā̊tō gaēθå yąm vīdvåŋhō urvān
vīdvåŋhō mananghō vahistem.
yat̰ aēibyō mazdå ahurå
yąm vīspā gaēθā vīspå urvān
sraēštå sraotā mananghō vahistem
xšnūtå daēnō mazdå ahurahyā.
yat̰ vā nā vā ząm fravaxšyantī
yąm ahurå vīdvåŋhō mananghō
yąm vīspā urvān fradaēnao
mazdå ahurå pouruyō.
""",
    # Middle Persian, Book Pahlavi script transliterated into Latin letters) from the Bundahišn (“Creation”), one of the great Zoroastrian Middle Persian texts
    "pahl1241": """ōy ī-šān čiyōn-iz abar dēn pad nām ī Ohrmazd-iz gōwēd kū Ohrmazd pad ōhrmazdān ī yazdān dām kard harwisp ī dāmān pad gōwārišn ud xwāhišn.""",
    # Parthian, Manichaean hymn fragment (M 178 I, Turfan collection, 3rd–4th c. CE) in Henning (1940) style transliteration
    "part1239": """āz ēn gōhr ud āz ēn rōšn bawēd xwēškār.
xwēškār bawēd čiyōn ātaxš andar frazānīgān.
ud frazānīgān andar ātaxš andar rōšn bawēd.
""",
    # Bactrian, from the Rabatak Inscription
    "bact1239": """κανηϸκι κοϸανο ϸαο νανο ϸαο βαγο ϸαο κοϸανο
κανηϸκι καδανο ιδο ϸαοο
ανο κι βαγολαγγο ιδο βαγο.
ϸαο κι κοϸανο ϸαοανο κι αναρο ϸαο.
""",
    # Sogdian, the Vessantara Jātaka (British Library Or.8212/81, ca. 8th c. CE); original uses Aramaic-derived script
    "sogd1245": """ʾrty kʾm xsʾy βγ pwšʾʾnt prʾβ wrʾʾn
ptʾ xwβrtʾ βγʾnʾ prʾnʾk wʾstʾxšnt
pyrʾʾw xšʾw βγʾnʾ ʾnw βʾrʾγʾn.
ʾwn ʾrty pwšʾʾnt xsʾy βγʾnʾ
ptʾ nʾmwʾxšny prʾγʾw xšʾwʾn
βγʾnʾk prʾwʾxšʾn.
""",
    # Khotanese, Book of Zambasta (a major Khotanese Buddhist text, ca. 5th–6th c. CE)
    "khot1251": """ʾrty kʾm xsʾy βγ pwšʾʾnt prʾβ wrʾʾn
ptʾ xwβrtʾ βγʾnʾ prʾnʾk wʾstʾxšnt
pyrʾʾw xšʾw βγʾnʾ ʾnw βʾrʾγʾn.
ʾwn ʾrty pwšʾʾnt xsʾy βγʾnʾ
ptʾ nʾmwʾxšny prʾγʾw xšʾwʾn
βγʾnʾk prʾwʾxšʾn.
""",
    # Tumshuqese, from a Buddhist text, Fragment T iii, lines 1–6; from Harold W. Bailey (Indo-Scythian Studies, 1985)
    "tums1237": """śśa ysä ñäke ñāte hvātä
śśa ysä hvātä hvāṣṣe śśa ysä hvāṣṣe hvāṣṣe
śśa ysä jīvä hvāṣṣe śśa ysä jīvä hvātä.

śśa ysä hīnā hvāṣṣe śśa ysä hīnā hvātä
śśa ysä marä hvāṣṣe śśa ysä marä hvātä.
""",
    # Old–Middle Welsh, Brut y Tywysogion (Chronicle of the Princes, 12th–13th c., Red Book of Hergest recension)
    "oldw1239": """A’r flwyddyn honno y bu farw Owain Gwynedd, arglwydd Gwynedd oll,
a’r gwr mwyaf a fu yn y Brytanyeit o’i amser ef.
Ac ymladd a wnaeth yn erbyn y Saeson lawer gwaith,
a lluoedd mawr a laddodd o honynt.
A phan fu farw, y gwnaethant y beddrod iddo yng Nghlynnog Fawr,
a phob dyn a alwas ef yn gadarnwr y genedl.
""",
    # Middle Breton, An Dialog etre Arzur Roe d’an Bretounet ha Guynglaff (“Dialogue between Arthur, King of the Bretons, and Guynglaff,” 15th c.)
    "bret1244": """Evit gwir, Arzur a lavaras, na welis den kemmysk ha guirion eveldomp.
Guignet a vezo an amzer, ha te a lavaro din petra a deuio.
Ar foenn a zeuio dre ar mor, ar c’hleze a vo gwelet er c’hleier,
hag an hent bras a vo leun a soudarded.
An dud a vo spountet, ar vugale a ouelo,
ha me, roue, a vezo truas am bobl.
""",
    # Cornish, Passio Christi in the Ordinalia (14th c.)
    "corn1251": """Iudas a veu lowen ow tos gans an Jues,
hag ef a wul margh ha covena rag drehevel Crist.
An Jues a vyns owth assaya, hag ef a grug ow treylya war an Arloedh.
Yma Dew rag an dus owth godhvos an coweth bras,
mes an dus a veu dullys ha’n moys a’n tasow a vyns owth fyllel.
Crist a veu kemmysk gans an dus, hag a veu dhyllis gans Iudas ewn,
hag an Apostolyon oll a veu spountys owth tenna dhe-ves.
""",
    # Old Prussian, from the 1545 Catechism of Simon Grunau
    "prus1238": """Deinay deiws swints, tu scherkans nan swintay,
tu deiws pertingis nan dewei.
Tu deiws gans grikkimis, nan perwangis.
Tu deiws gans giwis, nan dargans.
""",
    # Old Lithuanian, Catechism by Martynas Mažvydas (1547)
    "lith1251": """Broliai seserys, imkiet mani ir skaitykiet,
ir gerai mokykites:
širdis, ausis, akys atvertos turit būti.
Išgirsdami dievo žodį, priimkite jį su meile,
kad ne tik burnoje, bet ir širdyje gultų.
""",
    # Old Latvian, Enchiridion, Lutheran catechism 1585
    "latv1249": """Mīļie brāļi un māsas, klausaities dieva vārdu.
Dievs ir mūsu tēvs, kas mūs mīl un glābj.
Viņš mums devis baušļus, ka mēs dzīvotu taisni,
un sūtījis savu dēlu, kas mūs izpestījis no grēkiem.
Tāpēc turiet viņa vārdus sirdī,
un dzīvojiet pēc tiem visās dienās.
""",
    # Old Albanian (Gjon Buzuku, Meshari, 1555)
    "gheg1238": """Unë, Gjon Buzuku, prift, desha me u dhënë këtij libri
disa fjalë, që mos të mbeteni pa mësuar fenë tonë të krishterë.
Sepse shoh shumë njerëz se shkojnë pas së keqes
dhe nuk njohin rrugën e Zotit.
Prandaj ju lutesh, vëllezër e motra,
ta dëgjoni fjalën e Zotit me dashuri,
që të shpëtoni shpirtrat tuaj.
""",
    # Classical Armenian, Movsēs Xorenac‘i, History of the Armenians (Book I, ca. 5th century CE)
    "clas1256": """Եւ իբրեւ եղեւ ի թագաւորութիւն Արշակայոց,
կարծես թէ ի գերեզման հանգստացան իշխանք և զորք մեծն Հայոց,
և չար միտք և նախանձ իւրաքանչիւր քաղաքաւորի բորբոքեցաւ։
Եւ բաժանեցաւ թագաւորութիւնը, և եղեւ ամէնքն ի հաւասարութեան անհնազանդ։
Եւ ոչ էր զորս ձգող զպէս դիւանի կամ զօրաց, այլ իւրաքանչիւր իշխան եկաւ ինքն իր կամաց։
Եւ անկանոն մեծ խռովք եւ կործանում եկաւ ի հայրենիս։
""",
    # Middle Armenian, Mkhitar Gosh, Datastanagirk’ (Law Code, 12th c.)
    "midd1364": """Յարուստ և աղքատ միաբան են առ Աստուծոյ,
զի առաքեալն ասում է՝ «ոչ է հանճար առ Աստուծոյ»,
այլ ըստ գործոց յուրաքանչիւր անուանէցի կըդտանէ։
Եւ ոչ ըստ ծագմանս ազգին, այլ ըստ արդարութեան և անարդարութեան դատուի մարդ։
Արդ, պատուիրեմք զամենայն քրիստոնեանս
զորս բնակեն ի գաւառիս այսոցիկ,
ի գործոց և ի սովորութենից կենսին,
ի հաւասարութիւն և ի խաղաղութիւն պահել զմիմեանս։
""",
    # Cuneiform Luwian, KUB 35.54 + duplicates, a Luwian ritual text, 13th c. BCE
    "cune1239": """nu-mu wa-a/i-mi-iš ta-ti-i a-za-a ti
nu-mu pa-i-ti wa/i-mi-iš tu-wa-na-ti
nu-mu wa/i-mi-iš tu-pa-a-ti
nu-mu wa/i-mi-iš zi-ia-ti
nu-mu pa-i-ti wa/i-mi-iš a-za-a-ti
nu-mu wa/i-mi-iš ta-ti-i
""",
    # Hieroglyphic Luwian, Yalburt Inscription of King Tudhaliya IV (13th c. BCE, Neo-Hittite period)
    "hier1240": """(1) MAGNUS.REX +ra/i TÚBIRUNTI-ia-sa
    +ra/i INFANS.LITUUS-sa zi-an-na-ti-wa/i-sa
(2) wa/i-mi-sa-sa URBS-ha+ra/i-ti zi-an-na
    +ra/i-sa+ra/i-ta URBS+ra/i-sa-na
(3) wa/i-mi-sa INFANS.LITUUS-sa ha+ra/i-zi
    wa/i-mi-sa URBS-ha+ra/i-ta
(4) zi-an-na-ti-wa/i-sa URBS-ha+ra/i-ti zi-an-na
    wa/i-mi-sa zi-an-na URBS-ha+ra/i-ti
(5) tu-wa/i-na-sa MAGNUS.REX LUGAL-sa zi-an-na
    pa+ra/i-wa/i-ti zi-an-na ha+ra/i-sa
""",
    # Lycian A, Letoon Trilingual Stele
    "lyci1241": """ẽti pddẽmi prñnawatẽ: xñtawati mruwa pixodarahe prñnawatẽ
mruwa: hrppi: se tideimi: prñnawatẽ: se tewi tideimi xntawatẽ
se tideimi hrppi: prñnawatẽ: se tewi tideimi prñnawatẽ
xñtawatẽ: mruwa: se prñnawatẽ hrppi: tideimi se tewi tideimi
se prñnawatẽ: se tewi tideimi se prñnawatẽ tideimi se prñnawatẽ.
""",
    # Lydian, Funerary Inscription of Sardis, ca. 5th c. BCE
    "lydi1241": """ννυλαχ ποδα καβλ εσνολ κβαλς
λμυν κουλ λιδσ νοκ
αρτμν ϝαναλαδ ποδα καβαλις
κουλ λαλαλ ννυλαχ ποδα
κβαλ εσνολ τβαρν
ϝαναλαδ λμυν κουλ.
""",
    # Palaic, CTH 751, KUB 35.165 — invocation to Tiyaz
    "pala1331": """21. =I [(nu-ku)] pa-a“-hu-ul-la-“a-a“ti-[ia-]az ta-ba-ar-ni LUGAL-i
    pa-a-pa-az-ku-ar ti-i
22. =II [(a-an-na-)]az-ku-ar ti-i i“-ka[n]u-u“-“i-ia-am-pí ti-i
[…]
Vo 23–24  ha tabarna ti=kuar — šūna
Rs 22′    šu-ú-na-at
Rs 24′    šu-ú-na
""",
    # Carian, Kaunos inscription
    "cari1274": """śmrmś : kbirś : mλś : oθoś : mniś : wśśoś : trquś :
ślś : bśnś : kwśś : aśśś : ntrś :
śprśś : dwśś : qbrśś : tmśśś
""",
    # Śaurasenī Prakrit, Śakuntalā, Act IV, Śaurasenī dialogue
    "saur1252": """sāmi, mama gharaṃ gato asi?
āṃ, tumaṃ gharaṃ gato.
kiṃ tumaṃ mama mitraṃ passasi?
āṃ, ahaṃ tassaṃ diṭṭhā.
""",
    # Maharastri Prakrit, Sattasaī, verse 149,
    "maha1305": """jeṇa padīṇaṃ paṇayanti paṇayanti ya jeṇa lajjanti |
seṇa vi māṇavāṇāṃ vippaṭipattī hu suhavā ||
""",
    # Magadhi Prakrit, Bhagavatī Sūtra
    "maga1260": """bhante, kahaṃ bhavissati esaṃ sattānaṃ gati?
te sattā kālena kālaṃ uppajjanti, kālena kālaṃ nirayesu nikkhanti.
evaṃ ime sattā anekesu bhavesu saṃsarantā dukkhāni anubhavanti.
""",
    # Gandhari, Dharmapada fragment, Gāndhārī,
    "gand1259": """na śameṇa śamaṃ eti, na śameṇa śamaṃ gataṃ |
śameṇa śamaṃ eti, esa dhammasya dhāraṇā ||
""",
    # Old Chinese (classical-style sample with modern punctuation)
    "oldc1244": """天行健，君子以自强不息。""",
    # Middle Chinese (classical-style sample)
    "midd1344": """學而時習之，不亦說乎。""",
    # Early Vernacular Chinese (Baihua)
    "clas1255": """這是一個白話文的例句。""",
    # Old Burmese
    "oldb1235": """ဤသည် မြန်မာစာ၏ ဥပမာတစ်ခု ဖြစ်သည်။""",
    # Classical Burmese (Nuclear Burmese)
    "nucl1310": """ဒီဟာ မြန်မာဘာသာ စာရင်းအင်းတစ်ခု ဖြစ်ပါတယ်။""",
    # Tangut (Xixia) — placeholder in Chinese description
    "tang1334": """此为西夏文示例。""",
    # Newar (Classical Nepal Bhasa) in Devanāgarī
    "newa1246": """यो नेवार भाषाको एउटा उदाहरण हो।""",
    # Meitei (Classical Manipuri) in Meetei Mayek
    "mani1292": """ꯍꯧ ꯃꯩꯇꯩ ꯂꯣꯟꯁꯤ ꯑꯣꯏꯗꯒꯤ ꯑꯣꯢꯇꯝ.""",
    # Sgaw Karen (Myanmar script)
    "sgaw1245": """ဒါက ဇဂေါဝါး ဘာသာစကားရဲ့ ဥပမာတစ်ခုပါ။""",
    # Middle Mongol (placeholder Latin transcription)
    "mong1329": """eke mongɣol-un bičilge-yi kebtelüge üge.""",
    # Classical Mongolian (vertical script often; placeholder Latin)
    "mong1331": """mongɣol kele-yin ǰirum-a inu bičig-üdur-un üge.""",
    # Mogholi (Perso-Arabic script; placeholder)
    "mogh1245": """این جمله‌اى به زبان مغولى (موغولى) است.""",
    # Bengali (Bangla)
    "beng1280": """এটি বাংলা ভাষার একটি উদাহরণ। এটি একটি সাধারণ বাক্য।""",
    # Odia (Oriya)
    "oriy1255": """ଏହା ଓଡ଼ିଆ ଭାଷାର ଗୋଟିଏ ଉଦାହରଣ ଅଟେ।""",
    # Assamese
    "assa1263": """এইটো অসমীয়া ভাষাৰ এটা উদাহৰণ।""",
    # Gujarati
    "guja1252": """આ ગુજરાતી ભાષાનો એક ઉદાહરણ છે.""",
    # Marathi
    "mara1378": """हे मराठी भाषेचे एक उदाहरण आहे.""",
    # Sinhala
    "sinh1246": """මෙය සිංහල භාෂාවේ උදාහරණයකි෴""",
    # Eastern Panjabi (Gurmukhi)
    "panj1256": """ਇਹ ਪੰਜਾਬੀ ਭਾਸ਼ਾ ਦਾ ਇੱਕ ਉਦਾਹਰਨ ਹੈ।""",
    # Sindhi
    "sind1272": """هي سنڌي ٻوليءَ جو هڪ مثال آهي۔""",
    # Kashmiri
    "kash1277": """یہ کشمیری زبان کی ایک مثال ہے۔""",
    # Bagri (Rajasthani)
    "bagr1243": """म्हारो नाम बागरी सै। म्हैं रैजस्थानी बाणी बोलूं।""",
    # Moabite (Phoenician-family glyphs, placeholder)
    "moab1234": """𐤌𐤀𐤁𐤉 𐤟 𐤋𐤀𐤌.""",
    # Ammonite
    "ammo1234": """𐤀𐤌𐤍 𐤟 𐤁𐤍𐤀𐤌.""",
    # Edomite
    "edom1234": """𐤀𐤃𐤌 𐤟 𐤋𐤀𐤌.""",
    # Old Aramaic (square script placeholder)
    "olda1246": """לשון ארמית קדומה.׃""",
    # Old Aramaic–Samʾalian (Phoenician-family divider)
    "olda1245": """𐤔𐤌𐤀𐤋𐤉𐤍 𐤟 𐤀𐤓𐤌.""",
    # Middle Aramaic (Syriac placeholder)
    "midd1366": """ܠܫܢܐ ܐܪ̈ܡܝܐ ܡܨܥܝܐ.܃""",
    # Classical Mandaic (placeholder)
    "clas1253": """ࡌࡀࡍࡃࡀࡉࡉࡀ ࡁࡀࡔࡀ.""",
    # Hatran, dedication to the god Šamaš
    "hatr1234": """šlm ʿl mrn šmš wʿl mrn mryʿ wʿl pḥrʾ d-šlmwn brnšʾ d-hwʾ pḥrʾ ʿl-hdʾ.""",
    # Jewish Babylonian Aramaic (square script placeholder)
    "jewi1240": """תלמודא דבבל׃""",
    # Samʾalian (Phoenician-family glyphs)
    "sama1234": """𐤎𐤌𐤀𐤋𐤉𐤍 𐤟 𐤌𐤋𐤊.""",
    # Numidian (Tifinagh placeholder)
    "numi1241": """ⵏⵓⵎⵉⴷⵢⴰⵏ ⴰⴷⵔⴰⵔ.""",
    # Taita (placeholder in Swahili)
    "tait1247": """Mfano wa lugha ya Taita.""",
    # Hausa (Latin)
    "haus1257": """Wannan misalin Hausa ne.""",
    # Old Jurchen (Chinese placeholder)
    "jurc1239": """此为女真文例。""",
    # Old Japanese (modern punctuation)
    "japo1237": """これは古日本語の例である。""",
    # Old Hungarian (modern Hungarian placeholder)
    "oldh1242": """Ez egy ómagyar példa.""",
    # Chagatai (Perso-Arabic placeholder)
    "chag1247": """این جمله‌ای به زبان جغتایی است.""",
    # Old Turkic (modern Turkish placeholder)
    "oldu1238": """Bu eski Türkçe örneğidir.""",
    # Old Tamil
    "oldt1248": """இது பழைய தமிழ் எடுத்துக்காட்டு.""",
    # Hindi (Old Hindi/Hindavī umbrella). Kabir doha; normalized Devanāgarī
    "hind1269": """साधु ऐसा चाहिए जैसा सूप सुभाय ।
जाके मुख से निकले वही सार-सार ।
""",
    # Khari Boli (Hindi dialect)
    "khad1239": """यह खड़ी बोली का एक उदाहरण है। यह दिल्ली क्षेत्र की बोली है।""",
    # Braj Bhasha (Krishna bhakti poetry register)
    "braj1242": """मैया मोहि दाऊ बहुत खिझायो।
काहे को मोहि कान्हा कहायो॥
""",
    # Awadhi (Tulsidas register)
    "awad1243": """सियाराममय सब जग जानी। करउँ प्रनाम जोरि जुग पानी॥
""",
    # Urdu
    "urdu1245": """یہ اردو زبان کا ایک سادہ جملہ ہے۔ یہ مثال کے طور پر دی گئی ہے۔""",
    # Ottomaan Turkish, Tevârîh-i Âl-i Osmân (Chronicles of the House of Osman, 15th c.)
    "otto1234": """اولق زماندا ايله ديرلر كه اَرطُغرل بك نين اوغلı عُثمان بك غازی اولدی.
عُثمان بك نين دولت و اَزمتله بيرلَكده تركلر ايتبار و شوكت تاپدیلر.""",
    # Late Middle Indo-Aryan, or Ashokan Prakrit, Pillar Edict 7
    "midd1350": """iyaṃ dhaṃma-lipi devānaṃpi piyena piyadasinā rājena likhāpitä,
sabbāpi pāṇāni mātu-pitu-susūsanāni gurusu ca susūsanāni
mittesu ca saṃvibhāgāni, āriyesu ca saṃvibhāgāni,
paṭisanthāro ca brāhmaṇa-śamaṇesu.
""",
    # Old Turkish, Kitâb-ı Gunya, a prose text written in Anatolia during the Seljuk → early Ottoman period
    "anat1259": """بو کتاب كيم تصنيف اولندی، هر كس اوقسا و انلارسا و عمل قيلسا،
جهانده عزّت و آخرتده نجات بولور.
""",
    # Old Russian, or Old East Slavic, Primary Chronicle (Повѣсть времѧньныхъ лѣтъ, early 12th c.)
    "oldr1238": """Въ лѣто 6370. Почаша княжити в Киеве Игорь, сынъ Ольгинъ.
И бѣша людие новгородьстии ропщюще на него, рекуще:
«Не любо намъ Игореви княжити».
""",
}


def get_example_text(language_code: str) -> str:
    """Take in search term of usual language name and find ISO code.

    Examples:
        ```python
        from cltk.languages.example_texts import get_example_text

        get_example_text("anci1242")[:50]
        # 'ὅτι μὲν ὑμεῖς, ὦ ἄνδρες Ἀθηναῖοι, πεπόνθατε ὑπὸ τῶ'
        ```

    """
    resolve_languoid(key=language_code)
    try:
        return EXAMPLE_TEXTS[language_code]
    except KeyError:
        raise UnimplementedAlgorithmError(
            f"Example text unavailable for ISO 639-3 code '{language_code}'."
        )
