import requests
import math

# Base URL for the API endpoint
base_url = "https://eshop-api.banglalink.net/api/v1/product/variant"

# Initial parameters for the first request
params = {
    "series": "019",
    "page": 1,         # Start from the first page
    "limit": 50,       # You can increase the limit to fetch more items per request, up to what the API allows.
    "search": "",
    "product_id": 40
}

all_phone_numbers = []
total_items = 0
last_page = 1 # Initialize, will be updated from the first response

print("Starting to fetch phone numbers...")

while params["page"] <= last_page:
    try:
        print(f"Fetching page {params['page']}...")
        response = requests.get(base_url, params=params)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)

        data = response.json()

        if data["status"] == "SUCCESS" and data["code"] == 200:
            response_data = data["data"]

            # Update total_items and last_page from the first response
            if params["page"] == 1:
                total_items = response_data["total_items"]
                last_page = response_data["last_page"]
                print(f"Total items found: {total_items}")
                print(f"Total pages to fetch: {last_page}")

            # Extract numbers from the current page's items
            for item in response_data["items"]:
                number = item.get("variant_value") # or item.get("variant_name")
                if number:
                    all_phone_numbers.append(number)

            params["page"] += 1 # Move to the next page
        else:
            print(f"API returned an error on page {params['page']}: {data.get('message', 'Unknown error')}")
            break # Stop if there's an API-level error

    except requests.exceptions.RequestException as e:
        print(f"Network or HTTP error occurred: {e}")
        print(f"Attempting to retry page {params['page']} after a short delay...")
        import time
        time.sleep(5)
        continue # Try this page again
    except ValueError as e:
        print(f"Error decoding JSON response on page {params['page']}: {e}")
        break # Stop if response is not valid JSON
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        break # Stop for other unexpected errors

print(f"\nFinished fetching. Collected {len(all_phone_numbers)} unique phone numbers.")

# Optional: Save the numbers to a file
file_name = "banglalink_phone_numbers.txt"
with open(file_name, "w") as f:
    for number in all_phone_numbers:
        f.write(number + "\n")

print(f"Numbers saved to {file_name}")