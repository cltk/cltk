"""The Oscan alphabet. Sources:

- `<https://www.unicode.org/charts/PDF/U10300.pdf>`
-  Buck, C. A Grammar of Oscan and Umbrian.

"""

__author__ = ["Caio Geraldes <caio.geraldes@usp.br>"]


VOWELS = [
    "\U00010300",  # 𐌀 OSCAN LETTER A
    "\U00010304",  # 𐌄 OSCAN LETTER E
    "\U00010309",  # 𐌉 OSCAN LETTER I
    "\U00010316",  # 𐌖 OSCAN LETTER U
    "\U0001031D",  # 𐌝 OSCAN LETTER II
    "\U0001031E",  # 𐌞 OSCAN LETTER UU
]

CONSONANTS = [
    "\U00010301",  # 𐌁 OSCAN LETTER B
    "\U00010302",  # 𐌂 OSCAN LETTER K/G
    "\U00010303",  # 𐌃 OSCAN LETTER D
    "\U00010305",  # 𐌅 OSCAN LETTER V
    "\U00010307",  # 𐌇 OSCAN LETTER H
    "\U0001030A",  # 𐌊 OSCAN LETTER K
    "\U0001030B",  # 𐌋 OSCAN LETTER L
    "\U0001030C",  # 𐌌 OSCAN LETTER M
    "\U0001030D",  # 𐌍 OSCAN LETTER N
    "\U00010310",  # 𐌐 OSCAN LETTER P
    "\U00010314",  # 𐌔 OSCAN LETTER S
    "\U00010315",  # 𐌕 OSCAN LETTER T
    "\U0001031A",  # 𐌚 OSCAN LETTER F
]
