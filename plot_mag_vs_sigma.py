
import matplotlib.pyplot as plt
import numpy as np
import datalib as dl

data = dl.read_dat('evaluation.csv',',')

f, plots = plt.subplots(5, sharey=True)

dwarf_flags = dl.get_column(data,1)
kepmags = dl.get_column(data,3)
sigmas = []
for sigma in range(4,9):
	sigmas.append(dl.get_column(data,sigma))

for i in range(1,len(dl.get_column(data,0))):
	for seg in range(4,9):
		is_dwarf = dwarf_flags[i]
		if is_dwarf == '1.0':
			symbol = 'd'
		elif is_dwarf == '0.0':
			symbol = 'o'
		else:
			symbol = 'x'

		if sigma != 'nan' and kepmags[i] != 'nan':
			plots[seg-4].scatter(float(kepmags[i]),np.log10(float(sigmas[seg-4][i])),marker=symbol)

plt.show()
