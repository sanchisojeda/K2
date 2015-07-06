import K2
import datalib
import matplotlib.pyplot as plt
import random
import numpy as np
import scipy as sp

targets = datalib.get_column(K2.read_target_file('K2Campaign0targets.csv - K2Campaign0targets.csv'),0)
del targets[0]

for target in targets:
	info = K2.get_K2_info(int(target),poly_fit_deg = 8)
	
	if info['error'] == 'None':
		data_by_segs = info['subtraction_by_segments']
		for seg in data_by_segs:
			plt.plot(seg[0],seg[1])
		plt.show()
