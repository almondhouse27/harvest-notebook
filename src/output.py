import glob as blob
import logging
import os
import shutil
import pandas as pd
from datetime import datetime


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
    

def intermediate_save(data, chunk_count, output_dir, data_type):
    raw_dir = os.path.join(output_dir, "raw")
    os.makedirs(raw_dir, exist_ok=True)

    # file_name = f"website_words_chunk_{chunk_count}.csv"
    if data_type == "ww":
        file_name = f"website_words_chunk_{chunk_count}.csv"
    elif data_type == "ss":
        file_name = f"site_specifications_chunk_{chunk_count}.csv"
    else:
        raise ValueError("Unknown data type")

    file_path = os.path.join(raw_dir, file_name)

    pd.DataFrame(data).to_csv(file_path, index=False)

    logging.info(f"Saved chunk {chunk_count} with {len(data)} rows to {file_path}")
    print(f"Saved chunk {chunk_count} with {len(data)} rows to {file_path}")
    
    data.clear()


def stitch_chunks(output_dir, WORD, SPEC):
    raw_dir = os.path.join(output_dir, "raw")
    website_words_output_file = os.path.join(output_dir, WORD)
    site_specifications_output_file = os.path.join(output_dir, SPEC)

    website_words_chunk_files = blob.glob(os.path.join(raw_dir, "website_words_chunk_*.csv"))
    site_specifications_chunk_files = blob.glob(os.path.join(raw_dir, "site_specifications_chunk_*.csv"))
    
    website_words_chunk_files.sort()
    site_specifications_chunk_files.sort()

    website_words_df = pd.concat([pd.read_csv(chunk_file) for chunk_file in website_words_chunk_files], ignore_index=True)
    website_words_df.to_csv(website_words_output_file, index=False)

    site_specifications_df = pd.concat([pd.read_csv(chunk_file) for chunk_file in site_specifications_chunk_files], ignore_index=True)
    site_specifications_df.to_csv(site_specifications_output_file, index=False)

    logging.info(f"All website words chunks stitched together into {website_words_output_file}")
    print(f"All website words chunks stitched together into {website_words_output_file}")

    logging.info(f"All site specifications chunks stitched together into {site_specifications_output_file}")
    print(f"All site specifications chunks stitched together into {site_specifications_output_file}")

    shutil.rmtree(raw_dir)
    
    logging.info(f"Raw directory and files removed: {raw_dir}")
    print(f"Raw directory and files removed: {raw_dir}")


def basic_report_processing(output_dir):
    csv_files = blob.glob(os.path.join(output_dir, "*.csv"))

    if not csv_files:
        logging.info(f"No CSV files found in {output_dir}. How did you manage to get here?")
        print(f"No CSV files found in {output_dir}.")
        return

    for file in csv_files:
        try:
            df = pd.read_csv(file)
            #df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
            df = df.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))
            sort = df.columns[:2] if len(df.columns) > 1 else df.columns[:1]
            df = df.sort_values(by=sort.tolist(), kind="mergesort")
            df.to_csv(file, index=False)
            logging.info(f"Basic report processing complete for file: {file}")
            print(f"Basic report processing complete for file: {file}")

        except Exception as e:
            logging.error(f"Error processing file {file}: {e}")


def clean_log(clean_summary, output_dir):
    summary = os.path.join(output_dir, "clean.log")

    try:
        with open(summary, 'w') as file:
            file.write(clean_summary)
        print(f"Clean summary saved to {summary}")
        
    except Exception as e:
        print(f"Error saving clean summary to {summary}: {e}")
    