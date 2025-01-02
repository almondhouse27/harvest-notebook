import logging
from src.permission import robot_handshake

DELAY = .5
TIMEOUT = 20
USER_AGENTS = [
    "HarvestNotebook/1.0", 
    "AlmondAnalytics/1.0",
    "StudentDataProject/1.0"
]
PROXIES = [
    "http://proxy1.com",
    "http://proxy2.com",
    "http://proxy3.com"
]


def harvest():
    url = ""
    robot_handshake(url, USER_AGENTS, TIMEOUT, PROXIES, DELAY)
    return