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
# ['PRODUCTIVITY' 'BUSINESS' 'MEDICAL' 'GAME_PUZZLE' 'COMMUNICATION'
# 'GAME_RACING' 'EVENTS' 'GAME_CASINO' 'GAME_TRIVIA' 'SOCIAL' 'TOOLS'
#  'LIFESTYLE' 'HEALTH_AND_FITNESS' 'MUSIC_AND_AUDIO' 'VIDEO_PLAYERS'
#  'GAME_CASUAL' 'ENTERTAINMENT' 'SPORTS' 'GAME_STRATEGY' 'EDUCATION'
#  'GAME_SPORTS' 'GAME_EDUCATIONAL' 'TRAVEL_AND_LOCAL' 'GAME_ADVENTURE'
#  'GAME_SIMULATION' 'GAME_ROLE_PLAYING' 'GAME_MUSIC' 'GAME_WORD'
#  'GAME_BOARD' 'ART_AND_DESIGN' 'GAME_ARCADE' 'BOOKS_AND_REFERENCE'
#  'GAME_CARD' 'GAME_ACTION' 'HOUSE_AND_HOME' 'BEAUTY' 'AUTO_AND_VEHICLES'
#  'FINANCE' 'COMICS' 'PARENTING' 'DATING' 'PERSONALIZATION' 'PHOTOGRAPHY'
#  'WEATHER' 'SHOPPING' 'MAPS_AND_NAVIGATION' 'LIBRARIES_AND_DEMO'
#  'FOOD_AND_DRINK' 'NEWS_AND_MAGAZINES']
category = df['category1'].unique()
y_pos = np.arange(len(category))
globe =[]
cc = []
barWidth = 1

column_names = ["category",  "lix_de_gl", "wstf_gl", "fre_de_gl", "global"]
dfres = pd.DataFrame(columns = column_names)
plt.rc('ytick')
aversmog = []
avergfog = []
averlix_en = []
averfkgl = []
fre_en_gls = []
globas = []
res = []
for c in category:
    subset = df[df['category1'] == c]
    glob = subset['global'].mean()
    # dfres = dfres.append({'cat' : c , 'score' : glob} , ignore_index=True)
    lix_de_gl = subset['lix_de_gl'].mean()
    wstf_gl = subset['wstf_gl'].mean()
    fre_de_gl = subset['fre_de_gl'].mean()
    res = [c,  lix_de_gl, wstf_gl, fre_de_gl,  glob]
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
print(dfres)
dfres.plot.bar(x='category', stacked=True)
# plt.yticks(y_pos, cc)
plt.title('readability score according to category in German')
plt.legend(loc="lower left", mode = "expand", ncol = 6)
plt.grid(axis='y')

# dfres.plot.barh(x='cat', y='score')
plt.show()


