# import seaborn as sns
# import matplotlib.pyplot as plt
import pandas as pd
import emoji
from wordcloud import WordCloud
from urlextract import URLExtract
from collections import Counter

extractor = URLExtract()

def fetch(selected_user, df):

    if selected_user != 'Overall analysis':

        df = df[df['User'] == selected_user]
        
#    fetch number of messages
    num_messages = df.shape[0]
    
    # fetch number of mediafiles
    num_media = df[df["User_messages"] == '<Media omitted>\n'].shape[0]

    num_of_deleted = df[df["User_messages"] == "You deleted this message\n"].shape[0]+df[df["User_messages"] == "This message was deleted\n"].shape[0]

# number of links
    links =[]

    for i in df["User_messages"]:
        links.extend(extractor.find_urls(i))

    words= []
    for i in df['User_messages']:
        words.extend(i.split())


    return num_messages , len(words) , num_media ,len(links), num_of_deleted


def fetch_mostbusy(df):

    x = df["User"].value_counts()

    return x.head(10)
#word cloud

def create_wordcloud(selected_user,df):


    f = open("stophinglish.txt", 'r')
    stop_words = f.read()

    
    if selected_user != 'Overall analysis':
        df = df[df['User'] == selected_user]

    temp = df[df["User"] != "group notification"]
    temp = temp[temp["User_messages"] != '<Media omitted>\n']
    temp = temp[temp["User_messages"] != "This message was deleted\n"]
    temp = temp[temp["User_messages"] != "You deleted this message\n"]

    def remove_stop(m):
        y = []
        for i in m.lower().split():
            if i not in stop_words:
                y.append(i)
        return " ".join(y)

    # wc = WordCloud(width=1000,height=800,min_font_size=9 ,stopwords = stop_words.split())  we can also use this method
    wc = WordCloud(width=1000,height=800,min_font_size=9 )
    temp["User_messages"] =  temp["User_messages"].apply(remove_stop)

    df_wc = wc.generate(temp["User_messages"].str.cat(sep=" "))

    return df_wc

# most common words
def most_common(selected_user,df):

    f = open("stophinglish.txt", 'r')
    stop_words = f.read()

    if selected_user != 'Overall analysis':
        df = df[df['User'] == selected_user]


    temp = df[df["User"] != "group notification"]
    temp = temp[temp["User_messages"] != '<Media omitted>\n']
    temp=temp[temp["User_messages"] != "This message was deleted\n"]
    temp=temp[temp["User_messages"] != "You deleted this message\n"]

    words= []
    for i in temp['User_messages']:
        for j in i.lower().split():
            if j not in stop_words:
                words.append(j)

    c = Counter(words)
    most_common_df =pd.DataFrame(c.most_common(20))

    return most_common_df

#emoji datafram
def emojifind(selected_user ,df):

    if selected_user != 'Overall analysis':
        df = df[df['User'] == selected_user]


    e = df["User_messages"].str.cat(sep=" ")
    emoj = []
    for i in emoji.emoji_list(e):
        emoj.append(i['emoji'])

    emoj_df = pd.DataFrame((Counter(emoj)).keys() , (Counter(emoj)).values()).reset_index()

    return emoj_df.head(10)

#timline


def montly_user(selected_user,df):

    if selected_user != 'Overall analysis':
        df = df[df['User'] == selected_user]
        

    timeline = df.groupby(["Year" , "month_num" , "Month"]).count()["User_messages"].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline["Month"][i]+ '-'+ str(timeline["Year"][i]))

    timeline["Time"] = time

    return timeline

# weekly active
def weekly_activity(selected_user,df):

    if selected_user != 'Overall analysis':
        df = df[df['User'] == selected_user]

    return df

def heat_activity(selected_user,df):

    if selected_user != 'Overall analysis':
        df = df[df['User'] == selected_user]

    hours_activ = df.pivot_table(values='User_messages',index='Day name',columns='Hour',aggfunc='count').fillna(0)

    return hours_activ