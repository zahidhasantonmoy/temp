import requests
import time
import json
from typing import Set

# Configuration
DELAY_SECONDS = 2  # Delay between requests (adjust to avoid rate-limiting, e.g., 5-10 seconds)
BASE_URL = "https://www.bd.airtel.com/free-msisdn/get-msisdn-list"  # Verified from DevTools
OUTPUT_FILE = "airtel_numbers.txt"
MAX_RETRIES = 3  # Max retries per request
RETRY_BACKOFF = 5  # Seconds to wait before retrying after failure

# Headers (mimic browser)
headers = {
    "Content-Type": "application/json",
    "Origin": "https://www.bd.airtel.com",
    "Referer": "https://www.bd.airtel.com/en/sim-services",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    # Paste cookies from DevTools here
    "Cookie": ""  # E.g., "NEXT_LOCALE=en; __Host-authjs.csrf-token=376e21d147795686...; TS018b3528=01c9bf80bb..."
    # Add other headers if needed, e.g., "X-CSRF-Token": "abc123"
}

# Request payload
payload = {
    "msisdn": None,
    "brand": "AIRTEL",
    "simCategory": "PREPAID"
}

# Initialize session to persist cookies
session = requests.Session()
session.headers.update(headers)

# Initialize set for unique numbers
unique_numbers: Set[str] = set()

# Load existing numbers from file (if any) to avoid duplicates
try:
    with open(OUTPUT_FILE, "r") as f:
        unique_numbers.update(line.strip() for line in f if line.strip())
    print(f"Loaded {len(unique_numbers)} existing numbers from {OUTPUT_FILE}")
except FileNotFoundError:
    print(f"No existing file found. Starting fresh.")

print("Starting number collection...")

# Run until interrupted (Ctrl+C) or API stops providing numbers
try:
    while True:
        retries = 0
        while retries < MAX_RETRIES:
            try:
                response = session.post(BASE_URL, json=payload, timeout=10)
                print(f"HTTP Status: {response.status_code}")
                print(f"Response Headers: {dict(response.headers)}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if data.get("status") == "SUCCESSFUL" and "freeMsisdnList" in data:
                            new_numbers = data["freeMsisdnList"]
                            prev_count = len(unique_numbers)
                            unique_numbers.update(new_numbers)
                            new_count = len(unique_numbers)
                            print(f"Got {len(new_numbers)} numbers | New unique: {new_count - prev_count} | Total unique: {new_count}")
                            
                            # Save to file immediately
                            with open(OUTPUT_FILE, "w") as f:
                                for num in sorted(unique_numbers):
                                    f.write(num + "\n")
                        else:
                            print(f"Unexpected JSON format: {json.dumps(data, indent=2)}")
                    except ValueError as e:
                        print(f"JSON decode error: {e} | Raw response: {response.text[:200]}")
                        retries += 1
                        time.sleep(RETRY_BACKOFF * retries)
                        continue
                else:
                    print(f"HTTP Error: {response.status_code} | Response: {response.text[:200]}")
                    retries += 1
                    time.sleep(RETRY_BACKOFF * retries)
                    continue
                
                # Reset retries on success
                retries = 0
                break
                
            except Exception as e:
                print(f"Request failed: {e}")
                retries += 1
                time.sleep(RETRY_BACKOFF * retries)
        
        if retries >= MAX_RETRIES:
            print(f"Max retries ({MAX_RETRIES}) reached. Stopping.")
            break
        
        # Wait for the specified delay
        time.sleep(DELAY_SECONDS)

except KeyboardInterrupt:
    print(f"\nStopped by user. Collected {len(unique_numbers)} unique numbers. Saved to {OUTPUT_FILE}")

finally:
    session.close()