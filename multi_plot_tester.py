import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

my_data = [[28, 70, 195], [28, 67, 145], [26, 73, 175], [63, 70, 170], [64, 71, 185]]
family_array = np.array(my_data)
family_df = pd.DataFrame(family_array)
family_df.columns = ["age", "height", "weight"]
# print(family_df)
# family_df.plot(kind='scatter', x='age', y='height', subplots=True)
# family_df.plot(kind='scatter', x='age', y='weight', subplots=True)
# plt.show()

graph1_columns = ["age", "weight"]
graph2_columns = ["age", "height"]
graph1 = family_df[graph1_columns]

graph2 = family_df[graph2_columns]
plt.show()
