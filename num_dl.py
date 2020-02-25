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
    "select * from apps join d2.scores_normalized on apps.policy_link = scores_normalized.policy_link where avg_rating >1 and language = 'en'")
# cursor = connection.execute("select * from apps  join metrics on apps.policy_link  = metrics.entry_link ")
# cursor = connection.execute("select num_ratings, installs_range, continent, inapp_pay, eu_state, country, permissions, avg_rating, global, num_ratings, installs_range, android_version, smog, fkgl, gfog, lix_en from apps  join  scores on apps.policy_link = scores.policy_link  where language = 'en' ")

rows = cursor.fetchall()

field_names = [i[0] for i in cursor.description]
df = pd.DataFrame(rows, columns=field_names)
inrange = df.installs_range.unique()
inrange = sorted(inrange,key=len)


aversmog = []
avergfog = []
averlix_en = []
averfkgl = []
fre_en_gls = []
globas = []
for c in inrange:

    subset = df[df['installs_range'] == c]
    avgsmog = subset['smog_gl'].mean()
    avglix = subset['lix_en_gl'].mean()
    avgfkgl = subset['fkgl_gl'].mean()
    fre_en_gl = subset['fre_en_gl'].mean()
    avggfog = subset['gfog_gl'].mean()
    globa = subset['global'].mean()
    if (
            avgsmog != None and avgfkgl != None and
            avglix != None and avggfog != None
    ):
        aversmog.append(avgsmog)
        averlix_en.append(avglix)
        averfkgl.append(avgfkgl)
        avergfog.append(avggfog)
        fre_en_gls.append(fre_en_gl)
        globas.append(globa)
plt.plot(inrange,aversmog, label='smog_gl')
plt.plot(inrange,averlix_en, label='lix_en_gl')
plt.plot(inrange,averfkgl, label='fkgl_gl')
plt.plot(inrange,avergfog, label='gfog_gl')
plt.plot(inrange,fre_en_gls, label='fre_en_gl')
plt.plot(inrange,globas, label='global')
plt.xticks(inrange, fontsize=8, rotation='vertical')
plt.xlabel('number of downloads')
plt.ylabel('globalized scores')
plt.legend()
plt.title('Global score according to number of downloads in english')
plt.show()



# corr = df.corr(method ='pearson')
# with pd.option_context('display.max_columns', None):  # more options can be specified also
#     print(df)
# df.plot(y = 'num_ratings' ,x= 'fkgl', style = 'o')
# corr = np.corrcoef(r["avg_rating"], r['country'])
# print(corr)
exit()
