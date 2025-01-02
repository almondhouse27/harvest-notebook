import logging
import random
import requests
import time
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

def robot_handshake(url, USER_AGENTS, TIMEOUT, PROXIES, DELAY):
    
    parsed_url = urlparse(url)

    if not parsed_url.scheme or not parsed_url.netloc:
        logging.error(f"Invalid URL: {url}")
        return False
    
    user_agent = random.choice(USER_AGENTS)
    proxies = random.choice(PROXIES) if PROXIES else None
    base_url = '{0.scheme}://{0.netloc}'.format(urlparse(url))
    robots_url = f'{base_url}/robots.txt'

    try:
        headers = {'User-Agent': user_agent}
        response = requests.get(robots_url, headers=headers, timeout=TIMEOUT, proxies=proxies)
        response.raise_for_status()

        robert = RobotFileParser()
        robert.parse(response.text.splitlines())

        if robert.can_fetch(user_agent, url):
            logging.info(f"Permission granted to scrape: {url}")
            time.sleep(DELAY)
            return True
        else:
            logging.warning(f"Permission denied to scrape: {url}")
            time.sleep(DELAY)
            return False
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching robots.txt from {robots_url}: {e}")
        return False
    except Exception as e:
        logging.error(f"Error parsing robots.txt for {url}: {e}")
        return False