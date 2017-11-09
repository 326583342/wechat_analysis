# -*- coding: utf-8 -*-
import itchat
import pandas as pd
from pyecharts import Geo, Bar


itchat.login()
friends = itchat.get_friends(update=True)[0:]

def User2dict(User):
    User_dict = {}
    User_dict["NickName"] = User["NickName"] if User["NickName"] else "NaN"
    User_dict["City"] = User["City"] if User["City"] else "NaN"
    User_dict["Sex"] = User["Sex"] if User["Sex"] else 0
    User_dict["Signature"] = User["Signature"] if User["Signature"] else "NaN"
    User_dict["Province"] = User["Province"] if User["Province"] else "NaN"
    return User_dict

friends_list = [User2dict(i) for i in friends]
data = pd.DataFrame(friends_list)
data.to_csv('wechat_data.csv', index=True, encoding='utf8')

def Cal_mVw(data):
    result = {}
    for i in data:
        if i == 1:
            result["man"] = result.get("man", 0) + 1
        elif i == 2:
            result["woman"] = result.get("woman", 0) + 1
        else:
            result["unknown"] = result.get("nunknown", 0) + 1
    return result


def count_city(data):
    result = {}
    for i in data:
        if data is not "NaN" or data is not "nan":
            result[i] = result.get(i, 0) + 1
    return result

data1 = pd.read_csv('wechat_data.csv', encoding='utf8')
manVSwoman=Cal_mVw(data1["Sex"])
#print(manVSwoman)
bar = Bar("����΢�ź�����Ů����")
bar.add("��Ů����", ["��", "Ů", "����"], [139, 75, 1])
bar.render()

city=count_city(data1["City"])
geo = Geo("΢�ź��ѷֲ�", "", title_color="#fff", title_pos="center",
width=1200, height=600, background_color='#404a59')
#attr, value = geo.cast(city)
geo.add("", city.keys(), city.values(), visual_range=[0, 30], visual_text_color="#fff", symbol_size=15, is_visualmap=True)
geo.show_config()
geo.render()