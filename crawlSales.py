"""
crawlSales.py
Crawling sales data
"""
import hashlib
import json
import requests
import pandas as pd
from datetime import datetime
import auth

API_URL: str = 'https://area9-win.pospal.cn:443/pospal-api2/openapi/v1/userOpenApi/queryAllUser'
ENCODING: str = 'utf-8'
MILLISECONDS_PER_SECOND: int = 1000


def generateSecret(plaintext: str) -> str:
	return hashlib.md5(plaintext.encode(ENCODING)).hexdigest()

def generateDataSignature(appKey: str, json_body: str) -> str:
	joined_str: str = ('%s%s' % (auth.APP_KEY, json_body))
	secret: str = generateSecret(joined_str)
	return secret.upper()

def getStore() -> dict:
	# Get current timestamp
	currentTime = datetime.now()
	timestamp: int = int(datetime.timestamp(currentTime) * MILLISECONDS_PER_SECOND)

	# The body
	body: dict = {
		"appId": auth.APP_ID,
	}
	json_body: str = json.dumps(body)

	# The header
	headers: dict = {
		"User-Agent": "openAPI",
		"Content-Type": ("application/json; charset=%s" % (ENCODING)),
		"accept-encoding": "gzip,deflate",
		"time-stamp": str(timestamp),
		"data-signature": generateDataSignature(auth.APP_KEY, json_body)
	}

	response = requests.post(
		API_URL, 
		headers=headers,
		json=body
	)
	return response.json()

def main():
	stores = getStore()
	print (pd.DataFrame(stores['data']['result']))

main()	
