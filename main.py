import datalib
import os
import matplotlib.pyplot as plt
import random
import numpy as np
import scipy as sp
from scipy.interpolate import interp1d


def read_target_file(fname):
	data = []
	with open(fname,'r') as txt:
		for line in txt:
			line = line.replace('\n','')
			data.append(line.split(','))
	return data

def read_K2_file(fname):
	if fname == 'no_file':
		return ['no_data']
	data = []
	with open(fname,'r') as txt:
		for line in txt:
			line = line.replace('\n','')
			a = line.split('        ')
			b = a[0].split('     ')
			row = [b[0],b[1],a[1]]
			data.append(row)

	datalib.numerize_column(data,0)
	datalib.numerize_column(data,1)		
	datalib.numerize_column(data,2)		
		
	return data

def search_target_data(star_id,data):
	datalib.delete_row(data,0)
	for row in data:
		if int(row[0]) == star_id:
			return row
	return ['not_found']		

def search_photometry_files(star_id,folder):
	star_files = []
	for file in os.listdir(folder):
		if str(star_id) in file:
			star_files.append(folder + '/' + file)
	if star_files == []:
		star_files[0] = 'no_file'
	return star_files		

def split_data_in_segments(data):
	data_by_segments = []
	for i in range(0,int(get_data_segments(data))):
		data_by_segments.append(get_data_by_segment(data,i))
	return data_by_segments
def get_data_by_segment(data,segment):
	new = []
	for row in data:
		if row[2] == segment:
			new.append(row)
	return new

def get_data_segments(data):
	return data[len(data)-1][2] + 1

def f_plot_photo(data,col):
	x = datalib.get_column(data,0)
	y = datalib.get_column(data,1)
	print len(x),len(y)	
	plt.plot(x,y,'-',color = col)

def f_plot_poly(poly,x,col):
	xs = np.linspace(x[0],x[len(x)-1],100)
	p = np.poly1d(poly)
	plt.plot(xs,p(xs),'--',color = col)

def f_plot_spline(x,y,col):
	plt.plot(x,y,color = col)

def polynomial_fit(data,xcol,ycol,degree):
	x = datalib.get_column(data,xcol)
	y = datalib.get_column(data,ycol)
	return np.polyfit(x,y,degree)

def spline_interpolation(data,xcol,ycol,length_factor):
	x = datalib.get_column(data,xcol)
	y = datalib.get_column(data,ycol)
	new_length = length_factor*len(x)
	new_x = np.linspace(x[0], x[len(x)-1], new_length)
	new_y = sp.interpolate.interp1d(x, y, kind='cubic')(new_x)
	return [new_x,new_y]

#Points at >n*sigma become the average of all points
def smooth1(data,n):
	std = np.std(data)
	mean = np.mean(data)

	smoothed = []
	for value in data:
		if abs(value - mean) > n*std:
			smoothed.append(mean)
		else:
			smoothed.append(value)
	return smoothed

#Points at >n*sigma become the average of the next and previous points
def smooth2(data,n,iterations):

	if iterations > 1:
		smoothed = data
		for i in range(0,iterations):
			smoothed = smooth2(smoothed,n,0)
		return smoothed
	else:
		std = np.std(data)
		mean = np.mean(data)

		smoothed = []
		for i in range(0,len(data)):
			if abs(data[i] - mean) > n*std:
				if i>0 and i<len(data)-1:
					smoothed.append((data[i-1] + data[i+1])/2)
				if i == 0:
					smoothed.append(data[i+1])
				if i == len(data)-1:
					smoothed.append(data[i-1])
				smoothed.append(data[i])	
			else:
				smoothed.append(data[i])
		print len(data),len(smoothed)		
		return smoothed

def get_K2_info(star_id,plot_photo = False,plot_poly = False,plot_spline = False,photometry_dir = 'Decorrelatedphotometry2', targets_file = 'K2Campaign0targets.csv - K2Campaign0targets.csv',poly_fit_deg = 0,spline_fit=False,spline_length_factor = .25):
	info = dict()
	info['error'] = 'None'

	target_data = search_target_data(star_id,read_target_file(targets_file))

	if target_data[0] == 'not_found':
		info['error'] = 'Star is not a target.'
	else:
		info['star_info'] = target_data

		photo_data = read_K2_file(search_photometry_files(star_id,'Decorrelatedphotometry2')[0])

		info['photo_data_by_segments'] = split_data_in_segments(photo_data)

		info['means'] = []
		for segment in info['photo_data_by_segments']:
			info['means'].append(np.mean(datalib.get_column(segment,1)))
		print info['means']

		info['stds'] = []
		for segment in info['photo_data_by_segments']:
			info['stds'].append(np.std(datalib.get_column(segment,1)))
		print info['stds']
			
		info['polynomial_fits'] = []
		if poly_fit_deg != 0 or plot_poly:
			for segment in info['photo_data_by_segments']:
				info['polynomial_fits'].append(polynomial_fit(segment,0,1,poly_fit_deg))

		info['spline_fits'] = []	
		if spline_fit or plot_spline:
			for segment in info['photo_data_by_segments']:
				info['spline_fits'].append(spline_interpolation(segment,0,1,spline_length_factor))
		
		random.seed()
		if plot_photo or plot_poly or plot_spline:
			for i in range(0,len(info['photo_data_by_segments'])):
				if plot_photo:
					f_plot_photo(info['photo_data_by_segments'][i],[random.random(),random.random(),random.random()])
				if plot_poly:
					f_plot_poly(info['polynomial_fits'][i],datalib.get_column(info['photo_data_by_segments'][i],0),[random.random(),random.random(),random.random()])
				if plot_spline:
					f_plot_spline(info['spline_fits'][i][0],info['spline_fits'][i][1],[random.random(),random.random(),random.random()])
			plt.show()
	return info

print get_K2_info(202059210,spline_fit=False,plot_spline = False,plot_photo = True,plot_poly = False,poly_fit_deg = 5,spline_length_factor = 1)







#print '---------EPIC' + str(star_id) + '---------'
#print '*RA (J2000) [deg]:	' + target_data[1]
#print '*Dec (J2000) [deg]:	' + target_data[2]
#print '*Magnitude:		' + target_data[3]
#print '*Cadence [min]:		' + target_data[4]
#print '*Investigation IDs:	' + target_data[5]
#print '-------------------------------'
