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
    "select * from apps join scores on apps.policy_link = scores.policy_link where avg_rating >1 and language = 'en'")
# cursor = connection.execute("select * from apps  join metrics on apps.policy_link  = metrics.entry_link ")
# cursor = connection.execute("select num_ratings, installs_range, continent, inapp_pay, eu_state, country, permissions, avg_rating, global, num_ratings, installs_range, android_version, smog, fkgl, gfog, lix_en from apps  join  scores on apps.policy_link = scores.policy_link  where language = 'en' ")
rows = cursor.fetchall()

field_names = [i[0] for i in cursor.description]
df = pd.DataFrame(rows, columns=field_names)
corr = df.corr(method ='pearson')
with pd.option_context('display.max_columns', None):  # more options can be specified also
    print(corr)