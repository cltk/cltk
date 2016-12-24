# https://en.wikipedia.org/wiki/Greek_diacritics#Unicode
# https://unicode-table.com/en/blocks/greek-coptic/
# https://unicode-table.com/en/blocks/greek-extended/

#Upper Case Vowels
UPPER = [#
    '\u0391',# Α Greek Capital Letter Alpha
    '\u0395', # Ε Greek Capital Letter Epsilon
    '\u0397', # Η Greek Capital Letter Eta
    '\u0399', # Ι Greek Capital Letter Iota
    '\u039f', # Ο Greek Capital Letter Omicron
    '\u03a5', # Υ Greek Capital Letter Upsilon
    '\u03a9', # Ω Greek Capital Letter Omega
    '\u1fbc', # ᾼ Greek Capital Letter Alpha with Prosgegrammeni
    '\u1fcc', # ῌ Greek Capital Letter Eta with Prosgegrammeni
    '\u1ffc' # ῼ Greek Capital Letter Omega with Prosgegrammeni
]

UPPER_ACUTE = [#
    '\u0386', # Ά Greek Capital Letter Alpha with Tonos
    '\u0388', # Έ Greek Capital Letter Epsilon with Tonos
    '\u0389', # Ή Greek Capital Letter Eta with Tonos
    '\u038a', # Ί Greek Capital Letter Iota with Tonos
    '\u038c', # Ό Greek Capital Letter Omicron with Tonos
    '\u038e', # Ύ Greek Capital Letter Upsilon with Tonos
    '\u038f' # Ώ Greek Capital Letter Omega with Tonos
]

UPPER_GRAVE = [
    '\u1fba', # Ὰ Greek Capital Letter Alpha with Varia
    '\u1fc8', # Ὲ Greek Capital Letter Epsilon with Varia
    '\u1fca', # Ὴ Greek Capital Letter Eta with Varia
    '\u1fda', # Ὶ Greek Capital Letter Iota with Varia
    '\u1ff8', # Ὸ Greek Capital Letter Omicron with Varia
    '\u1fea', # Ὺ Greek Capital Letter Upsilon with Varia
    '\u1ffa' # Ὼ Greek Capital Letter Omega with Varia
]


UPPER_SMOOTH = [#
    '\u1f08', # Ἀ Greek Capital Letter Alpha with Psili
    '\u1f18', # Ἐ Greek Capital Letter Epsilon with Psili
    '\u1f28', # Ἠ Greek Capital Letter Eta with Psili
    '\u1f38', # Ἰ Greek Capital Letter Iota with Psili
    '\u1f48', # Ὀ Greek Capital Letter Omicron with Psili
    '\u1f68', # Ὠ Greek Capital Letter Omega with Psili
    '\u1f88', # ᾈ Greek Capital Letter Alpha with Psili and Prosgegrammeni
    '\u1f98', # ᾘ Greek Capital Letter Eta with Psili and Prosgegrammeni
    '\u1fa8' # ᾨ Greek Capital Letter Omega with Psili and Prosgegrammeni
]

UPPER_SMOOTH_ACUTE = [
    '\u1f0c', # Ἄ Greek Capital Letter Alpha with Psili and Oxia
    '\u1f1c', # Ἔ Greek Capital Letter Epsilon with Psili and Oxia
    '\u1f2c', # Ἤ Greek Capital Letter Eta with Psili and Oxia
    '\u1f3c', # Ἴ Greek Capital Letter Iota with Psili and Oxia
    '\u1fc4', # Ὄ Greek Capital Letter Omicron with Psili and Oxia
    '\u1f6c', # Ὤ Greek Capital Letter Omega with Psili and Oxia
    '\u1f8c', # ᾌ Greek Capital Letter Alpha with Psili and Oxia and Prosgegrammeni
    '\u1f9c', #  ᾜ Greek Capital Letter Eta with Psili and Oxia and Prosgegrammeni
    '\u1fac' # ᾬ Greek Capital Letter Omega with Psili and Oxia and Prosgegrammeni
]

