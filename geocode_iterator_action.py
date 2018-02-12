import requests
from iterator_action import iterator_action

class geocode_iterator_action(iterator_action):

	API_KEY = 'AIzaSyD0H_G1JKCgklUtvDFVcdoMtto3ooyalZ8'
	address_column_name = "Address"

	def get_action_verb(self):
		return "Geocoding"

	def test_iterator_action(self):
		return self.get_google_results({"Address":"London, England"}, self.API_KEY)

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

	    address = input[self.address_column_name]

	    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}".format(address)
	    if api_key is not None:
	        geocode_url = geocode_url + "&key={}".format(api_key)
	        
	    # Ping google for the reuslts:
	    results = requests.get(geocode_url)
	    # Results will be in JSON format - convert to dict using requests functionality
	    results = results.json()
	    
	    # if there's no results or an error, return empty results.
	    if len(results['results']) == 0:
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
	        answer = results['results'][0]
	        output = {
	            "formatted_address" : answer.get('formatted_address'),
	            "latitude": answer.get('geometry').get('location').get('lat'),
	            "longitude": answer.get('geometry').get('location').get('lng'),
	            "accuracy": answer.get('geometry').get('location_type'),
	            "google_place_id": answer.get("place_id"),
	            "type": ",".join(answer.get('types')),
	            "postcode": ",".join([x['long_name'] for x in answer.get('address_components') 
	                                  if 'postal_code' in x.get('types')])
	        }
	        
	    # Append some other details:    
	    output['input_string'] = address
	    output['number_of_results'] = len(results['results'])
	    output['status'] = results.get('status')
	    if return_full_response is True:
	        output['response'] = results
	    
	    return output

def main():
	print(geocode_iterator_action().test_iterator_action())

if __name__ == '__main__':
	main()
