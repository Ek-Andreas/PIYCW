import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns;
sns.set(color_codes=True)
connection = sqlite3.connect("policy_data.db")
##todo actually make it german
# cursor = connection.execute("select avg_rating, country from apps where avg_rating >= 1 and country <> 'Unknown'")
# cursor = connection.execute("select avg_rating from apps where country != 'Unknown' AND avg_rating != 0")
cursor = connection.execute(
    "select * from apps join scores on apps.policy_link = scores.policy_link where avg_rating >1 and language = 'de'")
# cursor = connection.execute("select * from apps  join metrics on apps.policy_link  = metrics.entry_link ")
# cursor = connection.execute("select num_ratings, installs_range, continent, inapp_pay, eu_state, country, permissions, avg_rating, global, num_ratings, installs_range, android_version, smog, fkgl, gfog, lix_en from apps  join  scores on apps.policy_link = scores.policy_link  where language = 'en' ")

rows = cursor.fetchall()

field_names = [i[0] for i in cursor.description]
print(len(rows))
df = pd.DataFrame(rows, columns=field_names)
rat = df['avg_rating'].value_counts().index.tolist()
arange = [x * 0.1 for x in range(11, 50)]  # for some reason numpy arange wasn't cooperating
wstf_gls = []
globalss = []
lix_de_gls = []
fre_de_gls = []
c = arange

#column_names = ["category",  "lix_de_gl", "wstf_gl", "fre_de_gl", "global"]

for c in arange:
    rc= round (c, 2)# to avoid a weird issue where c = 1.2000000001
    subset = df[df['avg_rating'] == rc]
    wstf_gl = subset['wstf_gl'].mean()
    lix_de_gl = subset['lix_de_gl'].mean()
    fre_de_gl = subset['fre_de_gl'].mean()
    globals = subset['global'].mean()
    wstf_gls.append(wstf_gl)
    lix_de_gls.append(lix_de_gl)
    fre_de_gls.append(fre_de_gl)
    globalss.append(globals)
plt.rcParams["figure.figsize"] = (8,6)

plt.plot(arange, wstf_gls, label='wstf_gl')
plt.plot(arange, lix_de_gls, label='fre_de_gl')
plt.plot(arange, fre_de_gls, label='fre_de_gl')
plt.plot(arange, globalss, label='global')
plt.legend()
plt.title('Global score according to Average user rating in german')

plt.xlabel('User rating')
plt.ylabel('Normalized scores')
plt.show()
#
# plt.plot(arange,num, label='global')
# plt.title('App distribution according to user rating in english')
# plt.xlabel('User rating')
# plt.ylabel('Number of downloads')
# plt.yscale("log")
# plt.show()

# corr = df.corr(method ='pearson')
# with pd.option_context('display.max_columns', None):  # more options can be specified also
#     print(df)
# df.plot(y = 'num_ratings' ,x= 'fkgl', style = 'o')
# corr = np.corrcoef(r["avg_rating"], r['country'])
# print(corr)

