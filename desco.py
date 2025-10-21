import requests
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# === DESCO account details ===
ACCOUNT_NO = "14039719"
METER_NO = "661120136562"

# === API endpoints ===
INFO_URL = "https://prepaid.desco.org.bd/api/tkdes/customer/getCustomerInfo"
BALANCE_URL = "https://prepaid.desco.org.bd/api/tkdes/customer/getBalance"

# === Common parameters ===
params = {
    "accountNo": ACCOUNT_NO,
    "meterNo": METER_NO
}

try:
    # --- Fetch customer information ---
    info_response = requests.get(INFO_URL, params=params, verify=False, timeout=10)
    info_response.raise_for_status()
    info_data = info_response.json()["data"]

    # --- Fetch balance information ---
    balance_response = requests.get(BALANCE_URL, params=params, verify=False, timeout=10)
    balance_response.raise_for_status()
    balance_data = balance_response.json()["data"]

    # --- Display results ---
    print("⚡ DESCO Prepaid Customer Information")
    print("====================================")
    print(f"👤 Name: {info_data['customerName']}")
    print(f"🏠 Address: {info_data['installationAddress']}")
    print(f"📞 Contact No: {info_data['contactNo']}")
    print(f"🌐 Feeder: {info_data['feederName']}")
    print(f"📅 Installed: {info_data['installationDate']}")
    print(f"🔌 Phase Type: {info_data['phaseType']}")
    print(f"⚙️  Tariff: {info_data['tariffSolution']}")
    print(f"🏢 Sub-Division: {info_data['SDName']}")
    print("------------------------------------")
    print("💰 Balance Information")
    print(f"💡 Current Balance: ৳{balance_data['balance']}")
    print(f"🔋 This Month Consumption: {balance_data['currentMonthConsumption']} kWh")
    print(f"🕒 Last Reading Time: {balance_data['readingTime']}")

except requests.exceptions.SSLError:
    print("❌ SSL certificate verification failed — even with verify=False (very rare).")
except requests.exceptions.ConnectionError:
    print("❌ Connection failed. Check your internet or DESCO site availability.")
except requests.exceptions.Timeout:
    print("⏳ Request timed out. Try again later.")
except Exception as e:
    print("⚠️ Unexpected error:", e)
