from flask import Flask, request, jsonify, render_template
import requests
import google.generativeai as genai
from urllib.parse import urlencode

app = Flask(__name__)

# News API Configuration
NEWS_API_KEY = "5c79806ac8d3477b843ffb4f52292802"  # Replace with your actual news API key
NEWS_BASE_URL = "https://api.worldnewsapi.com/search-news"

# Gemini API Configuration
GENAI_API_KEY = "AIzaSyDObyFQNBXvBwdwcyEe_02rkKOvpfcZmd0"  # Your new Gemini API key  # Replace with your actual Gemini API key
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")  # Ensure this model is available for your API key

def fetch_news(api_key, keyword, language='en'):
    """
    Fetches news articles based on the keyword and language.
    """
    params = {
        "api-key": api_key,
        "text": keyword,
        "language": language,
    }
    url = NEWS_BASE_URL + "?" + urlencode(params)

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (non-200 status codes)
        news_data = response.json()

        if 'news' in news_data and news_data['news']:
            return news_data['news']
        else:
            return []

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []

def summarize_with_gemini(article, content_type, tone):
       """
       Summarizes the article using Gemini with the desired tone and style.
       """
       # Check if 'content' is available in the article
       content = article.get('content', article.get('description', 'N/A'))

       prompt = (
           f"Summarize the following news article and rewrite it as a {content_type} "
           f"in a {tone} tone.\n\n"
           f"Title: {article.get('title', 'N/A')}\n"
           f"Content: {content}\n\n"  # Use content here
           f"Output:"
       )

       try:
           print("Prompt sent to Gemini:", prompt)  # Debugging line
           response = model.generate_content(prompt)
           return response.text.strip()
       except Exception as e:
           print(f"Error using Gemini for summarization: {e}")
           return "Error summarizing the article."
       
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    keyword = data.get('keyword')
    content_type = data.get('contentType')
    tone = data.get('tone')

    # Fetch news articles
    articles = fetch_news(NEWS_API_KEY, keyword)

    # Process articles and summarize
    processed_articles = []
    for article in articles:
        summary = summarize_with_gemini(article, content_type, tone)
        processed_articles.append({
            'title': article.get('title', 'N/A'),
            'published_date': article.get('published_date', 'N/A'),
            'source_name': article.get('source_name', 'N/A'),
            'url': article.get('url', 'N/A'),
            'summary': summary
        })

    return jsonify({'articles': processed_articles})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)