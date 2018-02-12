import requests
from iterator_action import iterator_action

class geocode_lsd_iterator_action(iterator_action):

	API_KEY = '465351144075618807441x4574'
	address_column_name = "Address"

	def get_action_verb(self):
		return "Geocoding"

	def test_iterator_action(self):
		return self.get_google_results({"Address":"04-16-031-15W"}, self.API_KEY)

	def run_iterator_action(self, input):
		return self.get_google_results(input)


	def get_google_results(self, input, api_key=None, return_full_response=False):
	    """
	    Get geocode results from Google Maps Geocoding API.
	    
	    Note, that in the case of multiple google geocode reuslts, this function returns details of the FIRST result.
	    
	    @param address: String address as accurate as possible. For Example "18 Grafton Street, Dublin, Ireland"
	    @param api_key: String API key if present from google. 
	                    If supplied, requests will use your allowance from the Google API. If not, you
	                    will be limited to the free usage of 2500 requests per day.
	    @param return_full_response: Boolean to indicate if you'd like to return the full response from google. This
	                    is useful if you'd like additional location details for storage or parsing later.
	    """
	    # Set up your Geocoding url
	    #geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}".format(address)
	    #if api_key is not None:
	    #    geocode_url = geocode_url + "&key={}".format(api_key)

	    address = input[self.address_column_name]

	    geocode_url = "https://geocoder.ca/?locate={}".format(address)
	    geocode_url = geocode_url + "&json=1"   

	        
	    # Ping google for the reuslts:
	    results = requests.get(geocode_url)
	    # Results will be in JSON format - convert to dict using requests functionality
	    results = results.json()
	    
	    # if there's no results or an error, return empty results.
	    #if len(results['results']) == 0:
	    if len(results) == 0:
	        output = {
	            "formatted_address" : None,
	            "latitude": None,
	            "longitude": None,
	            "accuracy": None,
	            "google_place_id": None,
	            "type": None,
	            "postcode": None
	        }
	    else:    
	        #answer = results['results'][0]
	        answer = results
	        output = {
	            "formatted_address" : answer.get('LSD'),
	            "latitude": answer.get('latt'),
	            "longitude": answer.get('longt'),
	            "accuracy": answer.get('confidence'),
	            "city": answer.get("city"),
	            "prov": answer.get('prov'),
	            "postcode": answer.get('postal'),
	            "TimeZone": answer.get('TimeZone'),
	            "stnumber": answer.get('stnumber'),
	            "staddress": answer.get('staddress'),
	            "AreaCode": answer.get('AreaCode'),
	            "error": answer.get('error')
	        }
	        
	    # Append some other details:    
	    output['input_string'] = address
	    #output['number_of_results'] = len(results)
	    output['status'] = answer.get('confidence')
	    if return_full_response is True:
	        output['response'] = results
	    
	    return output

def main():
	print(geocode_lsd_iterator_action().test_iterator_action())

if __name__ == '__main__':
	main()