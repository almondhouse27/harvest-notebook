import os
import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob

nltk_check = False


def advanced_report_processing(output_dir, WORD, SPEC):
    global nltk_check

    if not nltk_check:
        nltk.download('stopwords', quiet=True)
        nltk.download('punkt', quiet=True)
        nltk_check = True

    website_words = os.path.join(output_dir, WORD)
    advanced_website_words(website_words)

    site_specifications = os.path.join(output_dir, SPEC)
    advanced_site_specifications(site_specifications)


def advanced_website_words(website_words):
    df = pd.read_csv(website_words)
    stop_words = set(stopwords.words('english'))
    
    df['Word'] = df['Word'].apply(lambda x: x.translate(str.maketrans('', '', string.punctuation)).strip())
    
    df = df.dropna(subset=['Word'])
    df = df[df['Word'].str.strip() != '']
    
    df['Tokenized'] = df['Word'].apply(lambda x: [word for word in word_tokenize(str(x)) if word.lower() not in stop_words])
    
    df.to_csv(website_words, index=False)
    print(f"Processed website words saved to {website_words}")

    tokens_df = df[['Url', 'Tokenized']].explode('Tokenized').dropna()
    tokens_df['Tokenized'] = tokens_df['Tokenized'].str.lower()
    
    tokens_df = tokens_df.drop_duplicates().sort_values(by='Tokenized')
    tokens_df = tokens_df.rename(columns={'Tokenized': 'Token'})

    summary = os.path.join(os.path.dirname(website_words), 'tokens.csv')
    tokens_df.to_csv(summary, index=False)
    print(f"Tokens saved to {summary}")


def advanced_site_specifications(site_specifications):
    df = pd.read_csv(site_specifications)