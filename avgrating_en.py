import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns;
sns.set(color_codes=True)
connection = sqlite3.connect("policy_data.db")
connection.execute("ATTACH DATABASE 'normalized_privacy.db' as d2")

# cursor = connection.execute("select avg_rating, country from apps where avg_rating >= 1 and country <> 'Unknown'")
# cursor = connection.execute("select avg_rating from apps where country != 'Unknown' AND avg_rating != 0")
cursor = connection.execute(
    "select * from apps join d2.scores_normalized on apps.policy_link = scores_normalized.policy_link where avg_rating >1 and language = 'en'")
# cursor = connection.execute("select * from apps  join metrics on apps.policy_link  = metrics.entry_link ")
# cursor = connection.execute("select num_ratings, installs_range, continent, inapp_pay, eu_state, country, permissions, avg_rating, global, num_ratings, installs_range, android_version, smog, fkgl, gfog, lix_en from apps  join  scores on apps.policy_link = scores.policy_link  where language = 'en' ")

rows = cursor.fetchall()

field_names = [i[0] for i in cursor.description]
print(len(rows))
df = pd.DataFrame(rows, columns=field_names)
rat = df['avg_rating'].value_counts().index.tolist()
arange = [x * 0.1 for x in range(11, 50)]  # for some reason numpy arange wasn't cooperating
aversmog = []
avergfog = []
averlix_en = []
averfkgl = []
globas = []
num = []
fre_en_gls = []
c = arange
for c in arange:
    rc= round (c, 2)# to avoid a weird issue where c = 1.2000000001
    subset = df[df['avg_rating'] == rc]
    avgsmog = subset['smog_gl'].mean()
    avglix = subset['lix_en_gl'].mean()
    avgfkgl = subset['fkgl_gl'].mean()
    avggfog = subset['gfog_gl'].mean()
    fre_en_gl = subset['fre_en_gl'].mean()
    globa = subset['global'].mean()
    num.append(len(subset.index))
    aversmog.append(avgsmog)
    averlix_en.append(avglix)
    averfkgl.append(avgfkgl)
    avergfog.append(avggfog)
    fre_en_gls.append(fre_en_gl)
    globas.append(globa)

plt.rcParams["figure.figsize"] = (8,6)

plt.plot(arange,aversmog, label='smog_gl')
plt.plot(arange,averlix_en, label='lix_en_gl')
plt.plot(arange,averfkgl, label='fkgl_gl')
plt.plot(arange,avergfog, label='gfog_gl')
plt.plot(arange,fre_en_gls, label='fre_en_gl')
plt.plot(arange,globas, label='global')
plt.xlabel('User rating')
plt.ylabel('Normalized scores')
plt.legend()
plt.title('Global score according to Average user rating english')
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

