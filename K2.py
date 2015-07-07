import datalib
import os
import matplotlib.pyplot as plt
import random
import numpy as np
import scipy as sp
from scipy.interpolate import interp1d

import warnings

#returns the data from the target .csv file as a 2d array
def read_target_file(fname):
	data = []
	with open(fname,'r') as txt:
		for line in txt:
			line = line.replace('\n','')
			data.append(line.split(','))
	return data

#returns the data from a photometry file as a 2d array
def read_K2_file(fname):
	if fname == 'no_file':
		return ['no_data']
	data = []
	with open(fname,'r') as txt:
		for line in txt:
			line = line.replace('\n','')
			a = line.split('        ')
			b = a[0].split('    ')				
			row = [b[0],b[1],a[1]]
			data.append(row)
	try:
		datalib.numerize_column(data,0)
		datalib.numerize_column(data,1)		
		datalib.numerize_column(data,2)	
	except Exception, e:
		return ['no_data']
		
	return data

#returns the row from the target .csv file for a given EPIC id
def search_target_data(star_id,data):
	datalib.delete_row(data,0)
	for row in data:
		if int(row[0]) == star_id:
			return row
	return ['not_found']		

#returns a list of photometry files associated with an EPIC id
def search_photometry_files(star_id,folder):
	star_files = []
	for file in os.listdir(folder):
		if str(star_id) in file:
			star_files.append(folder + '/' + file)
	if star_files == []:
		star_files.append('no_file')
	return star_files		

#splits into segments the 2d array of the photometry data 
def split_data_in_segments(data):
	data_by_segments = []
	for i in range(0,int(get_data_segments(data))):
		data_by_segments.append(get_data_by_segment(data,i))
	return data_by_segments

#returns all the data corresponding to a segment
def get_data_by_segment(data,segment):
	new = []
	for row in data:
		if row[2] == segment:
			new.append(row)
	return new

#returns the amount of segments in a photometry file
def get_data_segments(data):
	return data[len(data)-1][2] + 1

#plots a photometry file
def f_plot_photo(data,col):
	x = datalib.get_column(data,0)
	y = datalib.get_column(data,1)
	plt.plot(x,y,'-',color = col)

#plots a polynomial fit 
def f_plot_poly(poly,x,col):
	xs = np.linspace(x[0],x[len(x)-1],100)
	p = np.poly1d(poly)
	plt.plot(xs,p(xs),'--',color = col)

#performs a polynomial fit, returning an array of the coefficients of the polynomial
def polynomial_fit(data,xcol,ycol,degree):
	x = datalib.get_column(data,xcol)
	y = datalib.get_column(data,ycol)
	delete_n_sigma(x,y,4)
	return np.polyfit(x,y,degree)

#deletes points > n*sigma
def delete_n_sigma(data_x,data_y,n):
	sigma = np.std(data_y)
	avg = np.average(data_y)
	i = 0
	end = len(data_x)
	while i in range(0,end):
		if abs(data_y[i]-avg) > n*sigma:
			del data_x[i],data_y[i]
		end = len(data_x)
		i+=1	
#subtracts vector b from vector a
def subtract(a,b):
	c = []
	if len(a) == len(b):
		for i in range(0,len(a)):
			c.append(a[i]-b[i])
		return c	
	else:
		print 'Lengths of a and b not equal!'

#subtracts a poly from a data set (poly is an array of coefficients generated by NumPy)
def subtract_poly_from_data(data_x,data_y,poly):
	delete_n_sigma(data_x,data_y,3)
	p = np.poly1d(poly)
	p_y = []
	for x in data_x:
		p_y.append(p(x))
	return [data_x,subtract(data_y,p_y)]

'''This function returns a dictionary with info and data retrieved and computed from a list of targets and photometry data

dictionary keys:

'error' --> Information about possible errors in the computations
'star_info' --> Info retrieved from the targets .csv file, it is an array with [RA,Dec,Mag,cadence,investigation ids] 
'photo_data_by_segments' --> A 3-dimensional array, first dimension is the segment, second is the time and third the flux
'polynomial_fits' --> An array with the polynomial (array of coefficients) that fits each segment.
'subtraction_by_segments' --> The photometry of each segment minus the polynomial fitted to that segment.
'''
def get_K2_info(star_id,plot_photo = False,plot_poly = False,photometry_dir = 'Decorrelatedphotometry2', targets_file = 'K2Campaign0targets.csv - K2Campaign0targets.csv',poly_fit_deg = 0,subtract_fit = True):
	info = dict()
	info['error'] = 'None'

	warnings.simplefilter('ignore', np.RankWarning)

	target_data = search_target_data(star_id,read_target_file(targets_file))

	if target_data[0] == 'not_found':
		info['error'] = 'Star is not a target.'
	else:
		info['star_info'] = target_data

		photo_data = read_K2_file(search_photometry_files(star_id,'Decorrelatedphotometry2')[0])

		if(photo_data[0] == 'no_data'):
			info['error'] = 'No photo data'
			return info

		info['photo_data_by_segments'] = split_data_in_segments(photo_data)
			
		info['polynomial_fits'] = []
		if poly_fit_deg != 0 or plot_poly:
			for segment in info['photo_data_by_segments']:
				info['polynomial_fits'].append(polynomial_fit(segment,0,1,poly_fit_deg))

		info['subtraction_by_segments'] = []
		if subtract_fit:
			for i in range(0,len(info['photo_data_by_segments'])):
				segment = info['photo_data_by_segments'][i]
				x = datalib.get_column(segment,0)
				y = datalib.get_column(segment,1)
				poly = info['polynomial_fits'][i]
				info['subtraction_by_segments'].append(subtract_poly_from_data(x,y,poly))
		random.seed()
		if plot_photo or plot_poly:
			for i in range(0,len(info['photo_data_by_segments'])):
				if plot_photo:					
					f_plot_photo(info['photo_data_by_segments'][i],[random.random(),random.random(),random.random()])
				if plot_poly:
					f_plot_poly(info['polynomial_fits'][i],datalib.get_column(info['photo_data_by_segments'][i],0),[random.random(),random.random(),random.random()])
			plt.show()
	return info
