import requests
import json

class GeoCode:
	def __init__(self,address,city,zip):
		self.address = address
		self.city = city
		self.zip = zip
		self.url_shortener = "https://www.googleapis.com/urlshortener/v1/url?key="
		self.api_key = "AIzaSyBCm1e-xWsP_OpovJ_IOdWcfU4EI41K57I"
		self.base_url = 'https://maps.googleapis.com/maps/api/geocode/'

	def base_geocode(self):
		address = str(self.address).replace("  ","+").replace(" ","+")
		city = str(self.city).replace(' ','+')
		zip = str(self.zip)
		full_address = address + ',' + city + ',' + zip
		final_address_to_encode = self.base_url + "json?address=" + full_address + "&key=" + self.api_key
		r = requests.get(final_address_to_encode)
		return r.json()['results']

	def lat_lng(self):
		return self.base_geocode()[0]['geometry']['location']

	def get_google_map_short_url(self):
		lat_lng = self.lat_lng()
		lat = lat_lng['lat']
		lng = lat_lng['lng']

		url = "http://maps.google.com/maps?z=12&t=m&q=loc:" + str(lat) + "+" + str(lng)
		data = {"longUrl" : url}
		headers = {"Content-Type" : 'application/json'}
		full_url = self.url_shortener + self.api_key
		return requests.post(full_url,headers=headers,data=json.dumps(data)).json()['id']
	
		