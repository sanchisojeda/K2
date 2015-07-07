import datalib
import matplotlib.pyplot as plt

data = datalib.read_dat('evaluation.csv',',')
del data[0]
mags = datalib.get_column_numerized(data,1)
sigma_avg = []
for row in data:
	S = 0
	i = 2
	n = 0
	while row[i] != '':
		S += float(row[i])
		n += 1
		i += 1

	sigma_avg.append(S/n)

plt.plot(sigma_avg,mags,'.')
plt.show()