UPPER_SMOOTH_GRAVE = [#
    '\u1f0a', # Ἂ Greek Capital Letter Alpha with Psili and Varia
    '\u1f1a', # Ἒ Greek Capital Letter Epsilon with Psili and Varia
    '\u1f2a', # Ἢ Greek Capital Letter Eta with Psili and Varia
    '\u1f3a', # Ἲ Greek Capital Letter Iota with Psili and Varia
    '\u1f4a', # Ὂ Greek Capital Letter Omicron with Psili and Varia
    '\u1f6a', # Ὢ Greek Capital Letter Omega With Psili And Varia
    '\u1f8a', # ᾊ Greek Capital Letter Alpha With Psili And Varia And Prosgegrammeni
    '\u1f9a', # ᾚ Greek Capital Letter Eta With Psili And Varia And Prosgegrammeni
    '\u1faa' # ᾪ Greek Capital Letter Omega With Psili And Varia And Prosgegrammeni
]
UPPER_SMOOTH_CIRCUMFLEX = [#
'\u1f0e', # Ἆ Greek Capital Letter Alpha With Psili And Perispomeni
'\u1f2e', # Ἦ Greek Capital Letter Eta With Psili And Perispomeni
'\u1f3e', # Ἶ Greek Capital Letter Iota With Psili And Perispomeni
'\u1f6e', # Ὦ Greek Capital Letter Omega With Psili And Perispomeni
'\u1f8e', # ᾎ Greek Capital Letter Alpha With Psili And Perispomeni And Prosgegrammeni
'\u1f9e', # ᾞ Greek Capital Letter Eta With Psili And Perispomeni And Prosgegrammeni
'\u1fae' # ᾮ Greek Capital Letter Omega With Psili And Perispomeni And Prosgegrammeni
]

UPPER_ROUGH = [#
'\u1f09', # Ἁ Greek Capital Letter Alpha With Dasia
'\u1f19', # Ἑ Greek Capital Letter Epsilon With Dasia
'\u1f29', # Ἡ Greek Capital Letter Eta With Dasia
'\u1f39', # Ἱ Greek Capital Letter Iota With Dasia
'\u1f49', # Ὁ Greek Capital Letter Omicron With Dasia
'\u1f59', # Ὑ Greek Capital Letter Upsilon With Dasia
'\u1f69', # Ὡ Greek Capital Letter Omega With Dasia
'\u1f89', # ᾉ Greek Capital Letter Alpha With Dasia And Prosgegrammeni
'\u1f99', # ᾙ Greek Capital Letter Eta With Dasia And Prosgegrammeni
'\u1fa9' # ᾩ Greek Capital Letter Omega With Dasia And Prosgegrammeni
]

UPPER_ROUGH_ACUTE = [#
'\u1f0d', # Ἅ Greek Capital Letter Alpha With Dasia And Oxia
'\u1f1d', # Ἕ Greek Capital Letter Epsilon With Dasia And Oxia
'\u1f2d', # Ἥ Greek Capital Letter Eta With Dasia And Oxia
'\u1f3d', # Ἵ Greek Capital Letter Iota With Dasia And Oxia
'\u1f4d', # Ὅ Greek Capital Letter Omicron With Dasia And Oxia
'\u1f5d', # Ὕ Greek Capital Letter Upsilon With Dasia And Oxia
'\u1f6d', # Ὥ Greek Capital Letter Omega With Dasia And Oxia
'\u1f8d', # ᾍ Greek Capital Letter Alpha With Dasia And Oxia And Prosgegrammeni
'\u1f9d', # ᾝ Greek Capital Letter Eta With Dasia And Oxia And Prosgegrammeni
'\u1fad' # ᾭ Greek Capital Letter Omega With Dasia And Oxia And Prosgegrammeni
]

UPPER_ROUGH_GRAVE = [#
'\u1f0b', # Ἃ Greek Capital Letter Alpha With Dasia And Varia
'\u1f1b', # Ἓ Greek Capital Letter Epsilon With Dasia And Varia
'\u1f2b', # Ἣ Greek Capital Letter Eta With Dasia And Varia
'\u1f3b', # Ἳ Greek Capital Letter Iota With Dasia And Varia
'\u1f4b', # Ὃ Greek Capital Letter Omicron With Dasia And Varia
'\u1f5b', # Ὓ Greek Capital Letter Upsilon With Dasia And Varia
'\u1f6b', # Ὣ Greek Capital Letter Omega With Dasia And Varia
'\u1f8b', # ᾋ Greek Capital Letter Alpha With Dasia And Varia And Prosgegrammeni
'\u1f9b', # ᾛ Greek Capital Letter Eta With Dasia And Varia And Prosgegrammeni
'\u1fab' # ᾫ Greek Capital Letter Omega With Dasia And Varia And Prosgegrammeni
]

