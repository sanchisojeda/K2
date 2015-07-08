__version__ = "1.0.1"

"""Reads a .dat file and returns a 2d matrix

Column separator: tab
"""
def read_dat(fname,separator):
	data = []
	with open(fname,"r") as txt:
		for line in txt:
			line = line.replace("\n","")
			data.append(line.split(separator))
	return data

"""Writes a 2d matrix into a .dat file 

Column separator: tab
"""	
def write_dat(data,fname,separator):
	output = open(fname,"w")
	for r in range(0,len(data)):
		row = ""
		for c in data[r]:
			row = row + str(c) + separator
		print >>output,row

"""Deletes a row of a 2d matrix

First arg: 2d matrix Second arg: row number
"""
def delete_row(data,row):
	del data[row]
	return data

"""Deletes a row of a 2d matrix

First arg: 2d matrix Second arg: column number
"""
def delete_column(data,column):
	for row in data:
		del row[column]
	return data

"""Converts the column values to floats

First arg: 2d matrix Second arg: column number
"""
def numerize_column(data,column):
	for row in data:
		row[column] = float(row[column])

"""Returns a column as 1d array

First arg: 2d matrix Second arg: column number
"""		
def get_column(data,c):
	column = []
	for row in data:
		if c < len(row)-1:	
			column.append(row[c])
		else:
			column.append('nan')
	return column

"""Returns a column as 1d array converting its values to floats

First arg: 2d matrix Second arg: column number
"""	
def get_column_numerized(data,c):
	column = []
	for row in data:
		column.append(float(row[c]))
	return column

""" Translates an array to a piece-wise function


First arg: array Secon arg:value
"""
def array_to_function(array,x):
	if int(x) > len(array):
		return 1/0
	else:
		return array[int(x)]


