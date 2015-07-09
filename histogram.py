import datalib as dl 
import numpy as np 
import matplotlib.pyplot as plt
from astroML.plotting import setup_text_plots
setup_text_plots(fontsize=10, usetex=True)


data = dl.read_dat('evaluation.csv',',')

f,plots = plt.subplots(3,2, sharex=False,sharey=False)

sigmas = []
for sigma in range(4,9):
	sigmas.append(dl.get_column(data,sigma))

for j in range(0,len(sigmas)):
	sigma = sigmas[j]
	good_sigmas = []
	for i in range(1,len(sigma)):
		if sigma[i] != 'nan':
			good_sigmas.append((float(sigma[i])))
	good_sigmas = np.sort(good_sigmas)
	good_sigmas = good_sigmas[0:int(0.9*len(good_sigmas))]
	hist = np.histogram(good_sigmas,bins = 175)
	plots[np.ceil((j)/2)][(j)%2].bar(hist[1][:-1],hist[0],width=hist[1][1]-hist[1][0])
	plots[np.ceil((j)/2)][(j)%2].set_xlabel('$\sigma_'+str(j+1)+'$',fontsize=40)
	plots[np.ceil((j)/2)][(j)%2].set_ylabel('$n$',fontsize=40)
	plots[np.ceil((j)/2)][(j)%2].text(15.25,-0.5,'Segment ' + str(j+3),fontsize=30)
	plots[np.ceil((j)/2)][(j)%2].tick_params(axis='both', which='major', labelsize=20)

f.delaxes(plots[2][1])		
f.set_size_inches(32,20)
f.savefig("sigma_histogram.png", dpi = 300)