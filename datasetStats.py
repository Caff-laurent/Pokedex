import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Show numbers of pokemon by type

dataCsv = pd.read_csv('./dataset/pokemon_types_names.csv', sep=',', index_col=0)

sns.set(style="darkgrid")
print(dataCsv)
ax = sns.countplot(x="Type_1", data=dataCsv)
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
plt.tight_layout()
plt.show()


# Show how much files by types

data = './Pokemon/dataset/'
datasetType = []
for directory in os.listdir(data):
    if os.path.isdir(os.path.join(data, directory)):
        file_count = len(os.listdir(os.path.join(data, directory)))
        datasetType.append((directory, file_count))

sns.set(style="darkgrid")
ax = sns.barplot(x=[entry[0] for entry in datasetType], y=[entry[1] for entry in datasetType])
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
ax.set_ylabel("File Count")
plt.tight_layout()
plt.show()