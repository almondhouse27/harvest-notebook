import logging
import os
import pandas as pd


def clear_bad_data(BAD_DATA):
    open(BAD_DATA, 'w').close()


def write_bad_data(df, BAD_DATA):
    if os.path.exists(BAD_DATA):
        clear_bad_data(BAD_DATA)
        df.to_csv(BAD_DATA, mode='a', header=True, index=False)
    else:
        df.to_csv(BAD_DATA, mode='w', header=True, index=False)


def reset_input_data(file_path, COLUMNS):
    open(file_path, 'w').close()
    with open(file_path, 'w') as f:
        f.write(','.join(COLUMNS) + '\n')


def check_csv_format(df, INPUT, COLUMNS, BAD_DATA):
    logging.error(f"Error: The file {INPUT} is not properly formatted.")

    write_bad_data(df, BAD_DATA)
    logging.info(f"Incorrectly formatted file copied to {BAD_DATA}.")

    reset_input_data(INPUT, COLUMNS)
    logging.info(f"Original file {INPUT} cleared and header row added.")

    print(f"Error: The file {INPUT} is not properly formatted.\n"
          f"Incorrectly formatted file copied to {BAD_DATA}.\n"
          f"Original file {INPUT} cleared and header row added.\n")


def read_csv(INPUT, COLUMNS, BAD_DATA):
    try:
        df = pd.read_csv(INPUT)

        if df.columns.tolist() != COLUMNS:
            check_csv_format(df, INPUT, COLUMNS, BAD_DATA)
            return None

        logging.info(f"CSV file {INPUT} read successfully.")
        return df
    
    except FileNotFoundError:
        logging.error(f"Error: The file {INPUT} was not found.")
    except Exception as e:
        logging.error(f"Error reading file {INPUT}: {e}")