import logging
import subprocess

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

def complete(task):
    print(f"{task} complete!")







