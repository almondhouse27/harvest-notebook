import logging
import random
import requests
import time
import pandas as pd
from collections import Counter
from bs4 import BeautifulSoup
from src.permission import robot_handshake
from src.output import intermediate_save


DELAY = .5
TIMEOUT = 20
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "HarvestNotebook/1.0 (Windows NT 10.0; Win64; x64)"
]
PROXIES = [
    # "http://proxy1.example.com:8080",
    # "http://proxy2.example.com:8080",
    # "http://proxy3.example.com:8080",
    # "http://proxy4.example.com:8080",
]
CHUNK = 5


def harvest(df, output_dir):
    website_words_data = []
    site_specifications_data = []
    chunk_count = 0

    for index, row in df.iterrows():
        category, name, url = row['Category'], row['Name'], row['Url']
        logging.info(f"[{index+1}/{len(df)}] Processing {url} (Category: {category}, Name: {name})")

        if robot_handshake(url, USER_AGENTS, TIMEOUT, PROXIES, DELAY):

            try:
                user_agent = random.choice(USER_AGENTS)
                proxy = random.choice(PROXIES) if PROXIES else None
                headers = {'User-Agent': user_agent}
                proxies = {'http': proxy, 'https': proxy} if proxy else None

                response = requests.get(url, headers=headers, timeout=TIMEOUT, proxies=proxies)
                response.raise_for_status()

                # WEBSITE WORDS ===========================
                word_counts = get_website_words(response.text)
                for word, count in word_counts.items():
                    website_words_data.append({
                        'Url': url,
                        'Word': word,
                        'WordCount': count
                    })
                
                # SITE SPECIFICATIONS =====================
                site_specifications = get_site_specifications(response.text)
                site_specifications_data.append({
                    'Category': category,
                    'Name': name,
                    'Url': url,
                    'WordCount': site_specifications['WordCount'],
                    'ScriptCount': site_specifications['ScriptCount'],
                    'StylesheetCount': site_specifications['StylesheetCount'],
                    'LinkCount': site_specifications['LinkCount'],
                    'FormCount': site_specifications['FormCount'],
                    'ImageCount': site_specifications['ImageCount'],
                    'VideoCount': site_specifications['VideoCount'],
                    'IframeCount': site_specifications['IframeCount'],
                    'MetaDescription': site_specifications['MetaDescription'],
                    'Title': site_specifications['Title'],
                    'CookieStatus': site_specifications['CookieStatus']
                })

                logging.info(f"Successfully processed {url}")

            except requests.RequestException as e:
                logging.error(f"Request error for {url}: {e}")
                
            except Exception as e:
                logging.error(f"Error scraping {url}: {e}")

        else:
            logging.warning(f"Skipping {url} due to robots.txt restrictions.")

        if (index + 1) % CHUNK == 0 or (index + 1) == len(df):
            chunk_count += 1

            if website_words_data:
                intermediate_save(website_words_data, chunk_count, output_dir, "ww")

            if site_specifications_data:

                intermediate_save(site_specifications_data, chunk_count, output_dir, "ss")

        time.sleep(DELAY)
    
    if website_words_data:
        logging.debug(f"Final save: chunk_count={chunk_count}, size={len(website_words_data)}")
        intermediate_save(website_words_data, chunk_count, output_dir, "ww")
    
    if site_specifications_data:
        logging.debug(f"Final save: chunk_count={chunk_count}, size={len(site_specifications_data)}")
        intermediate_save(site_specifications_data, chunk_count, output_dir, "ss")

    logging.info("Scraping completed. Compiling results into DataFrame.")
    website_words = pd.DataFrame(website_words_data)
    return website_words


def get_website_words(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator=' ')
    words = text.split()
    return Counter(words)


def get_site_specifications(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator=' ')
    word_count = len(text.split())
    script_count = len(soup.find_all('script'))
    stylesheet_count = len(soup.find_all('link', rel="stylesheet"))
    link_count = len(soup.find_all('a'))
    form_count = len(soup.find_all('form'))
    image_count = len(soup.find_all('img'))
    video_count = len(soup.find_all('video'))
    iframe_count = len(soup.find_all('iframe'))
    meta_description = soup.find('meta', attrs={'name': 'description'})
    meta_description = meta_description['content'] if meta_description else None
    title = soup.find('title').get_text() if soup.find('title') else None
    cookie_status = 'Yes' if soup.find_all('script', attrs={'src': lambda x: x and 'cookie' in x}) else 'No'

    return {
        'WordCount': word_count,
        'ScriptCount': script_count,
        'StylesheetCount': stylesheet_count,
        'LinkCount': link_count,
        'FormCount': form_count,
        'ImageCount': image_count,
        'VideoCount': video_count,
        'IframeCount': iframe_count,
        'MetaDescription': meta_description,
        'Title': title,
        'CookieStatus': cookie_status
    }
