import itchat  # itchat documentation -- https://itchat.readthedocs.io/zh/latest/api/
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import re
# from wordcloud import WordCloud, ImageColorGenerator
import PIL.Image as Image # pillow
# import jieba  # chinese word segementation tool
from matplotlib.font_manager import FontProperties
# since matplotlib and pandas.plot cannot display chinese
font = FontProperties(fname='./data/DroidSansFallbackFull.ttf', size=14)  # load chinese font
# login, default a QR code will be generated, scan for login
itchat.login()
friends = itchat.get_friends(update=True)[0:]  # get all friends
print(friends[0])  # the first one is yourself

def get_male_female_count(friends):
    male = 0
    female = 0
    others = 0
    for friend in friends:
        sex = friend['Sex']
        if sex == 1:
            male += 1
        elif sex == 2:
            female += 1
        else:
            others += 1
    return male, female, others
male, female, others = get_male_female_count(friends[1:])
total = len(friends[1:])
print('Male population: {:d}, ratio: {:.4f}'.format(male, male / float(total)))
print('Female population: {:d}, ratio: {:.4f}'.format(female, female / float(total)))
print('Others: {:d}, ratio: {:.4f}'.format(others, others / float(total)))
# plot male-female-ratio
index = np.arange(3)
genders = (male, female, others)
bar_width = 0.35
plt.figure(figsize=(14, 7))
plt.bar(index, genders, bar_width, alpha=0.6, color='rgb')
plt.xlabel('Gender', fontsize=16)  
plt.ylabel('Population', fontsize=16)
plt.title('Male-Female Population', fontsize=18)  
plt.xticks(index, ('Male', 'Female', 'Others'), fontsize=14, rotation=20)
plt.ylim(0,220)
for idx, gender in zip(index, genders):
    plt.text(idx, gender + 0.1, '%.0f' % gender, ha='center', va='bottom', fontsize=14, color='black')
plt.show()

# extract the variables: NickName, Sex, City, Province, Signature
def get_features(friends):
    features = []
    for friend in friends:
        feature = {'NickName': friend['NickName'], 'Sex': friend['Sex'], 'City': friend['City'], 
                  'Province': friend['Province'], 'Signature': friend['Signature']}
        features.append(feature)
    return pd.DataFrame(features)
features = get_features(friends[1:])
print(features.columns)
features.head()

locations = features.loc[:, ['Province', 'City']]  # get location columns
locations = locations[locations['Province'] != '']  # clean empty city or province records
data = locations.groupby(['Province', 'City']).size().unstack()  # group by and count
count_subset = data.take(data.sum(1).argsort())[-20:]  # obtain the 20 highest data
# plot
subset_plot = count_subset.plot(kind='bar', stacked=True, figsize=(24, 24))
# set fonts
xtick_labels = subset_plot.get_xticklabels()
for label in xtick_labels: 
    label.set_fontproperties(font)
legend_labels = subset_plot.legend().texts
for label in legend_labels:
    label.set_fontproperties(font)
    label.set_fontsize(10)
plt.xlabel('Province', fontsize=20)
plt.ylabel('Number', fontsize=20)
plt.show()