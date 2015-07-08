
import matplotlib.pyplot as plt
import numpy as np
import datalib as dl

def color_T(Teff):
	if Teff == 'nan' or Teff == '-1.0' or Teff == '1.0':
		return [0,0,0]
	Teff = float(Teff)
	return [1-(Teff-2265)/5375.0,0.0,(Teff-2265)/5375.0]

data = dl.read_dat('evaluation.csv',',')

f, plots = plt.subplots(5, sharex=True,sharey=True)

dwarf_flags = dl.get_column(data,1)
kepmags = dl.get_column(data,3)
Teffs = dl.get_column(data,2)
sigmas = []
for sigma in range(4,9):
	sigmas.append(dl.get_column(data,sigma))

length = len(dl.get_column(data,0))
for i in range(1,length):
	for seg in range(4,9):
		is_dwarf = dwarf_flags[i]
		if is_dwarf == '1.0':
			symbol = 'd'
		elif is_dwarf == '0.0':
			symbol = 'o'
		else:
			symbol = 'x'

		if sigma != 'nan' and kepmags[i] != 'nan': 
			plots[seg-4].scatter(float(kepmags[i]),np.log10(float(sigmas[seg-4][i])),marker=symbol,color = color_T(Teffs[i]))
		print int((i*100)/length) 
plt.show()
