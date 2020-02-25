import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
connection = sqlite3.connect("policy_data.db")
connection.execute("ATTACH DATABASE 'normalized_privacy.db' as d2")

cursor = connection.execute(
    "select * from apps join d2.scores_normalized on apps.policy_link = scores_normalized.policy_link where avg_rating >1 and language = 'en'")


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
cat = df['category1'].unique()
y_pos = np.arange(len(cat))
globe =[]
cc = []
column_names = ["cat", "score"]
dfres = pd.DataFrame(columns = column_names)
plt.rc('ytick', labelsize=5)

for c in cat:
    subset = df[df['category1'] == c]
    glob = subset['global'].mean()
    dfres = dfres.append({'cat' : c , 'score' : glob} , ignore_index=True)
    print(glob, c)

    globe.append(glob)
    cc.append(c)
    plt.bar(cat,c)
dfres = dfres.sort_values('score',ascending=True)
print(dfres)

#plt.barh(y_pos, globe)

plt.yticks(y_pos, cc)
plt.title('Global score according to category')

dfres.plot.barh(x='cat', y='score')
plt.show()


