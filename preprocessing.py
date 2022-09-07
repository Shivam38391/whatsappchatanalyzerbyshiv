import re
import pandas as pd

def preprocess(data):

    pattern = r"\d{1,2}/\d{1,2}/\d{1,2},\s\d+:\d+\s\w+"
    date_time = re.findall(pattern,data)
    messages = re.split(pattern,data)[1:]

    df= pd.DataFrame({'DATE':date_time, 'MESSAGES':messages})
    df['DATE']= pd.to_datetime(df.DATE )

    users = []
    user_mesages = []

    for x in df["MESSAGES"]:
        entry= re.split(r':\s',x)
        if entry[1:]==[]:
            users.append("group notification")
            user_mesages.append(x)
            
        else:
            users.append(entry[0])
            user_mesages.append(entry[1])


    df['User'] = users
    df['User_messages'] = user_mesages

    df['Year']= df["DATE"].dt.year
    df["month_num"] = df["DATE"].dt.month
    df['Month']= df["DATE"].dt.month_name()
    df['Day']= df["DATE"].dt.day
    df["Day name"] = df["DATE"].dt.day_name()
    df['Hour']= df["DATE"].dt.hour
    df["minutes"]= df["DATE"].dt.minute


    return df