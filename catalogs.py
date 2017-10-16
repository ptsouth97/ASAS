#!/usr/bin/python3.5

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def main():
	file = '000006+2553.2'
	check_vsx(file)


def check_vsx(filename) -> object:
	'''info goes here'''

	'''os.chdir('./00')
	info = pd.read_csv(filename)
	
	item1 = str(info.iloc[2])
	ra = item1[22:30]
	
	item2 = str(info.iloc[3])
	dec = item2[21:31]
	

	print(ra + dec)	'''

	ra1 = int(filename[0:2])
	ra2 = int(filename[2:4])
	ra3 = int(filename[4:6])
	ra  = round(ra1 + ra2/60 + ra3/3600, 6)

	dec1 = int(filename[6:9])
	dec2 = float(filename[9:])
	dec = round(dec1 + dec2/60, 6)
	
	lat = filename[6]
	
	coords = str(ra) + lat + str(dec)
	print('The coordinates are ' + coords)  

	url = 'http://www.aavso.org/vsx/index.php?view=results.get&format=d&order=9&coords=' + coords
	print('Checking coordinates in VSX...')
	print('')
	r = requests.get(url)
	html_doc = r.text
	soup = BeautifulSoup(html_doc, 'lxml')
	table = soup.find_all('table')[10]
	
	all_tr = table.find_all('tr')
	first_entry = all_tr[2]
	results = first_entry.get_text().lstrip(' ')
	dist = float(results[3:7])
	id = results[11:37].strip()
	
	if results[3:8] == 'There':
		print('No nearby objects were found')
	else:
		print('The VSX object {} is located {} arcmin from the coordinates you entered'.format(id, dist))
	print('')

	if dist > 2:
		answer = True
	else:
		answer = False

	return answer
	


if __name__ == '__main__':
	main()
