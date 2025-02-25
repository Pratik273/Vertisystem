# Flight Data Processing Project

## Overview
This project consists of two main tasks:
1. **Flight Data Generation (`task_1.py`)**: Generates synthetic flight data and stores it in JSON format.
2. **Flight Data Analysis (`task_2.py`)**: Processes the generated flight data, cleans it, and performs statistical analysis.

A **main script (`main.py`)** orchestrates the execution of both tasks sequentially.

## Project Structure
```
/your_project_directory
│-- main.py
│-- task_1.py
│-- task_2.py
│-- README.md
│-- main.log
├ -Flight_data.log
|── result.log
│-- /tmp/flights/  # Directory where JSON files are stored
```

## Installation & Prerequisites
Make sure you have **Python 3.x** installed along with the required dependencies.

### Install dependencies (if needed):
```bash
pip install numpy
```

## How to Run the Project
### Step 1: Run the `main.py` script
```bash
python main.py
```
This will:
- Generate flight data (`task_1.py` runs first)
- Process and analyze flight data (`task_2.py` runs next)

### Step 2: Check Log Files for Results
After execution, logs will be saved in the **logs** directory. You can check:
- **`main.log`** → Overall execution logs
- **`Flight_data.log`** → Logs for data generation
- **`result.log`** → Logs for data analysis result

To view logs:
```bash
cat logs/main.log  # On Linux/macOS
or
notepad logs\main.log  # On Windows
```

## Expected Output in Logs
- **Total records processed**
- **Total dirty records ignored**
- **Execution time**
- **Top 25 destination cities and their flight duration stats (AVG & P95 percentile)**
- **City with max passengers arrived and left**

## Troubleshooting
- If you see an error like `Failed to run task_1.py: [WinError 2] The system cannot find the file specified`, ensure `task_1.py` and `task_2.py` exist in the same directory as `main.py`.
- If logs are empty, try running `python task_1.py` and `python task_2.py` separately to debug.

## Notes
- Logs are written both to **log files** and the **console**.
- Data is generated randomly and stored in `/tmp/flights/`.
- Parallel processing is used for both **data generation** and **analysis** for performance optimization.

---
✅ **Now, simply run `python main.py` and check the logs for insights!**
