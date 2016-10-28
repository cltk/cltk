
"""Sankskrit stopwords.
Further explanations at: https://gist.github.com/Akhilesh28/b012159a10a642ed5c34e551db76f236
"""

__author__ = 'Akhilesh S. Chobey <akhileshchobey03@gmail.com>'

STOPS_LIST = ['अहम्',
              'आवाम्',
              'वयम्',
              'माम्',
              'मा',
              'आवाम्',
              'अस्मान्',
              'नः',
              'मया',
              'आवाभ्याम्',
              'अस्माभिस्',
              'मह्यम्',
              'मे',
              'आवाभ्याम्',
              'नौ',
              'अस्मभ्यम्',
              'नः',
              'मत्',
              'आवाभ्याम्',
              'अस्मत्',
              'मम',
              'मे',
              'आवयोः',
              'अस्माकम्',
              'नः',
              'मयि',
              'आवयोः',
              'अस्मासु',
              'त्वम्',
              'युवाम्',
              'यूयम्',
              'त्वाम्',
              'त्वा',
              'युवाम्',
              'वाम्',
              'युष्मान्',
              'वः',
              'त्वया',
              'युवाभ्याम्',
              'युष्माभिः',
              'तुभ्यम्',
              'ते',
              'युवाभ्याम्',
              'वाम्',
              'युष्मभ्यम्',
              'वः',
              'त्वत्',
              'युवाभ्याम्',
              'युष्मत्',
              'तव',
              'ते',
              'युवयोः',
              'वाम्',
              'युष्माकम्',
              'वः',
              'त्वयि',
              'युवयोः',
              'युष्मासु',
              'सः',
              'तौ',
              'ते',
              'तम्',
              'तौ',
              'तान्',
              'तेन',
              'ताभ्याम्',
              'तैः',
              'तस्मै',
              'ताभ्याम्',
              'तेभ्यः',
              'तस्मात्',
              'ताभ्याम्',
              'तेभ्यः',
              'तस्य',
              'तयोः',
              'तेषाम्',
              'तस्मिन्',
              'तयोः',
              'तेषु',
              'सा',
              'ते',
              'ताः',
              'ताम्',
              'ते',
              'ताः',
              'तया',
              'ताभ्याम्',
              'ताभिः',
              'तस्यै',
              'ताभ्याम्',
              'ताभ्यः',
              'तस्याः',
              'ताभ्याम्',
              'ताभ्यः',
              'तस्य',
              'तयोः',
              'तासाम्',
              'तस्याम्',
              'तयोः',
              'तासु',
              'तत्',
              'ते',
              'तानि',
              'तत्',
              'ते',
              'तानि',
              'तया',
              'ताभ्याम्',
              'ताभिः',
              'तस्यै',
              'ताभ्याम्',
              'ताभ्यः',
              'तस्याः',
              'ताभ्याम्',
              'ताभ्यः',
              'तस्य',
              'तयोः',
              'तासाम्',
              'तस्याम्',
              'तयोः',
              'तासु',
              'अयम्',
              'इमौ',
              'इमे',
              'इमम्',
              'इमौ',
              'इमान्',
              'अनेन',
              'आभ्याम्',
              'एभिः',
              'अस्मै',
              'आभ्याम्',
              'एभ्यः',
              'अस्मात्',
              'आभ्याम्',
              'एभ्यः',
              'अस्य',
              'अनयोः',
              'एषाम्',
              'अस्मिन्',
              'अनयोः',
              'एषु',
              'इयम्',
              'इमे',
              'इमाः',
              'इमाम्',
              'इमे',
              'इमाः',
              'अनया',
              'आभ्याम्',
              'आभिः',
              'अस्यै',
              'आभ्याम्',
              'आभ्यः',
              'अस्याः',
              'आभ्याम्',
              'आभ्यः',
              'अस्याः',
              'अनयोः',
              'आसाम्',
              'अस्याम्',
              'अनयोः',
              'आसु',
              'इदम्',
              'इमे',
              'इमानि',
              'इदम्',
              'इमे',
              'इमानि',
              'अनेन',
              'आभ्याम्',
              'एभिः',
              'अस्मै',
              'आभ्याम्',
              'एभ्यः',
              'अस्मात्',
              'आभ्याम्',
              'एभ्यः',
              'अस्य',
              'अनयोः',
              'एषाम्',
              'अस्मिन्',
              'अनयोः',
              'एषु',
              'एषः',
              'एतौ',
              'एते',
              'एतम्',
              'एनम्',
              'एतौ',
              'एनौ',
              'एतान्',
              'एनान्',
              'एतेन',
              'एताभ्याम्',
              'एतैः',
              'एतस्मै',
              'एताभ्याम्',
              'एतेभ्यः',
              'एतस्मात्',
              'एताभ्याम्',
              'एतेभ्यः',
              'एतस्य',
              'एतस्मिन्',
              'एतेषाम्',
              'एतस्मिन्',
              'एतस्मिन्',
              'एतेषु',
              'एषा',
              'एते',
              'एताः',
              'एताम्',
              'एनाम्',
              'एते',
              'एने',
              'एताः',
              'एनाः',
              'एतया',
              'एनया',
              'एताभ्याम्',
              'एताभिः',
              'एतस्यै',
              'एताभ्याम्',
              'एताभ्यः',
              'एतस्याः',
              'एताभ्याम्',
              'एताभ्यः',
              'एतस्याः',
              'एतयोः',
              'एनयोः',
              'एतासाम्',
              'एतस्याम्',
              'एतयोः',
              'एनयोः',
              'एतासु',
              'एतत्',
              'एतद्',
              'एते',
              'एतानि',
              'एतत्',
              'एतद्',
              'एनत्',
              'एनद्',
              'एते',
              'एने',
              'एतानि',
              'एनानि',
              'एतेन',
              'एनेन',
              'एताभ्याम्',
              'एतैः',
              'एतस्मै',
              'एताभ्याम्',
              'एतेभ्यः',
              'एतस्मात्',
              'एताभ्याम्',
              'एतेभ्यः',
              'एतस्य',
              'एतयोः',
              'एनयोः',
              'एतेषाम्',
              'एतस्मिन्',
              'एतयोः',
              'एनयोः',
              'एतेषु',
              'असौ',
              'अमू',
              'अमी',
              'अमूम्',
              'अमू',
              'अमून्',
              'अमुना',
              'अमूभ्याम्',
              'अमीभिः',
              'अमुष्मै',
              'अमूभ्याम्',
              'अमीभ्यः',
              'अमुष्मात्',
              'अमूभ्याम्',
              'अमीभ्यः',
              'अमुष्य',
              'अमुयोः',
              'अमीषाम्',
              'अमुष्मिन्',
              'अमुयोः',
              'अमीषु',
              'असौ',
              'अमू',
              'अमूः',
              'अमूम्',
              'अमू',
              'अमूः',
              'अमुया',
              'अमूभ्याम्',
              'अमूभिः',
              'अमुष्यै',
              'अमूभ्याम्',
              'अमूभ्यः',
              'अमुष्याः',
              'अमूभ्याम्',
              'अमूभ्यः',
              'अमुष्याः',
              'अमुयोः',
              'अमूषाम्',
              'अमुष्याम्',
              'अमुयोः',
              'अमूषु',
              'अमु',
              'अमुनी',
              'अमूनि',
              'अमु',
              'अमुनी',
              'अमूनि',
              'अमुना',
              'अमूभ्याम्',
              'अमीभिः',
              'अमुष्मै',
              'अमूभ्याम्',
              'अमीभ्यः',
              'अमुष्मात्',
              'अमूभ्याम्',
              'अमीभ्यः',
              'अमुष्य',
              'अमुयोः',
              'अमीषाम्',
              'अमुष्मिन्',
              'अमुयोः',
              'अमीषु',
              'कः',
              'कौ',
              'के',
              'कम्',
              'कौ',
              'कान्',
              'केन',
              'काभ्याम्',
              'कैः',
              'कस्मै',
              'काभ्याम्',
              'केभ्य',
              'कस्मात्',
              'काभ्याम्',
              'केभ्य',
              'कस्य',
              'कयोः',
              'केषाम्',
              'कस्मिन्',
              'कयोः',
              'केषु',
              'का',
              'के',
              'काः',
              'काम्',
              'के',
              'काः',
              'कया',
              'काभ्याम्',
              'काभिः',
              'कस्यै',
              'काभ्याम्',
              'काभ्यः',
              'कस्याः',
              'काभ्याम्',
              'काभ्यः',
              'कस्याः',
              'कयोः',
              'कासाम्',
              'कस्याम्',
              'कयोः',
              'कासु',
              'किम्',
              'के',
              'कानि',
              'किम्',
              'के',
              'कानि',
              'केन',
              'काभ्याम्',
              'कैः',
              'कस्मै',
              'काभ्याम्',
              'केभ्य',
              'कस्मात्',
              'काभ्याम्',
              'केभ्य',
              'कस्य',
              'कयोः',
              'केषाम्',
              'कस्मिन्',
              'कयोः',
              'केषु',
              'भवान्',
              'भवन्तौ',
              'भवन्तः',
              'भवन्तम्',
              'भवन्तौ',
              'भवतः',
              'भवता',
              'भवद्भ्याम्',
              'भवद्भिः',
              'भवते',
              'भवद्भ्याम्',
              'भवद्भ्यः',
              'भवतः',
              'भवद्भ्याम्',
              'भवद्भ्यः',
              'भवतः',
              'भवतोः',
              'भवताम्',
              'भवति',
              'भवतोः',
              'भवत्सु',
              'भवती',
              'भवत्यौ',
              'भवत्यः',
              'भवतीम्',
              'भवत्यौ',
              'भवतीः',
              'भवत्या',
              'भवतीभ्याम्',
              'भवतीभिः',
              'भवत्यै',
              'भवतीभ्याम्',
              'भवतीभिः',
              'भवत्याः',
              'भवतीभ्याम्',
              'भवतीभिः',
              'भवत्याः',
              'भवत्योः',
              'भवतीनाम्',
              'भवत्याम्',
              'भवत्योः',
              'भवतीषु',
              'भवत्',
              'भवती',
              'भवन्ति',
              'भवत्',
              'भवती',
              'भवन्ति',
              'भवता',
              'भवद्भ्याम्',
              'भवद्भिः',
              'भवते',
              'भवद्भ्याम्',
              'भवद्भ्यः',
              'भवतः',
              'भवद्भ्याम्',
              'भवद्भ्यः',
              'भवतः',
              'भवतोः',
              'भवताम्',
              'भवति',
              'भवतोः',
              'भवत्सु',
              'अये',
              'अरे',
              'अरेरे',
              'अविधा',
              'असाधुना',
              'अस्तोभ',
              'अहह',
              'अहावस्',
              'आम्',
              'आर्यहलम्',
              'आह',
              'आहो',
              'इस्',
              'उम्',
              'उवे',
              'काम्',
              'कुम्',
              'चमत्',
              'टसत्',
              'दृन्',
              'धिक्',
              'पाट्',
              'फत्',
              'फाट्',
              'फुडुत्',
              'बत',
              'बाल्',
              'वट्',
              'व्यवस्तोभति',
              'व्यवस्तुभ्',
              'षाट्',
              'स्तोभ',
              'हुम्मा',
              'हूम्',
              'अति',
              'अधि',
              'अनु',
              'अप',
              'अपि',
              'अभि',
              'अव',
              'आ',
              'उद्',
              'उप',
              'नि',
              'निर्',
              'परा',
              'परि',
              'प्र',
              'प्रति',
              'वि',
              'सम्',
              'अथवा',
              'उत',
              'अन्यथा',
              'इव',
              'च',
              'चेत्',
              'यदि',
              'तु',
              'परन्तु',
              'यतः',
              'करणेन',
              'हि',
              'यतस्',
              'यदर्थम्',
              'यदर्थे',
              'यर्हि',
              'यथा',
              'यत्कारणम्',
              'येन',
              'ही',
              'हिन',
              'यथा',
              'यतस्',
              'यद्यपि',
              'यात्',
              'अवधेस्',
              'यावति',
              'येन प्रकारेण',
              'स्थाने',
              'अह',
              'एव',
              'एवम्',
              'कच्चित्',
              'कु',
              'कुवित्',
              'कूपत्',
              'च',
              'चण्',
              'चेत्',
              'तत्र',
              'नकिम्',
              'नह',
              'नुनम्',
              'नेत्',
              'भूयस्',
              'मकिम्',
              'मकिर्',
              'यत्र',
              'युगपत्',
              'वा',
              'शश्वत्',
              'सूपत्',
              'ह',
              'हन्त',
              'हि']
