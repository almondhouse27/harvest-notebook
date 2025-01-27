import os
import json
import logging
import shutil
from datetime import datetime


def process_diagnostic_log(LOG, ARCHIVE, output_dir):
    start_time = None
    end_time = None
    total_duration = 0
    urls_attempted = []
    urls_skipped = []
    url_process_durations = []
    timed_out_count = connection_retry_count = 0
    info_count = debug_count = warning_count = error_count = 0
    current_url_start_time = None
    current_url = None

    with open(LOG, 'r') as f:

        for line in f:
            timestamp, log_level, message = parse_log_line(line)

            if start_time is None:
                start_time = timestamp

            end_time = timestamp

            if log_level == "INFO":
                info_count += 1
            elif log_level == "DEBUG":
                debug_count += 1
            elif log_level == "WARNING":
                warning_count += 1
            elif log_level == "ERROR":
                error_count += 1
                if "Read timed out" in message:
                    timed_out_count += 1
                elif "Max retries exceeded" in message:
                    connection_retry_count += 1

            if "Processing" in message:
                url = extract_url(message)
                urls_attempted.append(url)
                current_url = url
                current_url_start_time = timestamp
            if "Skipping" in message:
                url = extract_url(message)
                urls_skipped.append(url)
            if "Successfully processed" in message and current_url:
                process_time = calculate_time_difference(current_url_start_time, timestamp)
                url_process_durations.append(process_time)
                current_url = None

        avg_url_process_duration = (
            round(sum(url_process_durations) / len(url_process_durations), 2) if url_process_durations else 0
        )

        total_duration = (
            calculate_time_difference(start_time, end_time) if start_time and end_time else 0
        )

        diagnostic_log_data = {
            "Log":{
                "StartTime": start_time,
                "EndTime": end_time,
                "Duration": total_duration,
                "UrlsAttempted": len(urls_attempted),
                "UrlsSkipped": len(urls_skipped),
                "AvgUrlProcessDuration": avg_url_process_duration,
                "TimedOutCount": timed_out_count,
                "ConnectionRetryCount": connection_retry_count,
                "InfoCount": info_count,
                "DebugCount": debug_count,
                "WarningCount": warning_count,
                "ErrorCount": error_count,
            }
        }

        output_file = os.path.join(output_dir, 'diagnostic_log.json')
        with open(output_file, 'w') as json_file:
            json.dump(diagnostic_log_data, json_file, indent=4)

        logging.info(f"Scraping report generated and saved to {output_file}")
        logging.info(f"Log file archived and clearing.")

        with open(LOG, 'r') as log_file:
            with open(ARCHIVE, 'a') as archive_file:
                archive_file.write(log_file.read())

        transfer_app_log(LOG, output_dir)
        
        with open(LOG, 'w'):
            pass

        return diagnostic_log_data
    

def parse_log_line(line):
    parts = line.split(' - ', 2)
    timestamp_str = parts[0]
    log_level = parts[1]
    message = parts[2].strip() if len(parts) > 2 else ""
    return timestamp_str, log_level, message


def extract_url(message):
    url_start = message.find("https://")
    if url_start != -1:
        url_end = message.find(" ", url_start)
        return message[url_start:url_end] if url_end != -1 else message[url_start:]
    return ""


def calculate_time_difference(start_time_str, end_time_str):
    start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S,%f")
    end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S,%f")
    return (end_time - start_time).total_seconds()


def transfer_app_log(LOG, output_dir):
    transfer = os.path.join(output_dir, "app.log")
    shutil.copy(LOG, transfer)
    logging.info(f"Copied {LOG} to {transfer}")
    print(f"Copied {LOG} to {transfer}")