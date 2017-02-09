import requests
from uber_rides.session import Session,OAuth2Credential
from uber_rides.client import UberRidesClient
import os

#Variables
gps_Shoreham=[41.8867588, -87.6168219]
gps_Harper=[41.7889213, -87.5955699]
productIDs='4bfc6c57-98c0-424f-a72e-c1e2a1d49939'

#Uber with SDK
accessToken=os.environ['MORPH_ACCESS_TOKEN']

url='https://api.uber.com/v1.2/products?latitude=%(1)s&longitude=%(2)s' % {'1':gps_Shoreham[0],'2':gps_Shoreham[1]}
r=requests.get(url,headers={'Authorization':"Bearer %s" % accessToken})
print r.json()