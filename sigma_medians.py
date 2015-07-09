import datalib as dl
import numpy as np
import matplotlib.pyplot as plt

data = dl.read_dat('evaluation.csv',',')
sigmas = []
for sigma in range(4,9):
	sigmas.append(dl.get_column(data,sigma))

medians = []
for sigma in sigmas:
	good_sigmas = []
	for i in range(1,len(sigma)):
		if sigma[i] != 'nan':
			if np.log10(float(sigma[i])):
				good_sigmas.append(float(sigma[i]))
	good_sigmas = np.sort(good_sigmas)
	good_sigmas = good_sigmas[0:int(0.8*len(good_sigmas))]
	medians.append(np.median(good_sigmas))

plt.plot([1,2,3,4,5],medians)
plt.show()