UPPER_ROUGH_CIRCUMFLEX = [#
'\u1f0f', # Ἇ Greek Capital Letter Alpha With Dasia And Perispomeni
'\u1f2f', # Ἧ Greek Capital Letter Eta With Dasia And Perispomeni
'\u1f3f', # Ἷ Greek Capital Letter Iota With Dasia And Perispomeni
'\u1f5f', # Ὗ Greek Capital Letter Upsilon With Dasia And Perispomeni
'\u1f6f', # Ὧ Greek Capital Letter Omega With Dasia And Perispomeni
'\u1f8f', # ᾏ Greek Capital Letter Alpha With Dasia And Perispomeni And Prosgegrammeni
'\u1f9f', # ᾟ Greek Capital Letter Eta With Dasia And Perispomeni And Prosgegrammeni
'\u1faf' # ᾯ Greek Capital Letter Omega With Dasia And Perispomeni And Prosgegrammeni
]

UPPER_DIAERESIS = [#
'\u03aa', # Ϊ Greek Capital Letter Iota With Dialytika
'\u03ab' # Ϋ Greek Capital Letter Upsilon With Dialytika
]

UPPER_DIAERESIS = [#
'\u03aa', # Ϊ Greek Capital Letter Iota With Dialytika
'\u03ab' # Ϋ Greek Capital Letter Upsilon With Dialytika
]

UPPER_MACRON = [#
'\u1fb9', # Ᾱ Greek Capital Letter Alpha With Macron
'\u1fd9', # Ῑ Greek Capital Letter Iota With Macron
'\u1fe9' # Ῡ Greek Capital Letter Upsilon With Macron
]

UPPER_BREVE = [#
'\u1fb8', # Ᾰ Greek Capital Letter Alpha With Vrachy
'\u1fd8', # Ῐ Greek Capital Letter Iota With Vrachy
'\u1fe8' # Ῠ Greek Capital Letter Upsilon With Vrachy
]

# Lower Case Vowels

LOWER = [#
'\u03b1', # α Greek Small Letter Alpha
'\u03b5', # ε Greek Small Letter Epsilon
'\u03b7', # η Greek Small Letter Eta
'\u03b9', # ι Greek Small Letter Iota
'\u03bf', # ο Greek Small Letter Omicron
'\u03c5', # υ Greek Small Letter Upsilon
'\u03c9', # ω Greek Small Letter Omega
'\u1fb3', # ᾳ Greek Small Letter Alpha With Ypogegrammeni
'\u1fc3', # ῃ Greek Small Letter Eta With Ypogegrammeni
'\u1ff3' # ῳ Greek Small Letter Omega With Ypogegrammeni
]

LOWER_ACUTE = [#
'\u03ac', # ά Greek Small Letter Alpha With Tonos
'\u03ad', # έ Greek Small Letter Epsilon With Tonos
'\u03ae', # ή Greek Small Letter Eta With Tonos
'\u03af', # ί Greek Small Letter Iota With Tonos
'\u03cc', # ό Greek Small Letter Omicron With Tonos
'\u03cd', # ύ Greek Small Letter Upsilon With Tonos
'\u03ce', # ώ Greek Small Letter Omega With Tonos
'\u1fb4', # ᾴ Greek Small Letter Alpha With Oxia And Ypogegrammeni
'\u1fc4', # ῄ Greek Small Letter Eta With Oxia And Ypogegrammeni
'\u1ff4' # ῴ Greek Small Letter Omega With Oxia And Ypogegrammeni
]

LOWER_GRAVE = [#
'\u1f70', # ὰ Greek Small Letter Alpha With Varia
'\u1f72', # ὲ Greek Small Letter Epsilon With Varia
'\u1f74', # ὴ Greek Small Letter Eta With Varia
'\u1f76', # ὶ Greek Small Letter Iota With Varia
'\u1f78', # ὸ Greek Small Letter Omicron With Varia
'\u1f7a', # ὺ Greek Small Letter Upsilon With Varia
'\u1f7c', # ὼ Greek Small Letter Omega With Varia
'\u1fb2', # ᾲ Greek Small Letter Alpha With Varia And Ypogegrammeni
'\u1fc2', # ῂ Greek Small Letter Eta With Varia And Ypogegrammeni
'\u1ff2' # ῲ Greek Small Letter Omega With Varia And Ypogegrammeni
]

