#!/usr/bin/env python3
"""
Task 2
Description: CherryPy python web application.
Author: Amey Prasannakumar Chavan
"""

from flask import Flask, render_template, redirect, url_for, request
import redis
from urllib.parse import urlparse
import os


webapp = Flask(__name__)

"""
# Configure hostname & port number of redis client for local environment. Un-comment if need to run locally.
HOST_NAME = 'localhost'
PORT_NO = 6379
DB_NO = 0
"""

@webapp.route("/")
def index():
	# Create a client of redis.
	# redis_client_obj = redis.StrictRedis(host=HOST_NAME, port=PORT_NO, db=DB_NO, charset='utf-8')	# Un-comment if need to run locally.
	
	# Comment three lines below (upto 'redis_client_obj') if need to run locally. Un-comment if required to run on heroku.
	# url = urlparse(os.environ.get('REDISCLOUD_URL'))
	# redis_client_obj = redis.StrictRedis(host=url.hostname, port=url.port, password=url.password)
	redis_client_obj = redis.from_url(url=os.environ['REDISCLOUD_URL'])

	redis_keys = redis_client_obj.keys(pattern=u'*')	# Get all existing keys in redis.
	redis_keys = [decoded_str.decode(encoding='utf-8') for decoded_str in redis_keys]	# Decoded bytes to string.

	redis_list_dict = []
	for name in redis_keys:
		redis_list_dict.append(redis_client_obj.hgetall(name=name))
	
	# Decode byte key-value pairs to string within each dictionary of 'redis_list_dict'.
	i = 0
	for dict_items in redis_list_dict:
		temp_dict = {}
		temp_dict.clear()
		for key, value in dict_items.items():
			temp_dict[key.decode('utf-8')] = value.decode('utf-8')
		redis_list_dict[i] = temp_dict
		i = i + 1

	return render_template('index.html', redis_list_dict=redis_list_dict)


@webapp.route("/", methods=['POST', 'GET'])
def search_button_clicked():
	if request.method == 'POST':
		search_name = request.form['search_name_input_text']
		return redirect(url_for('search_result', search_name=search_name))
	elif request.method == 'GET':
		search_name = request.args.get('search_name_input_text')
		return redirect(url_for('search_result', search_name=search_name))


@webapp.route("/<string:search_name>")
def search_result(search_name=''):
	# Create a client of redis. Un-comment if need to run locally.
	# redis_client_obj = redis.StrictRedis(host=HOST_NAME, port=PORT_NO, db=DB_NO, charset='utf-8')
	redis_client_obj = redis.from_url(url=os.environ['REDISCLOUD_URL'])
	
	redis_keys = redis_client_obj.keys(pattern=u'*')	# Get all existing keys in redis
	redis_keys = [decoded_str.decode(encoding='utf-8') for decoded_str in redis_keys]	# Decoded bytes to string.

	redis_keys_found = [key for key in redis_keys if search_name.upper().strip() in key]

	redis_list_dict = []
	for name in redis_keys_found:
		redis_list_dict.append(redis_client_obj.hgetall(name=name))

	if redis_list_dict is not None:
		# Decode byte key-value pairs to string within each dictionary of 'redis_list_dict'.
		i = 0
		for dict_items in redis_list_dict:
			temp_dict = {}
			temp_dict.clear()
			for key, value in dict_items.items():
				temp_dict[key.decode('utf-8')] = value.decode('utf-8')
			redis_list_dict[i] = temp_dict
			i = i + 1
		return render_template('index.html', redis_list_dict=redis_list_dict)
	else:
		return render_template('index.html', redis_list_dict=None)
	

if __name__ == '__main__':
	webapp.run(debug=True)
