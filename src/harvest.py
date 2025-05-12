import requests
from bs4 import BeautifulSoup, Comment
from collections import Counter
import time
import re


STOPWORDS = set([
    "the", "and", "for", "are", "but", "not", "you", "all", "any", "can", "was",
    "with", "his", "her", "its", "has", "have", "had", "this", "that", "from",
    "they", "your", "their", "will", "would", "there", "what", "when", "where",
    "how", "why", "who", "been", "them", "more", "some", "could", "than", "then",
    "out", "get", "about", "which", "each", "also", "she", "him", "our", "one", "two"
])


def harvest_url(url):

    try:

        start_time = time.time()
        response = requests.get(url)
        response_time = time.time() - start_time
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        text = soup.get_text()
        text = text.lower()

        words = text.split()
        filtered_words = [word for word in words if word not in STOPWORDS]
        word_count = len(filtered_words)
        unique_word_count = len(set(filtered_words))
        
        title = soup.title.string.strip() if soup.title else ''
        stylesheet_count = len(soup.find_all('link', rel='stylesheet'))
        script_count = len(soup.find_all('script'))
        link_count = len(soup.find_all('a'))

        results = {
            'url': url,
            'title': title,
            'total_word_count': word_count,
            'unique_word_count': unique_word_count,
            'response_time': response_time,
            'stylesheet_count': stylesheet_count,
            'script_count': script_count,
            'link_count': link_count
        }

        return results

    except requests.exceptions.RequestException as e:

        print(f"Error fetching {url}: {e}")

        return {
            'url': url,
            'title': '',
            'total_word_count': 0,
            'unique_word_count': 0,
            'response_time': None,
            'stylesheet_count': 0,
            'script_count': 0,
            'link_count': 0
        }
    

def extract_word_counts(url):

    try:

        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        for element in soup(['script', 'style']):
            element.decompose()

        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()

        text = soup.get_text(separator=' ')
        text = text.lower()
        words = re.findall(r'\b[a-z]{3,}\b', text)  # Only words of 3+ letters
        filtered_words = [word for word in words if word not in STOPWORDS]
        word_counts = Counter(filtered_words)

        results = [
            {
                'url': url, 
                'word': word, 
                'word_count': count
            } for word, count in word_counts.items()
        ]

        return results

    except requests.exceptions.RequestException as e:
        
        print(f"Error fetching {url}: {e}")
        return []