LOWER_CIRCUMFLEX = [#
'\u1fb6', # ᾶ Greek Small Letter Alpha With Perispomeni
'\u1fc6', # ῆ Greek Small Letter Eta With Perispomeni
'\u1fd6', # ῖ Greek Small Letter Iota With Perispomeni
'\u1fe6', # ῦ Greek Small Letter Upsilon With Perispomeni
'\u1ff6', # ῶ Greek Small Letter Omega With Perispomeni
'\u1fb7', # ᾷ Greek Small Letter Alpha With Perispomeni And Ypogegrammeni
'\u1fc7', # ῇ Greek Small Letter Eta With Perispomeni And Ypogegrammeni
'\u1ff7' # ῷ Greek Small Letter Omega With Perispomeni And Ypogegrammeni
]

LOWER_SMOOTH = [#
'\u1f00', # ἀ Greek Small Letter Alpha With Psili
'\u1f10', # ἐ Greek Small Letter Epsilon With Psili
'\u1f20', # ἠ Greek Small Letter Eta With Psili
'\u1f30', # ἰ Greek Small Letter Iota With Psili
'\u1f40', # ὀ Greek Small Letter Omicron With Psili
'\u1f50', # ὐ Greek Small Letter Upsilon With Psili
'\u1f60', # ὠ Greek Small Letter Omega With Psili
'\u1f80', # ᾀ Greek Small Letter Alpha With Psili And Ypogegrammeni
'\u1f90', # ᾐ Greek Small Letter Eta With Psili And Ypogegrammeni
'\u1fa0', # ᾠ Greek Small Letter Omega With Psili And Ypogegrammeni
'\u1fe4' # ῤ Greek Small Letter Rho With Psili
]

LOWER_SMOOTH_ACUTE = [#
'\u1f04', # ἄ Greek Small Letter Alpha With Psili And Oxia
'\u1f14', # ἔ Greek Small Letter Epsilon With Psili And Oxia
'\u1f24', # ἤ Greek Small Letter Eta With Psili And Oxia
'\u1f34', # ἴ Greek Small Letter Iota With Psili And Oxia
'\u1f44', # ὄ Greek Small Letter Omicron With Psili And Oxia
'\u1f54', # ὔ Greek Small Letter Upsilon With Psili And Oxia
'\u1f64', # ὤ Greek Small Letter Omega With Psili And Oxia
'\u1f84', # ᾄ Greek Small Letter Alpha With Psili And Oxia And Ypogegrammeni
'\u1f94', # ᾔ Greek Small Letter Eta With Psili And Oxia And Ypogegrammeni
'\u1fa4' # ᾤ Greek Small Letter Omega With Psili And Oxia And Ypogegrammeni
]

LOWER_SMOOTH_GRAVE = [#
'\u1f02', # ἂ Greek Small Letter Alpha With Psili And Varia
'\u1f12', # ἒ Greek Small Letter Epsilon With Psili And Varia
'\u1f22', # ἢ Greek Small Letter Eta With Psili And Varia
'\u1f32', # ἲ Greek Small Letter Iota With Psili And Varia
'\u1f42', # ὂ Greek Small Letter Omicron With Psili And Varia
'\u1f52', # ὒ Greek Small Letter Upsilon With Psili And Varia
'\u1f62', # ὢ Greek Small Letter Omega With Psili And Varia
'\u1f82', # ᾂ Greek Small Letter Alpha With Psili And Varia And Ypogegrammeni
'\u1f92', # ᾒ Greek Small Letter Eta With Psili And Varia And Ypogegrammeni
'\u1fa2' # ᾢ Greek Small Letter Omega With Psili And Varia And Ypogegrammeni
]

LOWER_SMOOTH_CIRCUMFLEX = [#
'\u1f06', # ἆ Greek Small Letter Alpha With Psili And Perispomeni
'\u1f26', # ἦ Greek Small Letter Eta With Psili And Perispomeni
'\u1f36', # ἶ Greek Small Letter Iota With Psili And Perispomeni
'\u1f56', # ὖ Greek Small Letter Upsilon With Psili And Perispomeni
'\u1f66', # ὦ Greek Small Letter Omega With Psili And Perispomeni
'\u1f86', # ᾆ Greek Small Letter Alpha With Psili And Perispomeni And Ypogegrammeni
'\u1f96', # ᾖ Greek Small Letter Eta With Psili And Perispomeni And Ypogegrammeni
'\u1fa6' # ᾦ Greek Small Letter Omega With Psili And Perispomeni And Ypogegrammeni
]

