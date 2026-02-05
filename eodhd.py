from constants import *


def get_index_composition(index_symbol="NDX.INDX", api_token=EODHD_API_KEY):
	"""
	Fetches the current components of an index using EODHD Fundamental API.
	Common symbols: NDX.INDX (Nasdaq 100), GSPC.INDX (S&P 500).
	"""
	url = f"https://eodhd.com/api/fundamentals/{index_symbol}"
	params = {
		"api_token": api_token,
		"fmt": "json"
	}
	
	response = requests.get(url, params=params)
	
	if response.status_code != 200:
		raise Exception(f"API Request failed: {response.status_code} - {response.text}")
	
	data = response.json()
	
	# EODHD puts components inside the 'Components' key for Index symbols
	components = data.get('Components', {})
	
	if not components:
		print(f"No components found for {index_symbol}. Ensure you are using the .INDX suffix.")
		return pd.DataFrame()

	# Convert dictionary of components to a clean DataFrame
	df = pd.DataFrame.from_dict(components, orient='index')
	
	# Clean up column names (Code, Name, Sector, Industry, Weight)
	return df.reset_index(drop=True)

# Example Usage:
# api_key = "your_eodhd_key"
# ndx_df = get_index_composition("NDX.INDX", api_key)
# print(ndx_df.head())

def get_ndx_historical_changes(index_symbol="NDX.INDX", api_token=EODHD_API_KEY):
	# NDX.INDX is the EODHD symbol for Nasdaq 100
	url = f"https://eodhd.com/api/fundamentals/{index_symbol}"
	params = {
		"api_token": api_token,
		"fmt": "json"
	}
	
	response = requests.get(url, params=params)
	data = response.json()
	
	# EODHD stores historical additions/removals in 'HistoricalTickerComponents'
	historical_data = data.get('HistoricalTickerComponents', {})
	
	if not historical_data:
		return "No historical data found for this index."

	# Convert to DataFrame
	df = pd.DataFrame.from_dict(historical_data, orient='index')
	df['Date'] = pd.to_datetime(df['Date'])
	
	# Filter for the last 2 years
	two_years_ago = pd.Timestamp.now() - pd.DateOffset(years=2)
	return df[df['Date'] >= two_years_ago].sort_values(by='Date', ascending=False)

# usage: changes_df = get_ndx_historical_changes("your_api_token")