import urllib.robotparser
from urllib.parse import urlparse


"""
CHAT GPT FUNCTION
"""
def is_allowed(url, user_agent='*'):

    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(base_url)

    try:

        rp.read()
        return rp.can_fetch(user_agent, url)
    
    except:

        return False