LOWER_ROUGH = [#
'\u1f01', # ἁ Greek Small Letter Alpha With Dasia
'\u1f11', # ἑ Greek Small Letter Epsilon With Dasia
'\u1f21', # ἡ Greek Small Letter Eta With Dasia
'\u1f31', # ἱ Greek Small Letter Iota With Dasia
'\u1f41', # ὁ Greek Small Letter Omicron With Dasia
'\u1f51', # ὑ Greek Small Letter Upsilon With Dasia
'\u1f61', # ὡ Greek Small Letter Omega With Dasia
'\u1f81', # ᾁ Greek Small Letter Alpha With Dasia And Ypogegrammeni
'\u1f91', # ᾑ Greek Small Letter Eta With Dasia And Ypogegrammeni
'\u1fa1', # ᾡ Greek Small Letter Omega With Dasia And Ypogegrammeni
'\u1fe5' # ῥ Greek Small Letter Rho With Dasia
]

LOWER_ROUGH_ACUTE = [#
'\u1f05', # ἅ Greek Small Letter Alpha With Dasia And Oxia
'\u1f15', # ἕ Greek Small Letter Epsilon With Dasia And Oxia
'\u1f25', # ἥ Greek Small Letter Eta With Dasia And Oxia
'\u1f35', # ἵ Greek Small Letter Iota With Dasia And Oxia
'\u1f45', # ὅ Greek Small Letter Omicron With Dasia And Oxia
'\u1f55', # ὕ Greek Small Letter Upsilon With Dasia And Oxia
'\u1f65', # ὥ Greek Small Letter Omega With Dasia And Oxia
'\u1f85', # ᾅ Greek Small Letter Alpha With Dasia And Oxia And Ypogegrammeni
'\u1f95', # ᾕ Greek Small Letter Eta With Dasia And Oxia And Ypogegrammeni
'\u1fa5' # ᾥ Greek Small Letter Omega With Dasia And Oxia And Ypogegrammeni
]

LOWER_ROUGH_GRAVE = [#
'\u1f03', # ἃ Greek Small Letter Alpha With Dasia And Varia
'\u1f13', # ἓ Greek Small Letter Epsilon With Dasia And Varia
'\u1f23', # ἣ Greek Small Letter Eta With Dasia And Varia
'\u1f33', # ἳ Greek Small Letter Iota With Dasia And Varia
'\u1f43', # ὃ Greek Small Letter Omicron With Dasia And Varia
'\u1f53', # ὓ Greek Small Letter Upsilon With Dasia And Varia
'\u1f63', # ὣ Greek Small Letter Omega With Dasia And Varia
'\u1f83', # ᾃ Greek Small Letter Alpha With Dasia And Varia And Ypogegrammeni
'\u1f93', # ᾓ Greek Small Letter Eta With Dasia And Varia And Ypogegrammeni
'\u1fa3' # ᾣ Greek Small Letter Omega With Dasia And Varia And Ypogegrammeni
]

LOWER_ROUGH_CIRCUMFLEX = [#
'\u1f07', # ἇ Greek Small Letter Alpha With Dasia And Perispomeni
'\u1f27', # ἧ Greek Small Letter Eta With Dasia And Perispomeni
'\u1f37', # ἷ Greek Small Letter Iota With Dasia And Perispomeni
'\u1f57', # ὗ Greek Small Letter Upsilon With Dasia And Perispomeni
'\u1f67', # ὧ Greek Small Letter Omega With Dasia And Perispomeni
'\u1f87', # ᾇ Greek Small Letter Alpha With Dasia And Perispomeni And Ypogegrammeni
'\u1f97', # ᾗ Greek Small Letter Eta With Dasia And Perispomeni And Ypogegrammeni
'\u1fa7' # ᾧ Greek Small Letter Omega With Dasia And Perispomeni And Ypogegrammeni
]

LOWER_DIAERESIS = [#
'\u03ca', # ϊ Greek Small Letter Iota With Dialytika
'\u03cb' # ϋ Greek Small Letter Upsilon With Dialytika
]

LOWER_DIAERESIS_ACUTE = [#
'\u0390', # ΐ Greek Small Letter Iota With Dialytika And Tonos
'\u03b0' # ΰ Greek Small Letter Upsilon With Dialytika And Tonos
]

