import pandas as pd
import os
import glob
import numpy as np
from matplotlib import pyplot as plt
# import re

path = "./logs/"
print(path)
csv_files = glob.glob(os.path.join(path,"*.csv"))

for f in csv_files:
	df = pd.read_csv(f,usecols=[2])
	# df.set_index().plot()
	plt.figure()
	plt.plot(range(len(df)),df)
	plt.draw()
	plt.xlabel('$data points$')
	plt.ylabel('transmission time')
	plt.title('Latency')
	print(type(f))
	print(f)
	name = f.split('/')
	name = name[-1].split('.')
	plt.savefig("states_" + name[0] + ".png")




plt.show()
