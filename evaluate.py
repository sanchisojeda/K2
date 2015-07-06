import K2
import datalib
import matplotlib.pyplot as plt
import random
import numpy as np
import scipy as sp

targets = datalib.get_column(K2.read_target_file('K2Campaign0targets.csv - K2Campaign0targets.csv'),0)
del targets[0]

result = [['#EPIC','mag','sigma_1','sigma_2','sigma_3','sigma_4','sigma_5']]
errors = []
for i in range(0,len(targets)):
	target = targets[i]
	print target + ' : ' + str(int((100.0*i)/len(targets))) + '%' 
	info = K2.get_K2_info(int(target),poly_fit_deg = 8)
	if info['error'] == 'None':
		star = [target,info['star_info'][2]]
		data_by_segs = info['subtraction_by_segments']
		for seg in data_by_segs:
			sigma = np.std(seg[1])
			star.append(sigma)
		result.append(star)
	else:
		errors.append(target)
datalib.write_dat(result,'evaluation.csv',',')
datalib.write_dat(errors,'bad_data.csv','')