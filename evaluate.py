import K2
import datalib
import matplotlib.pyplot as plt
import random
import numpy as np
import scipy as sp

KEPLER_CADENCE = 29.42

def get_data(star_id,data):
	for row in data:
		if float(star_id) == float(row[0]):
			return row[1:4]
	return ['nan']*3

targets = datalib.get_column(K2.read_target_file('K2Campaign0targets.csv - K2Campaign0targets.csv'),0)
del targets[0]

result = [['#EPIC','is_dwarf','teff','kepmag','sigma_1','sigma_2','sigma_3','sigma_4','sigma_5']]
errors = []
quality = [['#EPIC','seg_1_ratio','seg_1_flag','seg_2_ratio','seg_2_flag','seg_3_ratio','seg_3_flag','seg_4_ratio','seg_4_flag','seg_5_ratio','seg_5_flag']]

tess_data = datalib.read_dat('k2tess.csv',',')
del tess_data[0]

faint_data = datalib.read_dat('k2faint.csv',',')
del faint_data[0]

for i in range(0,len(targets)):
	target = targets[i]
	print target + ' : ' + str(int((100.0*i)/len(targets))) + '%' 
	info = K2.get_K2_info(int(target),poly_fit_deg = 8)
	if info['error'] == 'None':
		star = []

		star_data_tess = get_data(target,tess_data)
		if star_data_tess != ['nan']*3:
			star = [target] + star_data_tess
		else:
			star = [target] + get_data(target,faint_data)

		star_qual = [target]
		data_by_segs = info['subtraction_by_segments']
		for seg in data_by_segs:
			t0 = seg[0][0]*1440
			t1 = seg[0][-1]*1440
			num_i = (t1-t0)/KEPLER_CADENCE
			if len(seg[0]) < .5*num_i:
				star_qual.append('BAD')
			else:
				star_qual.append('GOOD')
				sigma = np.std(seg[1])
				star.append(sigma)
			star_qual.append(len(seg[0])/float(num_i))	
		result.append(star)
		quality.append(star_qual)
	else:
		errors.append(target)
datalib.write_dat(result,'evaluation.csv',',')
datalib.write_dat(errors,'bad_data.csv','')
datalib.write_dat(quality,'quality.csv',',')