#!/usr/bin/env python3
"""
Task 1
Description: Download ZIP file. Extract, parse CSV file. Write records to redis.
Author: Amey Prasannakumar Chavan
"""

import os
import redis
import requests
import zipfile
import pandas as pd
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


def download_process_data():
	# Prepare date to get last day's data.
	last_date = str(int(date.today().strftime("%d")) - 1)	# Get date of last day.
	month = date.today().strftime("%m")						# Get current month.
	year = date.today().strftime("%y")						# Get current year.

	# Download url for the last day's ZIP file.
	download_url = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ' + last_date + month + year + '_CSV.ZIP'

	# Set the ZIP filename using above download url.
	zipfile_name = download_url[download_url.rfind('/') + 1 :]

	# Set the CSV filename using above download url to extract from ZIP file after download.
	csvfile_name = download_url[download_url.rfind('/') + 1 : download_url.rfind('_')] + '.CSV'

	# Remove old ZIP, CSV files if any, but should not remove the files from last day as in url above.
	directory_name = '.'
	get_listdir = os.listdir(directory_name)
	for item in get_listdir:
		if item.upper().endswith(".ZIP") and item not in zipfile_name:
			os.remove(os.path.join(directory_name, item))
		elif item.upper().endswith(".CSV") and item not in csvfile_name:
			os.remove(os.path.join(directory_name, item))

	
	# Download & extract the ZIP file in url only if is not present.
	zipfile_path = Path(zipfile_name)
	if not zipfile_path.is_file():
		# Create HTTP request.
		requested_file = requests.get(url=download_url)
		with open(zipfile_name, 'wb') as r_file:
			r_file.write(requested_file.content)	# Write the ZIP file to disk.
			del r_file

	# Extract CSV file from downloaded ZIP file.
	with zipfile.ZipFile(zipfile_name, 'r') as zip_obj:
		# zip_obj.extractall()
		zip_obj.extract(member=csvfile_name)		# Extract CSV file from ZIP.
		del zip_obj

	# Read CSV as a pandas dataframe.
	equity_df = pd.read_csv(csvfile_name, sep=',')

	"""
	# Configure hostname & port number of redis client for local environment. Un-comment if need to run locally.
	HOST_NAME = 'localhost'
	PORT_NO = 6379
	DB_NO = 0
	"""

	# Create a client of redis. Un-comment if need to run locally.
	# redis_client_obj = redis.StrictRedis(host=HOST_NAME, port=PORT_NO, db=DB_NO, charset='utf-8')
	
	# Comment two lines below if need to run locally. Un-comment if required to run on heroku.
	redis_client_obj = redis.from_url(url=os.environ['REDISCLOUD_URL'])

	redis_client_obj.flushall()		# Delete all keys in all databases on the current host.
	# redis_client_obj.flushdb()	# Delete all keys in the current database.

	# Iterate over dataframe rows to store data using redis client.
	for index, equity_df_row in equity_df.iterrows(): 
		redis_client_obj.hsetnx(name=str(equity_df_row['SC_NAME']).strip(), key='code', value=equity_df_row['SC_CODE'])
		redis_client_obj.hsetnx(name=str(equity_df_row['SC_NAME']).strip(), key='name', value=equity_df_row['SC_NAME'])
		redis_client_obj.hsetnx(name=str(equity_df_row['SC_NAME']).strip(), key='open', value=equity_df_row['OPEN'])
		redis_client_obj.hsetnx(name=str(equity_df_row['SC_NAME']).strip(), key='high', value=equity_df_row['HIGH'])
		redis_client_obj.hsetnx(name=str(equity_df_row['SC_NAME']).strip(), key='low', value=equity_df_row['LOW'])
		redis_client_obj.hsetnx(name=str(equity_df_row['SC_NAME']).strip(), key='close', value=equity_df_row['CLOSE'])

	print('\n Records stored to redis successfully !', end='\n\n')


if __name__ == '__main__':
	download_process_data()
