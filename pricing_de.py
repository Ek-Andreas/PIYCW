import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
connection = sqlite3.connect("policy_data.db")
connection.execute("ATTACH DATABASE 'normalized_privacy.db' as d2")

cursor = connection.execute(
    "select * from apps join d2.scores_normalized on apps.policy_link = scores_normalized.policy_link where avg_rating >1 and language = 'de'")


rows = cursor.fetchall()

field_names = [i[0] for i in cursor.description]
print(len(rows))
df = pd.DataFrame(rows, columns=field_names)

continent = df['price'].unique()
y_pos = np.arange(len(continent))
globe =[]
cc = []
barWidth = 1

column_names = ["price", "lix_de_gl", "wstf_gl", "fre_de_gl", "global"]
dfres = pd.DataFrame(columns = column_names)
plt.rc('ytick')

lix_de_gls = []
avergfog = []
wstf_gls = []
fre_de_gls = []
fre_en_gls = []
globas = []
res = []
for c in continent:
    subset = df[df['price'] == c]
    glob = subset['global'].mean()
    # dfres = dfres.append({'cat' : c , 'score' : glob} , ignore_index=True)
    lix_de_gl = subset['lix_de_gl'].mean()
    wstf_gl = subset['wstf_gl'].mean()
    fre_de_gl = subset['fre_de_gl'].mean()
    res = [c,lix_de_gl,wstf_gl,fre_de_gl,glob]
    dfres.loc[len(dfres)] = res

# dfres = dfres.sort_values('score',ascending=True)
#
# plt.bar(dfres, aversmog, edgecolor='white', width=barWidth)
# plt.bar(dfres, averlix_en, edgecolor='white', width=barWidth)
# plt.bar(dfres, averfkgl, edgecolor='white', width=barWidth)
# plt.bar(dfres, fre_en_gls, edgecolor='white', width=barWidth)
# plt.bar(dfres, avergfog, edgecolor='white', width=barWidth)
# plt.bar(dfres, globe, edgecolor='white', width=barWidth)
# plt.xticks(dfres, fontsize=8, rotation='vertical')
#
dfres = dfres.sort_values('global',ascending=True)
print(dfres)
plt.rcParams["figure.figsize"] = (8,6)
del dfres['global']
# dfres.drop('global', axis=1)
# plt.barh(y_pos, globe)
plt.ylabel('globalized scores')

dfres.plot.bar(x='price', stacked=True)
# plt.yticks(y_pos, cc)
plt.title('readability score according to price in German')
plt.legend(loc="lower left", mode = "expand", ncol = 6)
plt.grid(axis='y')

# dfres.plot.barh(x='cat', y='score')
plt.show()


