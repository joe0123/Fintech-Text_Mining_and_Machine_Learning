import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

original_data = pd.read_csv("co-occurrence_matrix.csv").drop(columns=["label_headers"]).values.flatten()
data = [i for i in original_data if i > 0]
plt.hist(data, bins = 20, cumulative = True, edgecolor='black')
plt.yticks(np.arange(500, 5000, step=500))
plt.show()

