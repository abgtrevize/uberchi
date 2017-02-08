#import scraperwiki
import time
import requests

expected_string = "Hassle-free web scraping."

# Check that proxy gives a working certificate for SSL connections
# If the certificate isn't valid it should throw an exception
#html = scraperwiki.scrape("https://morph.io")

#if not expected_string in html:
 #   raise Exception("Not expected result")

# Use requests library to do the same because it gets its CA certs a different way. Oh joy.
r = requests.get('https://morph.io')
if not expected_string in r.text:
    raise Exception("Not expected result")
