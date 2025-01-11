import glob
import logging
import os
import shutil
import subprocess
import pandas as pd
from datetime import datetime


def complete(task):
    print(f"{task} complete!")


def get_versions(STACK):

    # @nestedFunctionStart
    def get_version(command):
        try:
            version = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            version_info = version.stdout.strip() if version.stdout else version.stderr.strip()
            logging.info(f"Version fetched for {command[0]}: {version_info}")
            return version_info
        except Exception as e:
            logging.error(f"Error fetching version for {command}: {e}")
            return f"Error fetching version for {command}: {e}"
        
    # @parentFunctionStart
    versions = {command[0]: get_version(command) for command in STACK}
    logging.info("Completed version retrieval for the stack.")
    return versions


def create_output_directory(OUTPUT):
    try:
        if not os.path.exists(OUTPUT):
            os.makedirs(OUTPUT)

        timestamp = datetime.now().strftime("%y%m%d-%H%M")
        output_dir = os.path.join(OUTPUT, timestamp)
        counter = 1

        while os.path.exists(output_dir):
            output_dir = os.path.join(OUTPUT, f"{timestamp}_{counter}")
            counter += 1

        os.makedirs(output_dir)
        logging.info(f"Output directory created: {output_dir}")
        return output_dir
    
    except Exception as e:
        logging.error(f"Failed to create output directory: {e}")
        return f"Failed to create output directory: {e}"
    

def intermediate_save(website_data, chunk_count, output_dir):
    raw_dir = os.path.join(output_dir, "raw")
    os.makedirs(raw_dir, exist_ok=True)

    file_name = f"website_words_chunk_{chunk_count}.csv"
    file_path = os.path.join(raw_dir, file_name)

    pd.DataFrame(website_data).to_csv(file_path, index=False)

    logging.info(f"Saved chunk {chunk_count} with {len(website_data)} rows to {file_path}")
    print(f"Saved chunk {chunk_count} with {len(website_data)} rows to {file_path}")
    
    website_data.clear()


def stitch_chunks(output_dir):
    raw_dir = os.path.join(output_dir, "raw")
    output_file = os.path.join(output_dir, "website_words.csv")

    chunk_files = glob.glob(os.path.join(raw_dir, "website_words_chunk_*.csv"))
    chunk_files.sort()

    website_words = pd.concat([pd.read_csv(chunk_file) for chunk_file in chunk_files], ignore_index=True)
    website_words.to_csv(output_file, index=False)

    logging.info(f"All chunks stitched together into {output_file}")
    print(f"All chunks stitched together into {output_file}")

    shutil.rmtree(raw_dir)
    logging.info(f"Raw directory and files removed: {raw_dir}")
    print(f"Raw directory and files removed: {raw_dir}")


def process_outputs(output_dir):
    csv_files = glob.glob(os.path.join(output_dir, "*.csv"))

    if not csv_files:
        logging.info(f"No CSV files found in {output_dir}.")
        print(f"No CSV files found in {output_dir}.")
        return

    for file in csv_files:
        try:
            df = pd.read_csv(file)
            sort_columns = df.columns[:2] if len(df.columns) > 1 else df.columns[:1]
            sorted_df = df.sort_values(by=sort_columns.tolist(), kind="mergesort")
            sorted_df.to_csv(file, index=False)
            logging.info(f"Sorted and saved file: {file}")
            print(f"Sorted and saved file: {file}")

        except Exception as e:
            logging.error(f"Error processing file {file}: {e}")
            print(f"Error processing file {file}: {e}")

