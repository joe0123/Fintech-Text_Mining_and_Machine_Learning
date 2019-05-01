import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

original_data = pd.read_csv("co-occurrence_matrix.csv").drop(columns=["label_headers"]).values.flatten()
data = [i for i in original_data if i > 0]
_, axs=plt.subplots()
axs.hist(data, bins = 20, cumulative = True, edgecolor='black',density=True)
axs.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1))
plt.show()

