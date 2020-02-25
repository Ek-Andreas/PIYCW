import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns;
from natsort import natsorted, humansorted
plt.rcParams["figure.figsize"] = (8,6)

sns.set(color_codes=True)
connection = sqlite3.connect("policy_data.db")
connection.execute("ATTACH DATABASE 'normalized_privacy.db' as d2")

# cursor = connection.execute("select avg_rating, country from apps where avg_rating >= 1 and country <> 'Unknown'")
# cursor = connection.execute("select avg_rating from apps where country != 'Unknown' AND avg_rating != 0")
cursor = connection.execute(
    "select * from apps join d2.scores_normalized on apps.policy_link = scores_normalized.policy_link where avg_rating >1 and language = 'de'")
# cursor = connection.execute("select * from apps  join metrics on apps.policy_link  = metrics.entry_link ")
# cursor = connection.execute("select num_ratings, installs_range, continent, inapp_pay, eu_state, country, permissions, avg_rating, global, num_ratings, installs_range, android_version, smog, fkgl, gfog, lix_en from apps  join  scores on apps.policy_link = scores.policy_link  where language = 'en' ")

rows = cursor.fetchall()

field_names = [i[0] for i in cursor.description]
df = pd.DataFrame(rows, columns=field_names)
df = df[df.installs_range != "None to None"]

inrange = df.installs_range.unique()


inrange = sorted(inrange,key=len)

count = []
lix_de_gls = []
avergfog = []
wstf_gls = []
fre_de_gls = []
fre_en_gls = []
globas = []
for c in inrange:
#column_names = ["category",  "lix_de_gl", "wstf_gl", "fre_de_gl", "global"]
    subset = df[df['installs_range'] == c]
    count.append(subset.count())
    lix_de_gl = subset['lix_de_gl'].mean()
    wstf_gl = subset['wstf_gl'].mean()
    fre_de_gl = subset['fre_de_gl'].mean()
    globa = subset['global'].mean()
    if (
            lix_de_gl != None and wstf_gl != None and
            globa != None and fre_de_gl != None
    ):
        lix_de_gls.append(lix_de_gl)
        wstf_gls.append(wstf_gl)
        fre_de_gls.append(fre_de_gl)
        globas.append(globa)
# plt.plot(inrange, lix_de_gls, label='lix_de_gl')
# plt.plot(inrange, wstf_gls, label='wstf_gl')
# plt.plot(inrange, fre_de_gls, label='fre_de_gl')
# plt.plot(inrange,globas, label='global')
plt.xticks(inrange, fontsize=8, rotation='vertical')
# plt.xlabel('Number of downloads')
# plt.ylabel('Globalized scores')
# plt.legend(loc="lower right")
#
# plt.legend()
# plt.title('Global score according to number of downloads in German')
# plt.show()

plt.plot(count)

plt.show()


exit()
corr = df.corr(method ='pearson')
with pd.option_context('display.max_columns', None):  # more options can be specified also
    print(df)
# df.plot(y = 'num_ratings' ,x= 'fkgl', style = 'o')
# # corr = np.corrcoef(r["avg_rating"], r['country'])
# print(corr)