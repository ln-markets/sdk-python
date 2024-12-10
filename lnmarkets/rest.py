import os

from typing import Literal, TypedDict
from urllib.parse import urlencode
from datetime import datetime
from base64 import b64encode
from requests import request

import hashlib
import hmac
import json

type Network = Literal['mainnet', 'testnet']
type Method = Literal['GET', 'POST', 'PUT', 'DELETE']

def _get_hostname(network: Network) -> str:
	hostname = os.getenv('LNMARKETS_API_HOSTNAME')
	
	if hostname:
		return hostname
	elif network == 'testnet':
		return 'api.testnet.lnmarkets.com'
	else:
		return 'api.lnmarkets.com'
	
class _LNMOptions(TypedDict):
	key: str
	secret: str
	passphrase: str
	network: Network
	hostname: str
	custom_headers: dict[str, str]
	skip_api_key: bool

class LNMClient():
	def __init__(self, options: _LNMOptions):
		self.key = options.get('key', os.getenv('LNMARKETS_API_KEY'))
		self.secret = options.get('secret', os.getenv('LNM_API_SECRET'))
		self.passphrase = options.get('passphrase', os.getenv('LNM_API_PASSPHRASE'))
		self.network = options.get('network', os.getenv('LNM_API_NETWORK', 'mainnet'))
		self.hostname = _get_hostname(self.network)
		self.custom_headers = options.get('custom_headers')
		self.skip_api_key = options.get('skip_api_key', False)

	def _request_options(self, **options: dict[str, str | dict | bool]) -> dict:
		credentials: str = options.get('credentials')
		method = options.get('method')
		path = options.get('path')
		params = options.get('params')
		opts = { 'headers': {} }

		if method != 'DELETE':
			opts['headers']['Content-Type'] = 'application/json'

		if self.custom_headers:
			opts['headers'].update(**self.custom_headers)

		if method in ['GET', 'DELETE']:
				data = urlencode(params)
		elif method in ['POST', 'PUT']:
				data = json.dumps(params, separators=(',', ':'))
				
		if credentials and not self.skip_api_key:
			if not self.key:
				raise Exception('You need an API key to use an authenticated route')
			elif not self.secret:
				raise Exception('You need an API secret to use an authenticated route')
			elif not self.passphrase:
				raise Exception('You need an API passphrase to use an authenticated route')
			
			ts = str(int(datetime.now().timestamp() * 1000))

			payload = ts + method + '/v2' + path + data
			hashed = hmac.new(bytes(self.secret, 'utf-8'), bytes(payload, 'utf-8'), hashlib.sha256).digest()
			signature = b64encode(hashed)
			
			opts['headers']['LNM-ACCESS-KEY'] = self.key
			opts['headers']['LNM-ACCESS-PASSPHRASE'] = self.passphrase
			opts['headers']['LNM-ACCESS-TIMESTAMP'] = ts
			opts['headers']['LNM-ACCESS-SIGNATURE'] = signature

		opts['resource'] = 'https://' + self.hostname + '/v2' + path

		if method in ['GET', 'DELETE'] and params:
			opts['resource'] += '?' + data

		return opts

	def request_api(self, method: Method, path: str, params: dict, credentials: bool = False):
		options = {
			'method': method,
			'path': path,
			'params': params,
			'credentials': credentials
		}

		opts = self._request_options(**options)
		resource = opts.get('resource')
		headers = opts.get('headers')

		if method in ['GET', 'DELETE']:
			response = request(method, resource, headers = headers)
		elif method in ['POST', 'PUT']:
			response = request(method, resource, data = json.dumps(params, separators=(',', ':')), headers = headers)

		return response.text
	