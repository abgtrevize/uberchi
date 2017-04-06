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
	geo = GoogleV3(timeout=10)
	gpsCoord=geo.geocode(address);
	return gpsCoord;

def getPrice(start_latitude,start_longitude,end_latitude,end_longitude,productIDs):
	accessToken=os.environ['MORPH_ACCESS_TOKEN']
	url='https://api.uber.com/v1.2/requests/estimate'
	headers={'Authorization':"Bearer %s" % accessToken,"Content-Type": "application/json"}
	params={
		'start_latitude':gps_MPP.latitude,
		'start_longitude':gps_MPP.longitude,
		'end_latitude':gps_Harper.latitude,
		'end_longitude':gps_Harper.longitude,
		'seat_count':2,
		'product_id':productIDs['uberX']}
	requestx=requests.post(url,json=params,headers=headers).json()		
	scraperwiki.sqlite.save(
		unique_keys=['timestamp','product_id'],
		data=dict(params,**{'price':requestx['fare']['value'],'timestamp':time.strftime('%Y-%m-%d %H:%M:%S')}))
	params={
		'start_latitude':gps_MPP.latitude,
		'start_longitude':gps_MPP.longitude,
		'end_latitude':gps_Harper.latitude,
		'end_longitude':gps_Harper.longitude,
		'seat_count':1,
		'product_id':productIDs['uberPOOL']}
	requestp1=requests.post(url,json=params,headers=headers).json()		
	scraperwiki.sqlite.save(
		unique_keys=['timestamp','product_id'],
		data=dict(params,**{'price':requestp1['fare']['value'],'timestamp':time.strftime('%Y-%m-%d %H:%M:%S')}))
	params={
		'start_latitude':gps_MPP.latitude,
		'start_longitude':gps_MPP.longitude,
		'end_latitude':gps_Harper.latitude,
		'end_longitude':gps_Harper.longitude,
		'seat_count':2,
		'product_id':productIDs['uberPOOL']}
	requestp2=requests.post(url,json=params,headers=headers).json()		
	scraperwiki.sqlite.save(
		unique_keys=['timestamp','product_id'],
		data=dict(params,**{'price':requestp2['fare']['value'],'timestamp':time.strftime('%Y-%m-%d %H:%M:%S')}))

def __main__():
	#Get GPS Coords;
	gps_MPP=getGPS('151 N Michigan Ave, Chicago, IL 60601');
	gps_Shoreham=getGPS('400 East South Water St, Chicago, IL 60601');
	gps_Harper=getGPS('5807 S Woodlawn Ave, Chicago, IL 60637');
	productIDs=getProducts(accessToken,gps_Shoreham.latitude,gps_Shoreham.longitude)

	while time.localtime().tm_hour<18:
		if time.localtime().tm_hour<9:			
			getPrice(productIDs,gps_MPP.latitude,gps_MPP.longitude,gps_Harper.latitude,gps_Harper.longitude)
			getPrice(productIDs,gps_Shoreham.latitude,gps_Shoreham.longitude,gps_Harper.latitude,gps_Harper.longitude)
			getPrice(productIDs,gps_Harper.latitude,gps_Harper.longitude,gps_MPP.latitude,gps_MPP.longitude)
			getPrice(productIDs,gps_Harper.latitude,gps_Harper.longitude,gps_Shoreham.latitude,gps_Shoreham.longitude)
			time.sleep(60*5)
		elif time.localtime().tm_hour<11:
			time.sleep(60*30)
		elif time.localtime().tm_hour<14:
			getPrice(productIDs,gps_MPP.latitude,gps_MPP.longitude,gps_Harper.latitude,gps_Harper.longitude)
			getPrice(productIDs,gps_Shoreham.latitude,gps_Shoreham.longitude,gps_Harper.latitude,gps_Harper.longitude)
			getPrice(productIDs,gps_Harper.latitude,gps_Harper.longitude,gps_MPP.latitude,gps_MPP.longitude)
			getPrice(productIDs,gps_Harper.latitude,gps_Harper.longitude,gps_Shoreham.latitude,gps_Shoreham.longitude)
			time.sleep(60*5)
		elif time.localtime().tm_hour<16:
			time.sleep(60.30)
		else:
			getPrice(productIDs,gps_MPP.latitude,gps_MPP.longitude,gps_Harper.latitude,gps_Harper.longitude)
			getPrice(productIDs,gps_Shoreham.latitude,gps_Shoreham.longitude,gps_Harper.latitude,gps_Harper.longitude)
			getPrice(productIDs,gps_Harper.latitude,gps_Harper.longitude,gps_MPP.latitude,gps_MPP.longitude)
			getPrice(productIDs,gps_Harper.latitude,gps_Harper.longitude,gps_Shoreham.latitude,gps_Shoreham.longitude)
			time.sleep(60*10);

os.environ['TZ']='US/Central'
time.tzset()
if __name__ == '__main__':
		main()	