from constants import *

MASSIVE_BASE_URL = "https://api.polygon.io"

def get_option_contracts(underlying_ticker, API_KEY=MASSIVE_API_KEY):
	"""
	Fetches all option contract symbols for a given ticker 
	that were active in the last 2 years.
	"""
	contracts = []
	url = f"{MASSIVE_BASE_URL}/v3/reference/options/contracts"
	
	params = {
		"underlying_ticker": underlying_ticker,
		"expired": "true",     # Crucial for historical data
		"limit": 1000,         # Max limit per request
		"apiKey": API_KEY
	}

	while url:
		response = requests.get(url, params=params)
		data = response.json()
		
		if "results" in data:
			for result in data["results"]:
				contracts.append(result["ticker"])
		
		# Handle pagination for tickers with thousands of contracts
		url = data.get("next_url")
		if url:
			# next_url already contains the API key and params
			params = {} 
			
	return contracts