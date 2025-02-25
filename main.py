import os
import subprocess
import logging

# Configure logging
LOG_FILE = "main.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Get the absolute path of the current directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths to the scripts
TASK_1_PATH = os.path.join(SCRIPT_DIR, "task_1.py")
TASK_2_PATH = os.path.join(SCRIPT_DIR, "task_2.py")


def run_script(script_path):
    """Run a Python script and log the output."""
    logging.info(f"Starting {script_path}...")

    if not os.path.exists(script_path):
        logging.error(f"Script not found: {script_path}")
        return

    try:
        result = subprocess.run(
            ["python", script_path], capture_output=True, text=True, check=True
        )
        logging.info(f"Successfully executed {script_path}")
        logging.info(f"Output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to run {script_path}: {e}")
        logging.error(f"Error Output:\n{e.stderr}")


if __name__ == "__main__":
    logging.info("Main script execution started.")

    # Run both scripts sequentially
    run_script(TASK_1_PATH)
    run_script(TASK_2_PATH)

    logging.info("All tasks completed successfully.")
