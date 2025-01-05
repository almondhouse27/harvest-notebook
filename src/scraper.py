import logging
import os
import random
import requests
import time
import pandas as pd
from collections import Counter
from bs4 import BeautifulSoup
from src.permission import robot_handshake


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
CHUNK = 20


def get_website_words(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator=' ')
    words = text.split()
    return Counter(words)


def intermediate_save(website_data, chunk_count, reports_directory):
    raw_directory = os.path.join(reports_directory, "raw")
    os.makedirs(raw_directory, exist_ok=True)
    file_name = f"website_words_chunk_{chunk_count}.csv"
    file_path = os.path.join(raw_directory, file_name)
    pd.DataFrame(website_data).to_csv(file_path, index=False)
    logging.info(f"Saved chunk {chunk_count} with {len(website_data)} rows to {file_path}")
    print(f"Saved chunk {chunk_count} with {len(website_data)} rows to {file_path}")
    website_data.clear()


def harvest(df, reports_directory):
    website_data = []
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
                    website_data.append({
                        'Url': url,
                        'Word': word,
                        'WordCount': count
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
            intermediate_save(website_data, chunk_count, reports_directory)

        time.sleep(DELAY)

    logging.info("Scraping completed. Compiling results into DataFrame.")
    website_words = pd.DataFrame(website_data)
    return website_words