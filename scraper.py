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

def getPrices():
	#Get Client;
	accessToken=os.environ['MORPH_ACCESS_TOKEN']

	#Get GPS Coords;
	gps_MPP=getGPS('151 N Michigan Ave, Chicago, IL 60601');
	gps_Shoreham=getGPS('400 East South Water St, Chicago, IL 60601');
	gps_Harper=getGPS('5807 S Woodlawn Ave, Chicago, IL 60637');
	productIDs=getProducts(accessToken,gps_Shoreham.latitude,gps_Shoreham.longitude)

	url='https://api.uber.com/v1.2/requests/estimate'
	headers={'Authorization':"Bearer %s" % accessToken,"Content-Type": "application/json"}

	#MPP to Harper
	params={
		'start_latitude':gps_MPP.latitude,
		'start_longitude':gps_MPP.longitude,
		'end_latitude':gps_Harper.latitude,
		'end_longitude':gps_Harper.longitude,
		'seat_count':2,
		'product_id':productIDs['uberX']}
	x_MPP_Harper=requests.post(url,json=params,headers=headers).json()
    scraperwiki.sqlite.save(unique_keys=['timestamp','product'], data={'timestamp':time.strftime('%Y-%m-%d %H:%M:%S'),'product':'uberX','price':x_MPP_Harper['fare']['value']})

	params={
		'start_latitude':gps_MPP.latitude,
		'start_longitude':gps_MPP.longitude,
		'end_latitude':gps_Harper.latitude,
		'end_longitude':gps_Harper.longitude,
		'seat_count':1,
		'product_id':productIDs['uberPOOL']}
	p1_MPP_Harper=requests.post(url,json=params,headers=headers).json()
	params={
		'start_latitude':gps_MPP.latitude,
		'start_longitude':gps_MPP.longitude,
		'end_latitude':gps_Harper.latitude,
		'end_longitude':gps_Harper.longitude,
		'seat_count':2,
		'product_id':productIDs['uberPOOL']}
	p2_MPP_Harper=requests.post(url,json=params,headers=headers).json()

	#Shoreham to Harper
	params={
		'start_latitude':gps_Shoreham.latitude,
		'start_longitude':gps_Shoreham.longitude,
		'end_latitude':gps_Harper.latitude,
		'end_longitude':gps_Harper.longitude,
		'seat_count':2,
		'product_id':productIDs['uberX']}
	x_Shoreham_Harper=requests.post(url,json=params,headers=headers).json()
	params={
		'start_latitude':gps_Shoreham.latitude,
		'start_longitude':gps_Shoreham.longitude,
		'end_latitude':gps_Harper.latitude,
		'end_longitude':gps_Harper.longitude,
		'seat_count':1,
		'product_id':productIDs['uberPOOL']}
	p1_Shoreham_Harper=requests.post(url,json=params,headers=headers).json()
	params={
		'start_latitude':gps_Shoreham.latitude,
		'start_longitude':gps_Shoreham.longitude,
		'end_latitude':gps_Harper.latitude,
		'end_longitude':gps_Harper.longitude,
		'seat_count':2,
		'product_id':productIDs['uberPOOL']}
	p2_Shoreham_Harper=requests.post(url,json=params,headers=headers).json()

	#Harper to MPP
	params={
		'end_latitude':gps_MPP.latitude,
		'end_longitude':gps_MPP.longitude,
		'start_latitude':gps_Harper.latitude,
		'start_longitude':gps_Harper.longitude,
		'seat_count':2,
		'product_id':productIDs['uberX']}
	x_MPP_Harper=requests.post(url,json=params,headers=headers).json()
	params={
		'end_latitude':gps_MPP.latitude,
		'end_longitude':gps_MPP.longitude,
		'start_latitude':gps_Harper.latitude,
		'start_longitude':gps_Harper.longitude,
		'seat_count':1,
		'product_id':productIDs['uberPOOL']}
	p1_MPP_Harper=requests.post(url,json=params,headers=headers).json()
	params={
		'end_latitude':gps_MPP.latitude,
		'end_longitude':gps_MPP.longitude,
		'start_latitude':gps_Harper.latitude,
		'start_longitude':gps_Harper.longitude,
		'seat_count':2,
		'product_id':productIDs['uberPOOL']}
	p2_MPP_Harper=requests.post(url,json=params,headers=headers).json()

#Harper to Shoreham
	params={
		'end_latitude':gps_Shoreham.latitude,
		'end_longitude':gps_Shoreham.longitude,
		'start_latitude':gps_Harper.latitude,
		'start_longitude':gps_Harper.longitude,
		'seat_count':2,
		'product_id':productIDs['uberX']}
	x_Shoreham_Harper=requests.post(url,json=params,headers=headers).json()
	params={
		'end_latitude':gps_Shoreham.latitude,
		'end_longitude':gps_Shoreham.longitude,
		'start_latitude':gps_Harper.latitude,
		'start_longitude':gps_Harper.longitude,
		'seat_count':1,
		'product_id':productIDs['uberPOOL']}
	p1_Shoreham_Harper=requests.post(url,json=params,headers=headers).json()
	params={
		'end_latitude':gps_Shoreham.latitude,
		'end_longitude':gps_Shoreham.longitude,
		'start_latitude':gps_Harper.latitude,
		'start_longitude':gps_Harper.longitude,
		'seat_count':2,
		'product_id':productIDs['uberPOOL']}
	p2_Shoreham_Harper=requests.post(url,json=params,headers=headers).json()

    scraperwiki.sqlite.save(unique_keys=['ID'], data=data)

getPrices()
	