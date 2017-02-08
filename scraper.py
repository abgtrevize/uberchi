import requests
import sqlite3
import re
from time import sleep
from random import randint
import json
from geopy.geocoders import GoogleV3
from uber_rides.session import Session,OAuth2Credential
from uber_rides.client import UberRidesClient
import os
import ssl
from urllib3.contrib import pyopenssl


##Replace with known Lat, Long;
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context
#context = ssl._create_unverified_context()

#Get Session
def getAuth():
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
	return client

#Get Product IDs;
def getProducts(client,lattitude,longitude):
	products=client.get_products(lattitude,longitude).json['products']
	productIDs={'uberX':(i for i in products if i['display_name']=='uberX').next()['product_id'],
		'uberPOOL':(i for i in products if i['display_name']=='uberPOOL').next()['product_id']}
	return productIDs

#Get GPS Coordinates;
def getGPS(address):
	geo = GoogleV3(timeout=5)
	gpsCoord=geo.geocode(address);
	return gpsCoord;

def sendToDB():
	#Get Client;
	client=getAuth();

	#Get GPS Coords;
	gps_MPP=getGPS('151 N Michigan Ave, Chicago, IL 60601');
	gps_Shoreham=getGPS('400 East South Water St, Chicago, IL 60601');
	gps_Harper=getGPS('5807 S Woodlawn Ave, Chicago, IL 60637');
	productIDs=getProducts(client,gps_Shoreham.latitude,gps_Shoreham.longitude)

	#Price Estimates
	x_MPP_Harper=client.estimate_ride(
		start_latitude=gps_MPP.latitude,
		start_longitude=gps_MPP.longitude,
		end_latitude=gps_Harper.latitude,
		end_longitude=gps_Harper.longitude,
		seat_count=2,
		product_id=productIDs['uberX']
		)
	p1_MPP_Harper=client.estimate_ride(
		start_latitude=gps_MPP.latitude,
		start_longitude=gps_MPP.longitude,
		end_latitude=gps_Harper.latitude,
		end_longitude=gps_Harper.longitude,
		seat_count=1,
		product_id=productIDs['uberPOOL']
		)
	p2_MPP_Harper=client.estimate_ride(
		start_latitude=gps_MPP.latitude,
		start_longitude=gps_MPP.longitude,
		end_latitude=gps_Harper.latitude,
		end_longitude=gps_Harper.longitude,
		seat_count=2,
		product_id=productIDs['uberPOOL']
		)

	x_Shoreham_Harper=client.estimate_ride(
		start_latitude=gps_Shoreham.latitude,
		start_longitude=gps_Shoreham.longitude,
		end_latitude=gps_Harper.latitude,
		end_longitude=gps_Harper.longitude,
		seat_count=2,
		product_id=productIDs['uberX']
		)
	p1_Shoreham_Harper=client.estimate_ride(
		start_latitude=gps_Shoreham.latitude,
		start_longitude=gps_Shoreham.longitude,
		end_latitude=gps_Harper.latitude,
		end_longitude=gps_Harper.longitude,
		seat_count=1,
		product_id=productIDs['uberPOOL']
		)
	p2_Shoreham_Harper=client.estimate_ride(
		start_latitude=gps_Shoreham.latitude,
		start_longitude=gps_Shoreham.longitude,
		end_latitude=gps_Harper.latitude,
		end_longitude=gps_Harper.longitude,
		seat_count=2,
		product_id=productIDs['uberPOOL']
		)

	x_Harper_MPP=client.estimate_ride(
		start_latitude=gps_Harper.latitude,
		start_longitude=gps_Harper.longitude,
		end_latitude=gps_MPP.latitude,
		end_longitude=gps_MPP.longitude,
		seat_count=2,
		product_id=productIDs['uberX']
		)
	p1_Harper_MPP=client.estimate_ride(
		start_latitude=gps_Harper.latitude,
		start_longitude=gps_Harper.longitude,
		end_latitude=gps_MPP.latitude,
		end_longitude=gps_MPP.longitude,
		seat_count=1,
		product_id=productIDs['uberPOOL']
		)
	p2_Harper_MPP=client.estimate_ride(
		start_latitude=gps_Harper.latitude,
		start_longitude=gps_Harper.longitude,
		end_latitude=gps_MPP.latitude,
		end_longitude=gps_MPP.longitude,
		seat_count=2,
		product_id=productIDs['uberPOOL']
		)

	x_Harper_Shoreham=client.estimate_ride(
		start_latitude=gps_Harper.latitude,
		start_longitude=gps_Harper.longitude,
		end_latitude=gps_Shoreham.latitude,
		end_longitude=gps_Shoreham.longitude,
		seat_count=2,
		product_id=productIDs['uberX']
		)
	p1_Harper_Shoreham=client.estimate_ride(
		start_latitude=gps_Harper.latitude,
		start_longitude=gps_Harper.longitude,
		end_latitude=gps_Shoreham.latitude,
		end_longitude=gps_Shoreham.longitude,
		seat_count=1,
		product_id=productIDs['uberPOOL']
		)
	p2_Harper_Shoreham=client.estimate_ride(
		start_latitude=gps_Harper.latitude,
		start_longitude=gps_Harper.longitude,
		end_latitude=gps_Shoreham.latitude,
		end_longitude=gps_Shoreham.longitude,
		seat_count=2,
		product_id=productIDs['uberPOOL']
		)
	print p2_Harper_Shoreham.json

sendToDB()
	