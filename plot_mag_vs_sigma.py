
import matplotlib.pyplot as plt
import numpy as np
import datalib as dl

def color_T(Teff):
	if Teff == 'nan' or Teff == '-1.0' or Teff == '1.0':
		return [0,0,0]
	Teff = float(Teff)
	x = (Teff-2265)/5375.0
	return [-x*x+1,-4*x*(x-1),-x*(x-2)]

data = dl.read_dat('evaluation.csv',',')

f,plots = plt.subplots(3,2, sharex=True,sharey=True)

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
			plots[np.ceil((seg-4)/2)][(seg-4)%2].scatter(float(kepmags[i]),np.log10(float(sigmas[seg-4][i])),marker=symbol,color = color_T(Teffs[i]))
			plots[np.ceil((seg-4)/2)][(seg-4)%2].set_ylabel('$\log{\sigma_' + str(seg-3) +'}$')
			plots[np.ceil((seg-4)/2)][(seg-4)%2].set_xlabel('$Kepler \, band \, magnitude$')
		print int((i*100)/length) 
plt.show()
