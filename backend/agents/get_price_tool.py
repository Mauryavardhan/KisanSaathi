import requests
import sys
import json

API_URL = "https://api.data.gov.in/resource/35985678-0d79-46b4-9ed6-6f13308a1d24"
API_KEY = "579b464db66ec23bdd000001cdeb4bd9cead42c474ca965998e73503"

def fetch_market_price(state_name="Kerela", commodity=None, district=None):
    print(f"[INFO] Fetching market prices for state: {state_name}")
    params = {
        "api-key": API_KEY,
        "format": "json",
        "offset": "0",
        "limit": "100",
    }
    
    # Add filters if provided
    if state_name:
        params["filters[State]"] = state_name
    if commodity:
        params["filters[Commodity]"] = commodity
        print(f"[INFO] Filtering by commodity: {commodity}")
    if district:
        params["filters[District]"] = district
        print(f"[INFO] Filtering by district: {district}")
    
    try:
        response = requests.get(API_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
    except requests.RequestException as e:
        error_msg = f"Failed to fetch data: {e}"
        print(f"[ERROR] {error_msg}")
        return {"error": error_msg, "data": []}
    
    records = data.get("records", [])
    filtered = []
    
    for record in records:
        # Double check state filter since API might not always respect it
        if record.get("State", "").strip().lower() == state_name.strip().lower():
            filtered.append({
                "state": record.get("State"),
                "district": record.get("District"),
                "market": record.get("Market"),
                "commodity": record.get("Commodity"),
                "variety": record.get("Variety"),
                "min_price": record.get("Min_Price"),
                "max_price": record.get("Max_Price"),
                "modal_price": record.get("Modal_Price"),
                "arrival_date": record.get("Arrival_Date", "")
            })
    
    if filtered:
        print(f"[INFO] Found {len(filtered)} records for state: {state_name}")
        result = {"success": True, "state": state_name, "count": len(filtered), "data": filtered}
    else:
        print(f"[INFO] No records found for state: {state_name}")
        result = {"success": False, "state": state_name, "count": 0, "data": [], "message": "No records found"}

    return result

if __name__ == "__main__":
    if len(sys.argv) == 1:
        state = 'Jharkhand'
        commodity = None
        district = None
    elif len(sys.argv) == 2:
        state = sys.argv[1]
        commodity = None
        district = None
    elif len(sys.argv) == 3:
        state = sys.argv[1]
        commodity = sys.argv[2]
        district = None
    else:
        state = sys.argv[1]
        commodity = sys.argv[2]
        district = sys.argv[3]
    
    result = fetch_market_price(state, commodity, district)
    
    # Print results
    if result.get("success"):
        print(f"\n=== Market Prices for {state} ===")
        print(f"Total records: {result['count']}")
        
        if commodity:
            print(f"Filtered by commodity: {commodity}")
        if district:
            print(f"Filtered by district: {district}")
        
        for i, record in enumerate(result["data"], 1):
            print(f"\nRecord {i}:")
            print(f"  Market: {record['market']}")
            print(f"  Commodity: {record['commodity']}")
            print(f"  Variety: {record['variety']}")
            print(f"  Price Range: ₹{record['min_price']} - ₹{record['max_price']}")
            print(f"  Modal Price: ₹{record['modal_price']}")
            print(f"  Arrival Date: {record['arrival_date']}")
    else:
        print(f"Error: {result.get('message', result.get('error', 'Unknown error'))}")