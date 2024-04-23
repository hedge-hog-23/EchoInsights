import streamlit as st
import pandas as pd
import googleapiclient.discovery
from googleapiclient.discovery import build
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import base64
import io

# Function to fetch video comments
def fetch_comments(video_id):
    # Your code to fetch comments here

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyB47XVqTefMFpRGzMavn1KMc9W1Jf8BrCg"

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.commentThreads().list(
    part="snippet",
    videoId=video_id,
    maxResults=100
    )   
    response = request.execute()

    comments = []

    for item in response['items']:
      comment = item['snippet']['topLevelComment']['snippet']
      comments.append([
        comment['authorDisplayName'],
        comment['publishedAt'],
        comment['updatedAt'],
        comment['likeCount'],
        comment['textDisplay']
      ])

    df = pd.DataFrame(comments, columns=['author', 'published_at', 'updated_at', 'like_count', 'text'])
    
    return df

# Function to translate comments
def translate_comments(df):
    # Your code to translate comments here
    from googletrans import Translator
    def translate_text(text, src='auto', dest='en'):
      translator = Translator()
      translated_text = translator.translate(text, src=src, dest=dest)
      return translated_text.text
    # Apply translation to the 'text' column
    df['translated_text'] = df['text'].apply(lambda x: translate_text(x))
    return df

# Function to perform sentiment analysis
def analyze_sentiment(df):
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    # Function to perform sentiment analysis using VADER
    def get_vader_sentiment(text):
      analyzer = SentimentIntensityAnalyzer()
      sentiment_score = analyzer.polarity_scores(text)
      # We extract the compound score which represents the overall sentiment
      return sentiment_score['compound']
    # Apply sentiment analysis to the 'translated_text' column
    df['vader_sentiment'] = df['translated_text'].apply(get_vader_sentiment)
    return df


# Function to generate word cloud
def generate_wordcloud(df_column):
    comment_text = ' '.join(df_column)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(comment_text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

def input_page():
    st.title("YouTube Sentiment Analysis - Input")

    # Get YouTube video link from user
    youtube_link = st.text_input("Enter YouTube video link:")
    if st.button("Analyze") and youtube_link:
        # Extract video ID from the link
        video_id = youtube_link.split("=")[-1]
        # Set query parameters to navigate to the next page
        st.session_state["query_params"] = {"youtube_link": youtube_link, "video_id": video_id}

def result_page():
    st.title("YouTube Sentiment Analysis - Results")

    if st.button("Home"):
        # Clear session state
        st.session_state.clear()
        # Redirect to input page
        input_page()

    # Get video ID from query parameters
    query_params = st.session_state.get("query_params", {})
    youtube_link = query_params.get("youtube_link", "")
    video_id = query_params.get("video_id", "")

    

    # Fetch comments
    df = fetch_comments(video_id)
    st.subheader("Fetched Comments")
    # Display selected columns' heads in Streamlit
    st.write(df.head(15))

    # Translate comments
    translated_comments = translate_comments(df)
    selected_columns = ['text', 'translated_text']
    selected_df = df[selected_columns]
    st.subheader("Translated Comments")
    st.write(selected_df.head(15))

    # Perform sentiment analysis
    sentiment_analysis = analyze_sentiment(translated_comments)
    selected_columns = ['author','text', 'translated_text','vader_sentiment']
    selected_df = df[selected_columns]
    # Display top 10 comments with sentiments
    st.subheader("Top 10 Comments with Sentiments")
    st.write(selected_df.head(10))

    # Display overall sentiment
    overall_sentiment = sentiment_analysis['vader_sentiment'].mean()
    st.subheader("Overall Sentiment")
    st.write(f"Overall sentiment: {overall_sentiment}")

    # Generate and display word cloud
    st.subheader("Word Cloud")
    generate_wordcloud(translated_comments['text'])





def main():
    # Render the appropriate page based on query parameters
    if st.session_state.get("query_params"):
        result_page()
    else:
        input_page()

if __name__ == "__main__":
    main()    