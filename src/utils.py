import logging
import os
import subprocess
from datetime import datetime


def complete(task):
    print(f"{task} complete!")


def get_version(command):
    try:
        version = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        version_info = version.stdout.strip() if version.stdout else version.stderr.strip()
        logging.info(f"Version fetched for {command[0]}: {version_info}")
        return version_info
    
    except Exception as e:
        logging.error(f"Error fetching version for {command}: {e}")
        return f"Error fetching version for {command}: {e}"


def get_versions(STACK):
    versions = {command[0]: get_version(command) for command in STACK}
    logging.info("Completed version retrieval for the stack.")
    return versions


def create_output_directory(OUTPUT):
    try:
        if not os.path.exists(OUTPUT):
            os.makedirs(OUTPUT)

        timestamp = datetime.now().strftime("%y%m%d-%H%M")
        output_directory = os.path.join(OUTPUT, timestamp)
        counter = 1

        while os.path.exists(output_directory):
            output_directory = os.path.join(OUTPUT, f"{timestamp}_{counter}")
            counter += 1

        os.makedirs(output_directory)
        logging.info(f"Output directory created: {output_directory}")
        return output_directory
    
    except Exception as e:
        logging.error(f"Failed to create output directory: {e}")
        return f"Failed to create output directory: {e}"








