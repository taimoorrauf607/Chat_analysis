
from urlextract import URLExtract
from collections import Counter
import pandas as pd
import emoji
extract = URLExtract()


# function to get statistics 
def get_stats(select_user,df):
    
    if select_user != 'Overall':
        df = df[df['users']==  select_user]

    total_message = df.shape[0]
    words = [] # words total
    for word in df['message']:
        words.extend(word.split())

    media =df[df['message']=='Files'].shape[0]   # get media files 

    links = []  # get links using extract
    for mess in df['message']:
        links.extend(extract.find_urls(mess))

    return total_message, len(words), media, len(links)

# function for most active user in Chat
def active_user(df):
    x = df['users'].value_counts().head()

    user_percentage = round((df['users'].value_counts()/df.shape[0])*100, 2)
    
    return x, user_percentage

# word cloud
def make_wordcloud(select_user,df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if select_user != 'Overall':
        df = df[df['users']==  select_user]
# remove unuseful messages 
    temp_df = df[df['message']!='Files']
    temp_df=temp_df[temp_df['users']!='Notification']
    # delete stop_words
    def stop_word_del(message):
        words = []
        for message in temp_df['message']:
            for word in message.lower().split():
                if word not in stop_words:
                    words.append(word)
        return " ".join(words)
    
    temp_df['message'] = temp_df['message'].apply(stop_word_del)

    return temp_df['message']

# Remove stop_words from the message using file
def common_words(select_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if select_user != 'Overall':
        df = df[df['users']==  select_user]

# remove useless file and Notifications from messages 
    temp_df = df[df['message']!='Files']
    temp_df=temp_df[temp_df['users']!='Notification']

    words = []
    for message in temp_df['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    
    common_words = pd.DataFrame(Counter(words).most_common(20))
    return common_words

# emojis counter , top_emojis
def emoji_counter(select_user,df):
    if select_user != 'Overall':
        df = df[df['users']==  select_user]

    emojis = []
    for message in df['message']:
        emojis.extend([char for char in message if char in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    top_emoji = pd.DataFrame(Counter(emojis).most_common(10))
    emoji_df = emoji_df.rename({0:'emoji',1:"count"}, axis=1)

    return emoji_df, top_emoji

# Month-year wise activity using a function
def monthly_activity(select_user, df):
    if select_user != 'Overall':
        df = df[df['users']==  select_user]

    month_count =df.groupby(['year','Month',"Day"]).count()['message'].reset_index()

    month_year = []
    for i in range(month_count.shape[0]):
        month_year.append((month_count['Month'][i]+"-"+str(month_count['year'][i])))
    
    month_count['time'] = month_year
    return month_count

# make a bar graph on Days and month to find most busy_month and days
def busy_time(select_user,df):
    if select_user != 'Overall':
        df = df[df['users']==  select_user]

    days = df['Day'].value_counts()
    month = df['Month'].value_counts()

    return days, month

# Make a heatmap on active_time 
def active_time(select_user,df):
    if select_user != 'Overall':
        df = df[df['users']==  select_user]
    
    duration_table = df.pivot_table(index='time',columns='Day',values='message',aggfunc='count').fillna(0)

    return duration_table