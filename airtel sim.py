
import requests
import json
import re # For regular expressions to parse the response

def fetch_airtel_numbers(msisdn=None, brand="AIRTEL", sim_category="PREPAID"):
    """
    Fetches a list of free MSISDNs (phone numbers) from Airtel Bangladesh.
    """
    url = "https://www.bd.airtel.com/en/sim-services"

    # Construct the inner JSON string for the 'body'
    inner_body_json = json.dumps({
        "msisdn": msisdn,
        "brand": brand,
        "simCategory": sim_category
    })

    # Construct the full payload as a Python list.
    # requests.post(json=...) will handle serializing this to JSON string.
    payload = [
        "/free-msisdn/get-msisdn-list",
        {
            "method": "POST",
            "body": inner_body_json # The inner JSON string
        }
    ]

    # Mimic browser headers to ensure the request is accepted
    headers = {
        "Accept": "text/x-component",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json", # This is crucial for the payload
        "Host": "www.bd.airtel.com",
        "Origin": "https://www.bd.airtel.com",
        "Referer": "https://www.bd.airtel.com/en/sim-services",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
        # Important Next.js specific headers, as seen in your request:
        "next-action": "602fff4bf69490335ee829a4bb0e62e2c7c60ea65c",
        "next-router-state-tree": "%5B%22%22%2C%7B%22children%22%3A%5B%5B%22locale%22%2C%22en%22%2C%22d%22%5D%2C%7B%22children%22%3A%5B%22sim-services%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2C%22%2Fen%2Fsim-services%22%2C%22refresh%22%5D%7D%5D%7D%5D%7D%2Cnull%2Cnull%2Ctrue%5D",
        "sec-ch-ua": "\"Chromium\";v=\"140\", \"Not=A?Brand\";v=\"24\", \"Brave\";v=\"140\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
    }
    # You might also need the 'cookie' header from your request if it's session-dependent.
    # cookie_header = "NEXT_LOCALE=en; deviceId=dfb94e7e-63c1-40d2-b547-de38e59ccce5; BIGipServerpool_revamp_bd_airtel=!lhwz4gZ9gbLixmrtWRLzbIBtPd0xFG4g6P2oU3cU6DpDlqdmus7t2D83/30Al5ozvLXtV74YzgdVt1I=; __Host-authjs.csrf-token=e4b0de7e1ecb675e986f59838f8f2fb5551948d6ecd2d5685eef72b863040a33%7Cd46a555fb1c166ca15896a0d12d4cfe5d52abbbbc6ae4e0b905e3ccd61ad5c33; __Secure-authjs.callback-url=https%3A%2F%2Fwww.bd.airtel.com; TS018b3528=01c9bf80bb27fe473aecb942a093fc19779d1d7cce7bf3fde2d297701437957b215c136d0c5746bf438383449800253f837d8915c2ab4ea4800bc09d75ca25fb751cc3f2b7ee3ad14994b6870482bd186adc02ea3b4bf36c662154f6fe42458ec60986274ef4b9d33d2b0e4c8cd2fa2d0c436a2b21"
    # headers["Cookie"] = cookie_header


    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status() # Raise an exception for HTTP errors

        # The response is not straightforward JSON. It's text/x-component.
        # We need to extract the JSON string that contains "freeMsisdnList".
        response_text = response.text
        # print("Raw response:", response_text) # For debugging

        # Use regex to find the JSON object starting with "1:{"
        # We're looking for a pattern like `1:{"status":"SUCCESSFUL", ... "freeMsisdnList":[...]}
        match = re.search(r'1:(\{.*"freeMsisdnList":\[.*?\]\})', response_text)

        if match:
            json_string = match.group(1)
            # print("Extracted JSON string:", json_string) # For debugging
            data = json.loads(json_string) # Parse the extracted JSON string

            if data.get("status") == "SUCCESSFUL" and data.get("freeMsisdnList"):
                return data["freeMsisdnList"], data.get("available", False) # Return numbers and the 'available' flag
            else:
                print(f"API response indicates failure or no free MSISDNs: {data.get('status')}")
                return [], False
        else:
            print("Could not find the 'freeMsisdnList' JSON in the response.")
            return [], False

    except requests.exceptions.RequestException as e:
        print(f"Network or HTTP error occurred: {e}")
        return [], False
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return [], False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return [], False

# --- Main execution ---
if __name__ == "__main__":
    all_airtel_numbers = []
    has_more = True
    # The 'msisdn' parameter in the payload can be used for searching,
    # but there's no clear 'page' or 'limit' in your provided snippet.
    # If the website implements "Load More" or "Next Page" functionality,
    # you'll need to inspect how 'msisdn', or other parameters, change
    # to fetch subsequent sets of numbers.

    # As a first step, let's just make the initial request as observed.
    print("Attempting to fetch Airtel numbers (initial request)...")
    numbers, more_available = fetch_airtel_numbers(brand="AIRTEL", sim_category="PREPAID")

    if numbers:
        all_airtel_numbers.extend(numbers)
        print(f"Found {len(numbers)} numbers on the initial request.")
        # The 'available' flag here is key. If it's always false after one request,
        # it might mean the API gives a fixed set and doesn't support pagination
        # directly through this endpoint.
        print(f"More numbers available? {more_available}")

        # If 'available' is true or if you notice a pattern in the browser's
        # network tab (e.g., a 'page' or 'offset' parameter changes in the
        # *inner_body_json* or other query params), you would implement a loop here.
        # For example, if there was a 'offset' parameter:
        # offset = len(all_airtel_numbers)
        # while more_available:
        #     numbers, more_available = fetch_airtel_numbers(offset=offset, ...)
        #     all_airtel_numbers.extend(numbers)
        #     offset = len(all_airtel_numbers)
        #     print(f"Found {len(numbers)} more. Total: {len(all_airtel_numbers)}. More available? {more_available}")
        #     import time
        #     time.sleep(1) # Be polite!

    else:
        print("No numbers found on the initial request.")

    print(f"\nTotal unique Airtel numbers collected: {len(set(all_airtel_numbers))}") # Using set to get unique numbers

    # Optional: Save to a file
    if all_airtel_numbers:
        file_name = "airtel_phone_numbers.txt"
        with open(file_name, "w") as f:
            for number in sorted(list(set(all_airtel_numbers))): # Sort and save unique numbers
                f.write(number + "\n")
        print(f"Numbers saved to {file_name}")

    # You can also print them
    # print("\n--- All Collected Airtel Phone Numbers ---")
    # for number in sorted(list(set(all_airtel_numbers))):
    #     print(number)