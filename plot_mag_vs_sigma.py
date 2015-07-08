
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import datalib as dl
import astroML 
from astroML.plotting import setup_text_plots
setup_text_plots(fontsize=10, usetex=True)

def color_T(Teff):
	if Teff == 'nan' or Teff == '-1.0' or Teff == '1.0':
		return [0,0,0]
	Teff = float(Teff)
	x = (Teff-2265)/5375.0
	return [-x*x+1,-4*x*(x-1),-x*(x-2)]
def label_d(is_dwarf):
	if is_dwarf == '1.0':
		return 'Dwarf'
	elif is_dwarf == '0.0':
		symbol = 'Giant'
	else:
		symbol = 'Unkown'
data = dl.read_dat('evaluation.csv',',')

f,plots = plt.subplots(3,2, sharex=False,sharey=False)

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
			plots[np.ceil((seg-4)/2)][(seg-4)%2].set_ylabel('$\log{\sigma_' + str(seg-3) +'}$',fontsize=20)
			plots[np.ceil((seg-4)/2)][(seg-4)%2].tick_params(axis='both', which='major', labelsize=20)
			plots[np.ceil((seg-4)/2)][(seg-4)%2].grid(True)
			plots[np.ceil((seg-4)/2)][(seg-4)%2].set_xlim([8.25,17])
			plots[np.ceil((seg-4)/2)][(seg-4)%2].set_ylim([-4.5,0])
			plots[np.ceil((seg-4)/2)][(seg-4)%2].text(15.25,-0.5,'Segment ' + str(seg-3),fontsize=30)
		print int((i*100)/length)

plots[2][0].set_xlabel('Kepler band magnitude',fontsize=20)
plots[1][1].set_xlabel('Kepler band magnitude',fontsize=20)
f.delaxes(plots[2][1])		
f.set_size_inches(32,20)
f.savefig("sigma_vs_mag.png", dpi = 300)