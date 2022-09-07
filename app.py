import streamlit as st
import preprocessing,helper
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px 
import time


st.sidebar.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTc1ImonWhZlgau0PiWRBhWd0eLHSv_I7LZ1A&usqp=CAU' , width=300 )
st.sidebar.title("WELCOME To Whatsapp chat Analyzer :smile:")

st.sidebar.header(' Please uploade *.txtfile of your chat without media *' )
st.sidebar.text("* This code only support 12hours format of chat")

uploaded_file = st.sidebar.file_uploader("Choose a file")

# if st.sidebar.button("Show DataFrame of chat"):

if uploaded_file is not None:
        # To read file as bytes:
    byte = uploaded_file.getvalue()
    data = byte.decode('utf-8')

    df = preprocessing.preprocess(data)

          #fetch users
    user_list = df['User'].unique().tolist()
    user_list.remove('group notification')
    user_list.insert(0, "Overall analysis")

    selected_user = st.sidebar.selectbox('Show analysis wrt', user_list)

    if st.sidebar.button("Click me "):
        st.write("Pleasewait.....")
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.02)
            progress.progress(i+1)

        st.markdown('''# Analysis wrt '''+ selected_user +'*')

        num,num_words, num_media, num_links,num_of_deleted = helper.fetch(selected_user, df)

        col1, col2, col3, col4 ,col5 = st.columns(5)

        with col1:
            st.subheader("Total messages")
            st.subheader(num)

        with col2:
            st.subheader("Total words ")
            st.subheader(num_words)

        with col3:
            st.subheader("Media shared")
            st.subheader(num_media)

        with col4:
            st.subheader("Links shared")
            st.subheader(num_links)

        with col5:
            st.subheader("Deleted messages")
            st.markdown(num_of_deleted)


        #timeline

        timeline = helper.montly_user(selected_user,df)
        st.title("Monthly Traffic")
        st.write("This line chart graph show the frequency of messages from the starting of group till now ")

        fig = px.line(x= 'Time' , y ='User_messages', data_frame = timeline)
        fig.update_layout(paper_bgcolor = "black")
        # fig, ax = plt.subplots(figsize=(25,7))
        # sns.lineplot(x= timeline["Time"] ,y = timeline["User_messages"])
        # ax.grid(True)
        # plt.xticks(rotation = "vertical")
        st.plotly_chart(fig)

        # most busy days

        wdf = helper.weekly_activity(selected_user,df)
        st.title("Busy days in week")
        st.text("This graph show the days in week where chating frequency is high")
        fig, ax = plt.subplots()
        sns.countplot(x="Day name", data = wdf, palette='prism')
        plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
        ax.grid(True)
        st.pyplot(fig)
        
    
        #finding bussiestuser
        if selected_user == 'Overall analysis': # its only applicable on gouplevel
            # st.title("Top 10 busy users")

            x = helper.fetch_mostbusy(df)

            col1, col2 = st.columns(2)
            #seabornplot

            with col1:
                st.title("Top 10 busy users")
                st.text("Most Chatty peoples")
                fig, ax = plt.subplots()
                sns.barplot(x=x.values,y = x.index)
                ax.grid(True)
                st.pyplot(fig)

            with col2:
                st.header("Percentage%  of top 10 users")
                fig, ax = plt.subplots()
                plt.pie(x.values, labels = x.index, autopct='%1.2f%%',shadow=True)
                st.pyplot(fig)

            # wprd cloud
        st.title("WORD CLOUD :cloud:")
        st.text("Word Clouds display the most prominent or frequent words used in a chat")
        st.subheader("Words used in group ["+ selected_user+']')
        df_wc = helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        plt.axis("off")
        ax.imshow(df_wc)
        st.pyplot(fig)


        # most common words
        st.header("Most common words")
        st.title("Bar chart of Popular words")
        most_common_df = helper.most_common(selected_user,df)
        fig, ax = plt.subplots()
        sns.barplot(x = most_common_df[1], y = most_common_df[0] ,palette='prism_r')
        # ax.barh(most_common_df[0],most_common_df[1])
        ax.grid(True)
        st.pyplot(fig)

        emoj_df = helper.emojifind(selected_user,df)
        st.title("Top 10 Emojis ["+ selected_user+']')
        st.text("Pie chart of Commonly used emojies")
        fig = px.pie(emoj_df , values = "index" , names = 0 )
        fig.update_layout(paper_bgcolor = "black")

        st.write(fig)



        mdf = helper.weekly_activity(selected_user,df)
        st.title("Busy month[" + selected_user +']')
        st.text("This graph show the month where chating frequency is high")
        fig, ax = plt.subplots()
        sns.countplot(x="Month", data = wdf, palette='prism')
        plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
        plt.xticks(rotation= 'vertical')
        ax.grid(True)
        st.pyplot(fig)

        st.title("Hourly activity Heatmap")
        st.text("This is a heatmap shows busy hours, lighter shades means the high messages frequency ")
        hour_activ = helper.heat_activity(selected_user,df)
        fig, ax = plt.subplots(figsize=(20,8))
        
        sns.heatmap(hour_activ)
        st.pyplot(fig)

    st.sidebar.header("Created by Shivam sharma")
    st.sidebar.subheader('Contact:'+"shivamsharma38391@gmail.com")
    st.sidebar.subheader("LINKEDIN profile:")
    st.sidebar.write("https://www.linkedin.com/in/shivam-sharma-6499061a9/")
    st.sidebar.subheader("Github Profile")
    st.sidebar.write("https://github.com/Shivam38391")
    st.sidebar.text("Special thanks to Nitish sir")