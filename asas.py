#!/usr/bin/python3.5

import pandas as pd
import matplotlib.pyplot as plt
import lombscargle
import os
import catalogs
import phase_adjustments
from matplotlib.ticker import FormatStrFormatter


def main():
	'''info goes here'''

	path = './00'
	filelist = sorted(os.listdir(path))
	os.chdir(path)	
	
	for file in filelist:
		proceed = catalogs.check_vsx(file)
		if proceed == False:
			print('The object is already classified')
			print('')
			continue
		
		head = ['HJD', 'MAG_3', 'MAG_0', 'MAG_1', 'MAG_2', 'MAG_4', 'MER_3', \
			    'MER_0', 'MER_1', 'MER_2', 'MER_4', 'GRADE', 'FRAME']
		
		data = pd.read_csv(file, names=head, header=None, comment='#', sep='\s+')

		filtered = data[data.GRADE == 'A']
		
		sliced = filtered[['HJD', 'MAG_3']]
		sliced = sliced.rename(columns={'MAG_3':'mag'})
		
		plt.scatter(filtered['HJD'], sliced['mag'])
		plt.gca().invert_yaxis()
		plt.title('RAW DATA ' + file)
		plt.xlabel('HJD')
		plt.ylabel('mag')
		plt.show()

		freq, folded_df = lombscargle.find_freq(sliced, file)
		
		epoch, zeroed = phase_adjustments.set_min_to_zero(folded_df)
		# print(zeroed)
		period = round(1 / freq, 4)
	
		# plot final phase diagram
		fig, ax = plt.subplots()
		ax.yaxis.set_major_formatter(FormatStrFormatter('%0.2f'))
		plt.scatter(zeroed['Phase'], zeroed['mag'], color='black', s=5)
		plt.gca().invert_yaxis()
		plt.ylabel('Ic-mag')
		plt.xlabel('Phase')
		plt.title(file + ' (P = ' + str(period) + ' d)')
		plt.grid()
		plt_name = file + '_Phase_Diagram'
		# plt.savefig(plt_name)
		plt.show()

		exit = input("Enter [1] to continue or any other key to exit ").strip()
		print('')
		if exit != '1':
			break


if __name__ == '__main__':
	main()
