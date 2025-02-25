import os
import json
import random
import logging
import multiprocessing
from datetime import datetime, timedelta
from pathlib import Path

# Configure logging
LOG_FILE = "Flight_data.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Constants
N = 5000  # Number of JSON files to generate
M_RANGE = (50, 100)  # Number of records per file
K_RANGE = (100, 200)  # Total set of cities
NULL_PROBABILITY = (0.005, 0.001)  # Probability of NULL values
DATA_DIR = Path("/tmp/flights")  # Store files in /tmp/flights
NUM_PROCESSES = multiprocessing.cpu_count()  # Parallel processing

# Ensure the directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Generate list of cities
cities = [f"City_{i}" for i in range(max(K_RANGE))]
logging.info(f"Generated {len(cities)} unique cities.")

def get_random_flight_record():
    """Generate a random flight record."""
    date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d')
    origin_city, destination_city = random.sample(cities, 2)
    flight_duration_secs = random.randint(1800, 54000)  # Between 30 min and 15 hours
    passengers_on_board = random.randint(1, 400)

    # Introduce NULL values with given probability
    null_fields = []
    if random.random() < random.uniform(*NULL_PROBABILITY):
        field_to_nullify = random.choice(['date', 'origin_city', 'destination_city', 'flight_duration_secs', 'passengers_on_board'])
        locals()[field_to_nullify] = None
        null_fields.append(field_to_nullify)

    return {
        "date": date,
        "origin_city": origin_city,
        "destination_city": destination_city,
        "flight_duration_secs": flight_duration_secs,
        "passengers_on_board": passengers_on_board
    }, null_fields

def ensure_at_least_one_null(records):
    """Ensure at least one record in the file has a NULL field."""
    null_count = sum(1 for record in records if None in record[0].values())
    if null_count == 0:
        random_record, _ = random.choice(records)
        field_to_nullify = random.choice(list(random_record.keys()))
        random_record[field_to_nullify] = None
        null_count += 1
    return records, null_count

def generate_flight_file(file_index):
    """Generate and save a unique JSON file with flight records."""
    origin_city = random.choice(cities)
    month_year = datetime.now().strftime("%m-%y")
    file_path = DATA_DIR / f"{month_year}-{origin_city}-{file_index}-flights.json"
    num_records = random.randint(*M_RANGE)

    records_with_nulls = [get_random_flight_record() for _ in range(num_records)]
    records, null_count = ensure_at_least_one_null(records_with_nulls)

    records = [record[0] for record in records]  # Extract actual records

    try:
        with open(file_path, 'w') as f:
            json.dump(records, f, indent=4)
        logging.info(f"Generated file {file_index}/{N}: {file_path} with {num_records} records, NULL count: {null_count}, Origin City: {origin_city}")
    except Exception as e:
        logging.error(f"Failed to write file {file_path}: {e}")

def generate_flight_data_parallel():
    """Generate flight data using parallel processing."""
    with multiprocessing.Pool(NUM_PROCESSES) as pool:
        pool.map(generate_flight_file, range(N))

if __name__ == "__main__":
    logging.info("Starting flight data generation using parallel processing.")
    generate_flight_data_parallel()
    logging.info("Flight data generation completed.")
