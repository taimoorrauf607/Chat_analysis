import seaborn as sns
import preprocessor
import helper
import streamlit as st
import matplotlib.pyplot as plt

# Sidebar title
st.sidebar.title("WhatsApp Chat Analyzer")

# Maintain button clicks using session state
if "show_analysis" not in st.session_state:
    st.session_state.show_analysis = False

if "show_timeline" not in st.session_state:
    st.session_state.show_timeline = False

# File uploader
uploaded_file = st.sidebar.file_uploader("Choose file from PC")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')

    # Preprocess data
    df = preprocessor.preprocessing(data)
    st.dataframe(df)

    # Fetch unique users
    user_list = df['users'].unique().tolist()
    user_list.sort()
    user_list.insert(0, 'Overall')

    # Select user for analysis
    select_user = st.sidebar.selectbox("Select User for Analysis", user_list)

    # Show Analysis Button
    if st.sidebar.button("Show Analysis"):
        st.session_state.show_analysis = True

    if st.session_state.show_analysis:
        # Display key statistics
        col1, col2, col3, col4 = st.columns(4)
        total_messages, words, media, link = helper.get_stats(select_user, df)

        with col1:
            st.header("Total Messages")
            st.title(total_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Shared Files")
            st.title(media)

        with col4:
            st.header("Shared Links")
            st.title(link)

        # Active user analysis
        if select_user == 'Overall':
            st.title("Most Active Users")
            x, user_per = helper.active_user(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='cornflowerblue')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(user_per)

        # Common words graph
        common_words = helper.common_words(select_user, df)
        fig, ax = plt.subplots()
        ax.barh(common_words[0], common_words[1])
        st.title("Most Common Words")
        st.pyplot(fig)

        # Emoji analysis
        emoji_df, top_emoji = helper.emoji_counter(select_user, df)
        
        col1, col2 = st.columns(2)

        with col1:
            fig, ax = plt.subplots()
            ax.pie(top_emoji.iloc[:, 1],labels=top_emoji.iloc[:,0],explode=[0.1,0.1,0,0,0,0,0,0,0,0])
            ax.legend(title='emoji')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.dataframe(emoji_df)

    # Most busy Time zone Analysis
    st.title("Most busy Time")
    col1, col2 = st.columns(2)
    days, month = helper.busy_time(select_user,df)

    with col1:
        
        plt.figure(figsize=(12, 6))
        plt.subplot(121)
        plt.bar(days.index,days.values)
        plt.xticks(rotation='vertical')
        st.pyplot(plt)
    
    with col2:
        days = helper.busy_time(select_user,df)
        plt.figure(figsize=(12, 6))
        plt.subplot(121)
        plt.bar(month.index,month.values, color='g')
        plt.xticks(rotation='vertical')
        st.pyplot(plt)

    # Show Timeline Button (only enabled after analysis)
    if st.session_state.show_analysis:
    #     Select timeline before the button
        month_count= helper.monthly_activity(select_user, df)
        plot_list = ['line', 'bar', 'barh', 'hist','box', 'kde']
        plot_type = st.selectbox("Choose a Plot Type", plot_list)
    # Show Timeline Button
    if st.sidebar.button("Timeline Analysis"):
        st.session_state.show_timeline = True

    if st.session_state.show_timeline:
            # plot a graph for time = month-year 
            plt.figure(figsize=(10, 5))
            plt.subplot(121)
            color_input = st.text_input("Enter color for Your Graph")
            colors = [c.strip() for c in color_input.split(",") if c.strip()] if color_input else ["black"]# Process color input
            month_count.plot('time', 'message', kind=plot_type, color=colors)
            plt.xticks(rotation='vertical')
            st.pyplot(plt)
            # plot heatmap for most active time
            st.title("Activity Time Graph")
            active_time = helper.active_time(select_user,df)
            plt.figure(figsize=(18,8))
            sns.heatmap(active_time)
            st.pyplot(plt)
