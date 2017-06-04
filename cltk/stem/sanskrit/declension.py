"""
program to convert data from Inria's declension engine to a list of tuples 
"""

import sys
import urllib.request
from bs4 import BeautifulSoup

def declension(stem, gender): #gender can be Mas,Fem,Neu
	decl = []

	req = urllib.request.Request('http://sanskrit.inria.fr/cgi-bin/SKT/sktdeclin?lex=SH&q='+stem+'&t=VH&g='+gender+'&font=roma')
	with urllib.request.urlopen(req) as response:
		html = response.read()

	soup = BeautifulSoup(html, "lxml")
	table = soup.find("table", class_="inflexion")
	tags = table.find_all("span", class_="red")
	words = [t.string for t in tags]

	for i in range(int(len(words)/3)):
		tup = (words[3*i], words[3*i+1], words[3*i+2])
		decl.append(tup)

	return decl

if __name__ == '__main__':
	stem = sys.argv[1]; gender = sys.argv[2]
	for tup in declension(stem, gender):
		print(tup)