LOWER_DIAERESIS_GRAVE = [#
'\u1f0e', # Ἆ Greek Capital Letter Alpha With Psili And Perispomeni
'\u1f2e', # Ἦ Greek Capital Letter Eta With Psili And Perispomeni
'\u1f3e', # Ἶ Greek Capital Letter Iota With Psili And Perispomeni
'\u1f6e', # Ὦ Greek Capital Letter Omega With Psili And Perispomeni
'\u1f8e', # ᾎ Greek Capital Letter Alpha With Psili And Perispomeni And Prosgegrammeni
'\u1f9e', # ᾞ Greek Capital Letter Eta With Psili And Perispomeni And Prosgegrammeni
'\u1fae' # ᾮ Greek Capital Letter Omega With Psili And Perispomeni And Prosgegrammeni
]

LOWER_DIAERESIS_CIRCUMFLEX = [#
'\u1f0e', # Ἆ Greek Capital Letter Alpha With Psili And Perispomeni
'\u1f2e', # Ἦ Greek Capital Letter Eta With Psili And Perispomeni
'\u1f3e', # Ἶ Greek Capital Letter Iota With Psili And Perispomeni
'\u1f6e', # Ὦ Greek Capital Letter Omega With Psili And Perispomeni
'\u1f8e', # ᾎ Greek Capital Letter Alpha With Psili And Perispomeni And Prosgegrammeni
'\u1f9e', # ᾞ Greek Capital Letter Eta With Psili And Perispomeni And Prosgegrammeni
'\u1fae' # ᾮ Greek Capital Letter Omega With Psili And Perispomeni And Prosgegrammeni
]

LOWER_MACRON = [#
'\u1fb1', # ᾱ Greek Small Letter Alpha With Macron
'\u1fd1', # ῑ Greek Small Letter Iota With Macron
'\u1fe1' # ῡ Greek Small Letter Upsilon With Macron
]

LOWER_BREVE = [#
'\u1fb0', # ᾰ Greek Small Letter Alpha With Vrachy
'\u1fd0', # ῐ Greek Small Letter Iota With Vrachy
'\u1fe0' # ῠ Greek Small Letter Upsilon With Vrachy
]

LOWER_RHO = '\u03c1' # ρ Greek Small Letter Rho

LOWER_RHO_SMOOTH = '\u1fe4' # ῤ Greek Small Letter Rho With Psili

LOWER_RHO_ROUGH = '\u1fe5' # ῥ Greek Small Letter Rho With Dasia


# Consonants --------------------------

UPPER_CONSONANTS = [#
'\u0392', # Β Greek Capital Letter Beta
'\u0393', # Γ Greek Capital Letter Gamma
'\u0394', # Δ Greek Capital Letter Delta
'\u0396', # Ζ Greek Capital Letter Zeta
'\u0398', # Θ Greek Capital Letter Theta
'\u039a', # Κ Greek Capital Letter Kappa
'\u039b', # Λ Greek Capital Letter Lamda
'\u039c', # Μ Greek Capital Letter Mu
'\u039d', # Ν Greek Capital Letter Nu
'\u039e', # Ξ Greek Capital Letter Xi
'\u03a0', # Π Greek Capital Letter Pi
'\u03a1', # Ρ Greek Capital Letter Rho
'\u03a3', # Σ Greek Capital Letter Sigma
'\u03a4', # Τ Greek Capital Letter Tau
'\u03a6', # Φ Greek Capital Letter Phi
'\u03a7', # Χ Greek Capital Letter Chi
'\u03a8', # Ψ Greek Capital Letter Psi
]

LOWER_CONSONANTS = [#
'\u03b2', # β Greek Small Letter Beta
'\u03b3', # γ Greek Small Letter Gamma
'\u03b4', # δ Greek Small Letter Delta
'\u03b6', # ζ Greek Small Letter Zeta
'\u03b8', # θ Greek Small Letter Theta
'\u03ba', # κ Greek Small Letter Kappa
'\u03bb', # λ Greek Small Letter Lamda
'\u03bc', # μ Greek Small Letter Mu
'\u03bd', # ν Greek Small Letter Nu
'\u03be', # ξ Greek Small Letter Xi
'\u03c0', # π Greek Small Letter Pi
'\u03c1', # ρ Greek Small Letter Rho
'\u03c3', # σ Greek Small Letter Sigma
'\u03c4', # τ Greek Small Letter Tau
'\u03d5', # ϕ Greek Phi Symbol
'\u03c7', # χ Greek Small Letter Chi
'\u03c8' # ψ Greek Small Letter Psi
]
