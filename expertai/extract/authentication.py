import os

import base64
import json
import ssl
import time
import urllib3
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Authentication:
    __access_token = None
    __authorization_host = None

    def __init__(self, authorization_host=None):
        if authorization_host is None:
            self.__authorization_host = "https://developer.expert.ai/oauth2/token"
        else:
            self.__authorization_host = authorization_host

    @property
    def __username(self):
        username = os.getenv("EAI_USERNAME")
        if not username:
            raise Exception("Missing username env variable")
        return username

    @property
    def __password(self):
        password = os.getenv("EAI_PASSWORD")
        if not password:
            raise Exception("Missing password env variable")
        return password

    @property
    def __is_jwt_token(self):
        payload_base64 = self.__access_token.split(".")
        if len(payload_base64) == 3:
            return True
        return False

    def set_access_token(self, token):
        self.__access_token = token

    def set_authorization_host(self, authorization_host):
        self.__authorization_host = authorization_host

    def token_is_expired(self):
        if not self.__access_token or not self.__is_jwt_token:
            return True

        payload_base64 = self.__access_token.split(".")[1]

        if len(payload_base64) % 4 != 0:
            payload_base64 = payload_base64 + '=' * (4 - len(payload_base64) % 4)

        payload_decoded = base64.b64decode(payload_base64)
        exp = json.loads(payload_decoded).get('exp')

        current_date = round(time.time())

        return exp is not None and current_date >= exp

    def generate_token(self):
        username = self.__username
        password = self.__password
        encoded_body = json.dumps({
            "username": username,
            "password": password
        }).encode('utf-8')

        response = self.__make_request_with_body(encoded_body)

        if response.status != 200:
            raise Exception(f"Failed authentication with status: {response.status} and reason: {response.reason}")

        return response.data.decode('utf-8')

    def __create_http_configuration(self):
        return urllib3.PoolManager(cert_reqs=ssl.CERT_NONE)

    def __make_request_with_body(self, encoded_body):
        return self.__create_http_configuration().request(
            "POST",
            self.__authorization_host,
            body=encoded_body,
            headers={"Content-Type": "application/json"}
        )

    def get_access_token(self):
        if self.__access_token and not self.token_is_expired():
            return self.__access_token

        self.__access_token = self.generate_token()
        return self.__access_token

