import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('1.csv')

# Set page title
st.title('YouTube Comments Analysis')

# Display the entire DataFrame
st.subheader('Raw Data:')
st.write(df)

# Best 5 comments based on like count
st.subheader('Best 5 Comments:')
best_comments = df.nlargest(5, 'like_count')
st.write(best_comments)

# Worst 5 comments based on sentiment score
st.subheader('Worst 5 Comments:')
worst_comments = df.nsmallest(5, 'vader_sentiment')
st.write(worst_comments)

# Average sentiment score
avg_sentiment = df['vader_sentiment'].mean()
st.subheader('Average Sentiment Score:')
st.write(avg_sentiment)

# Histogram of sentiment scores
st.subheader('Distribution of Sentiment Scores:')
plt.figure(figsize=(8, 6))
sns.histplot(df['vader_sentiment'], bins=20, kde=True)
plt.xlabel('Sentiment Score')
plt.ylabel('Frequency')
st.pyplot()

# Bar chart of like count by author
st.subheader('Like Count by Author:')
like_count_by_author = df.groupby('author')['like_count'].sum().sort_values(ascending=False)
plt.figure(figsize=(10, 8))
like_count_by_author.plot(kind='bar')
plt.xlabel('Author')
plt.ylabel('Total Like Count')
plt.xticks(rotation=45)
st.pyplot()

# Word cloud of comments
from wordcloud import WordCloud
comment_text = ' '.join(df['translated_text'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(comment_text)
st.subheader('Word Cloud of Comments:')
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
st.pyplot()

