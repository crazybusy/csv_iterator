from iterator_action import iterator_action
import requests


class distances_iterator_action():

	API_KEY = 'AIzaSyD0H_G1JKCgklUtvDFVcdoMtto3ooyalZ8'

	def get_action_verb(self):
		return "Finding distances"

	def test_iterator_action(self):
		origins="34.0209141,-118.2855371"
		destination = "34.021955,-118.283894"
		return self.get_google_results(origins, destination, self.API_KEY)

	def run_iterator_action(self, input):
		return self.get_google_results(input['from_address'], input['formatted_address'], self.API_KEY)

	def get_google_results(self, origins, destination, api_key):
		geocode_url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={}&destinations={}"\
			.format(origins, destination)
		if api_key is not None:
			geocode_url = geocode_url + "&key={}".format(api_key)
		# Ping google for the reuslts:
		print (geocode_url)
		results = requests.get(geocode_url)

		# Results will be in JSON format - convert to dict using requests functionality
		results = results.json()

		output = {}
		output['status'] = results['status']

		output['origins'] = origins
		output['destination'] = destination
		if results['status'] == 'OK':
			output['distances'] = results['rows'][0]['elements'][0]['distance']['value']
			output['duration'] = results['rows'][0]['elements'][0]['duration']['value']

		return output


def main():
	print(routes_iterator_action().test_iterator_action())

if __name__ == '__main__':
	main()
