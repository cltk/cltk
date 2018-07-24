greek_sub_patterns = [
    ('(ων|οντος|οντι|οντα|ον|ουσα|ούσης|ούσῃ|ούσης|ουσαν)$', r'\1ω'),
    ('(ό)(εις|εντος|εντι|εντα)$', r'\1εις'),
    ]


greek_pps = {
#    'abluo': [3, 'ablu', 'abluere', 'ablu', 'ablut'],
}

### Regexps for Latin verb endings; default patterns for use with PPLemmatizer
### Todo: Refactor to be more compact

#pia_patterns = [(r'(\w*)o\b', 1),
#                (r'(\w*)[a|e|i]?s\b', 1),
#                (r'(\w*)[a|e|i]?t\b', 1),
#                (r'(\w*)[a|e|i]?mus\b', 1),
#                (r'(\w*)[a|e|i]?tis\b', 1),
#                (r'(\w*)[a|e|u]nt\b', 1)]


#latin_verb_patterns = fpfa_patterns + ppfa_patterns + pfia_patterns + iia_patterns + fia_patterns + pia_patterns + pip_patterns + iip_patterns + psa_patterns + isa_patterns + isp_patterns + pfsa_patterns + ppfsa_patterns
