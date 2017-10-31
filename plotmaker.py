import os
import math
import numpy as np
import matplotlib.pyplot as plt

models = sorted([model for model in os.listdir('.') if os.path.isdir(model)])

logR_range = np.linspace(-1, 3, 41)

logRlogMgrid = [[0 for x in range(16)] for y in range(41)]
exposure = [[0 for x in range(16)] for y in range(41)]

for model in models:
	if model == '4.0Msun_nolim':
		continue
	with open(model+'/LOGS/history.data') as source:
		data = source.readlines()

	info = {str(data[1].split()[i]): data[2].split()[i] for i in range(len(data[1].split()))} 

	params_labels = data[5].strip().split()

	all_dat = [[] for _ in range(len(params_labels))]

	for line in data[6:]:
		for i in range(len(params_labels)):
			all_dat[i].append(line.split()[i])

	parameters = {str(params_labels[i]): all_dat[params_labels.index(str(params_labels[i]))] for i in range(len(params_labels))}

	plotting = [
		'star_age',
		'star_mass',
		'log_L',
		'log_Teff',
		'log_R',
		'he_core_mass'
		]

	plt.plot(parameters.get(plotting[3]), parameters.get(plotting[2]), label=model)

	for value in range(len(parameters.get(plotting[4]))):
		radius, model_index, he_core_mass = parameters.get(plotting[4]), models.index(model), parameters.get(plotting[5])
		index = min(enumerate(logR_range), key=lambda x: abs(x[1]-round(float(radius[value]), 1)))[0]
		logRlogMgrid[index][model_index] += float(he_core_mass[value])
		exposure[index][model_index] += 1

	#for value in range(len(logR_range)):
		#index = min(enumerate(parameters.get(plotting[4])), key=lambda x: abs(float(x[1])-logR_range[value]))[0]
		#logRlogMgrid[value][models.index(model)] = float(parameters.get(plotting[5])[index])

plt.xlabel(plotting[3])
plt.ylabel(plotting[2])
plt.gca().invert_xaxis()
plt.title('H-R Diagram')
plt.legend()
plt.show()
plt.close()

logRlogMgrid = np.divide(logRlogMgrid, exposure)

fig, ax = plt.subplots()
plt.imshow(logRlogMgrid, origin='lower', extent=[1.0, 4.0, -1.0, 3.0], interpolation='none')
plt.colorbar()
plt.grid()
plt.xlabel(r'Mass $\mathrm{(M_{\odot})}$', fontsize=15)
plt.ylabel(r'Log $\mathrm{R/R_{\odot}}$', fontsize=15)
plt.show()
plt.close()
