import logging
import os
import subprocess
import sys

def install_requirements():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        logging.info("Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error installing dependencies: {e}")
        
def setup_logging(log_file):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler(log_file),
            #logging.StreamHandler()
        ]
    )
    logging.info("======================================================")
    logging.info(f"Logging setup complete. Logs will be saved to {log_file}.")