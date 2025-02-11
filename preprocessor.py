import pandas as pd
import re
import numpy as np
# pre-processing
def preprocessing(text):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}\s[apAP][mM]\s-'
    messages = re.split(pattern,text)[1:]
    dates = re.findall(pattern,text)

    # make a good format of Dates column
    df = pd.DataFrame({'Dates':dates,'messages':messages})

    name = []
    message = []
    for mess in df['messages']:
        text = re.split('([\w\W]+?):\s',mess)
        if text[1:]:
            name.append(text[1])
            message.append(text[2])
        else:
            name.append('Notification')
            message.append(text[0])
    
    df['users'] = name
    df['users'] =df['users'].str.replace('زندگی 🥹','Taimoor')
    
    df['message'] = message
    df['message']=df['message'].str.replace('\n','')
    df['message']=df['message'].str.replace('<Media omitted>','Files')

    df['Dates'] =df['Dates'].str.replace('-','')
    df['Dates'] =df['Dates'].str.replace(',','')
    # df['Dates']=df['Dates'].str.replace(r'\s+', ' ', regex=True).str.strip()
    df['Dates']=pd.to_datetime(df['Dates'])

    # fetch columns from Dates column
    df['day'] =df['Dates'].dt.day
    df['year'] =df['Dates'].dt.year
    df['Day'] =df['Dates'].dt.day_name()
    df['month'] =df['Dates'].dt.month
    df['Month'] =df['Dates'].dt.month_name()
    df['Hour'] =df['Dates'].dt.hour
    df['Minute'] =df['Dates'].dt.minute
    # Most active time 
    duration = []
    for hour in df[['Day','Hour']]['Hour']:
        if hour ==23:
            duration.append(str(hour)+"-"+str("00"))
        elif hour==0:
            duration.append(str('00'+'-'+str(hour+1)))
        else:
            duration.append(str(hour)+'-'+str(hour+1))

    df['time']=duration
    # df['year'] =np.where((df['Month'] != 'January') & (df['year'] == 2025), 2024, df['year'])

    return df.drop(['messages','Dates'],axis=1)