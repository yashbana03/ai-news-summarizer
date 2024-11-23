# Import necessary libraries
import streamlit as st
import requests
from transformers import pipeline

# Set up the Streamlit app
st.title("AI-Powered News Summarizer")
st.sidebar.title("Options")

# Sidebar options
option = st.sidebar.selectbox("Choose Action", ["Search News", "View Summaries"])

# NewsAPI base URL
NEWS_API_URL = "https://newsapi.org/v2/everything"  # NewsAPI endpoint

# Set up the summarization pipeline using Hugging Face Transformers
summarizer = pipeline("summarization")

# Function to fetch news from NewsAPI
def fetch_news(keyword):
    """Fetch news articles from NewsAPI based on a keyword."""
    # Replace with your actual API key
    API_KEY = "8af0b2b3133b4816bc1a6af07991786f"
    
    # Endpoint with query parameters
    response = requests.get(
        NEWS_API_URL,
        params={
            "q": keyword,  # The search query
            "apiKey": API_KEY,  # API key for authentication
            "language": "en",  # Optional: Filter news by language
            "pageSize": 5       # Optional: Limit number of results
        }
    )
    
    # Handle the response
    if response.status_code == 200:
        return response.json().get("articles", [])  # Return the list of articles
    else:
        st.error("Failed to fetch news. Please try again later.")
        return []

# Function to summarize text
def summarize_article(content):
    """Summarizes a given news article."""
    summary = summarizer(content, max_length=150, min_length=30, do_sample=False)
    return summary[0]["summary_text"]

# Main app logic
if option == "Search News":
    # User inputs a keyword
    keyword = st.text_input("Enter a topic or keyword:")
    if st.button("Search"):
        articles = fetch_news(keyword)
        if articles:
            st.subheader(f"News Articles for '{keyword}':")
            for article in articles:
                st.markdown(f"**{article['title']}**")
                st.write(article['description'])  # Use 'description' for a short summary
                with st.expander("View Full Content"):
                    st.write(article['content'] or "No content available.")
                with st.expander("View AI Summary"):
                    summary = summarize_article(article['content'] or article['description'])
                    st.write(summary)

elif option == "View Summaries":
    st.write("This section can show saved summaries or summaries based on trends.")
    # Future: Extend functionality to save and manage summaries.

# Footer
st.sidebar.markdown("Powered by Streamlit and NewsAPI")
