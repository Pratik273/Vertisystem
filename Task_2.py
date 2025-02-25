import os
import json
import logging
import multiprocessing
import time
import numpy as np
from pathlib import Path
from collections import defaultdict

# Configure logging
LOG_FILE = "result.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Constants
DATA_DIR = Path("/tmp/flights")
NUM_PROCESSES = multiprocessing.cpu_count()

def process_file(file_path):
    """Process a single JSON file to extract required statistics."""
    try:
        with open(file_path, 'r') as f:
            records = json.load(f)
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return []

    processed_records = []
    for record in records:
        if None in record.values():  # Dirty record
            continue
        processed_records.append(record)

    return processed_records

def analyze_flight_data():
    """Analyze all JSON files and compute required statistics."""
    start_time = time.time()

    if not DATA_DIR.exists():
        logging.error("Data directory does not exist.")
        return

    files = list(DATA_DIR.glob("*.json"))
    total_files = len(files)
    logging.info(f"Found {total_files} files for analysis.")

    total_records = 0
    dirty_records = 0
    flight_durations = defaultdict(list)
    city_passenger_counts = defaultdict(int)

    # Use multiprocessing to process files in parallel
    with multiprocessing.Pool(NUM_PROCESSES) as pool:
        results = pool.map(process_file, files)

    # Consolidate results
    for records in results:
        total_records += len(records)
        for record in records:
            flight_durations[record['destination_city']].append(record['flight_duration_secs'])
            city_passenger_counts[record['origin_city']] -= record['passengers_on_board']
            city_passenger_counts[record['destination_city']] += record['passengers_on_board']

    # Compute top 25 destination cities with highest flight volume
    top_25_cities = sorted(flight_durations.keys(), key=lambda city: len(flight_durations[city]), reverse=True)[:25]

    duration_stats = {}
    for city in top_25_cities:
        durations = flight_durations[city]
        duration_stats[city] = {
            "AVG": np.mean(durations),
            "P95": np.percentile(durations, 95)
        }

    # Find cities with max passengers arrived and left
    max_arrival_city = max(city_passenger_counts, key=city_passenger_counts.get)
    max_departure_city = min(city_passenger_counts, key=city_passenger_counts.get)

    # Log results
    run_duration = time.time() - start_time
    logging.info(f"Total records processed: {total_records}")
    logging.info(f"Total dirty records ignored: {dirty_records}")
    logging.info(f"Analysis completed in {run_duration:.2f} seconds")
    logging.info(f"Top 25 cities with flight duration stats: {duration_stats}")
    logging.info(f"City with max passengers arrived: {max_arrival_city} ({city_passenger_counts[max_arrival_city]} passengers)")
    logging.info(f"City with max passengers left: {max_departure_city} ({abs(city_passenger_counts[max_departure_city])} passengers)")

    print("Analysis complete. Check logs for details.")

if __name__ == "__main__":
    logging.info("Starting flight data analysis.")
    analyze_flight_data()
    logging.info("Flight data analysis completed.")