import requests
from uber_rides.session import Session,OAuth2Credential
from uber_rides.client import UberRidesClient
import os

#Variables
gps_Shoreham=[41.8867588, -87.6168219]
gps_Harper=[41.7889213, -87.5955699]
productIDs='4bfc6c57-98c0-424f-a72e-c1e2a1d49939'

#Uber with SDK
credentials = {
	'access_token': os.environ['MORPH_ACCESS_TOKEN'],
	'client_id': os.environ['MORPH_CLIENT_ID'],
	'client_secret': os.environ['MORPH_CLIENT_SECRET'],
	'expires_in_seconds': 2592000,  
	'grant_type': 'authorization_code',
	'scopes': None
}
oauth2_credential = OAuth2Credential(**credentials)
session = Session(oauth2credential=oauth2_credential)
client = UberRidesClient(session)

x_Shoreham_Harper=client.estimate_ride(
	start_latitude=gps_Shoreham[0],
	start_longitude=gps_Shoreham[1],
	end_latitude=gps_Harper[0],
	end_longitude=gps_Harper[1],
	seat_count=2,
	product_id=productIDs
	)

print x.json