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
import scraperwiki
import time

#Get Product IDs;
def getProducts(accessToken,latitude,longitude):
	url='https://api.uber.com/v1.2/products?latitude=%(1)s&longitude=%(2)s' % {'1':latitude,'2':longitude}
	products=requests.get(url,headers={'Authorization':"Bearer %s" % accessToken}).json()['products']
	productIDs={'uberX':(i for i in products if i['display_name']=='uberX').next()['product_id'],
		'uberPOOL':(i for i in products if i['display_name']=='uberPOOL').next()['product_id']}
	return productIDs

#Get GPS Coordinates;
def getGPS(address):
	geo = GoogleV3(timeout=5)
	gpsCoord=geo.geocode(address);
	return gpsCoord;

def getPrice(products,start_latitude,start_longitude,end_latitude,end_longitude):
	accessToken=os.environ['MORPH_ACCESS_TOKEN']
	url='https://api.uber.com/v1.2/requests/estimate'
	headers={'Authorization':"Bearer %s" % accessToken,"Content-Type": "application/json"}
	params={
		'start_latitude':start_latitude,
		'start_longitude':start_longitude,
		'end_latitude':end_latitude,
		'end_longitude':end_longitude,
		'seat_count':2,
		'product_id':products['uberX']}
	requestx=requests.post(url,json=params,headers=headers)
	print requestx.reason	
	scraperwiki.sqlite.save(
		unique_keys=['timestamp','product_id'],
		data=dict(params,**{'price':requestx.json()['fare']['value'],'timestamp':time.strftime('%Y-%m-%d %H:%M:%S')}))
	params={
		'start_latitude':start_latitude,
		'start_longitude':start_longitude,
		'end_latitude':end_latitude,
		'end_longitude':end_longitude,
		'seat_count':1,
		'product_id':products['uberPOOL']}
	requestp1=requests.post(url,json=params,headers=headers)
	print requestp1.reason	
	scraperwiki.sqlite.save(
		unique_keys=['timestamp','product_id'],
		data=dict(params,**{'price':requestp1.json()['fare']['value'],'timestamp':time.strftime('%Y-%m-%d %H:%M:%S')}))
	params={
		'start_latitude':start_latitude,
		'start_longitude':start_longitude,
		'end_latitude':end_latitude,
		'end_longitude':end_longitude,
		'seat_count':2,
		'product_id':products['uberPOOL']}
	requestp2=requests.post(url,json=params,headers=headers).json()	
	print requestp2	
	scraperwiki.sqlite.save(
		unique_keys=['timestamp','product_id'],
		data=dict(params,**{'price':requestp2.json()['fare']['value'],'timestamp':time.strftime('%Y-%m-%d %H:%M:%S')}))

def main():
	#Get GPS Coords;
	accessToken=os.environ['MORPH_ACCESS_TOKEN']
	gps_MPP=getGPS('151 N Michigan Ave, Chicago, IL 60601');
	gps_Shoreham=getGPS('400 East South Water St, Chicago, IL 60601');
	gps_Harper=getGPS('5807 S Woodlawn Ave, Chicago, IL 60637');
	productIDs=getProducts(accessToken,gps_Shoreham.latitude,gps_Shoreham.longitude)

	while time.localtime().tm_hour<19 and time.localtime().tm_min<=30:
		getPrice(productIDs,gps_MPP.latitude,gps_MPP.longitude,gps_Harper.latitude,gps_Harper.longitude)
		getPrice(productIDs,gps_Shoreham.latitude,gps_Shoreham.longitude,gps_Harper.latitude,gps_Harper.longitude)
		getPrice(productIDs,gps_Harper.latitude,gps_Harper.longitude,gps_MPP.latitude,gps_MPP.longitude)
		getPrice(productIDs,gps_Harper.latitude,gps_Harper.longitude,gps_Shoreham.latitude,gps_Shoreham.longitude)
		time.sleep(60*5)

os.environ['TZ']='US/Central'
time.tzset()
if __name__ == '__main__':
		main()	