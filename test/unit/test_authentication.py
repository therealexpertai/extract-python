import unittest

from expertai.extract.authentication import Authentication
from unittest.mock import patch
import time
import base64


class AuthenticationTestCase(unittest.TestCase):
    def setUp(self):
        self.authentication = Authentication()
        self.expired_access_token = "_.eyJleHAiOjE2NDI0OTMyMjZ9._"
        self.plain_text_token = "-1RDVOdFM1UHJBar"

    @patch("os.getenv", return_value=None)
    def test_the_username_env_is_not_set(self, patch_getenv):
        with self.assertRaises(Exception) as context:
            self.authentication.__username
            self.assertTrue("Missing username env variable" in str(context.exception))

    @patch("os.getenv", return_value=None)
    def test_the_password_env_is_not_set(self, patch_getenv):
        with self.assertRaises(Exception) as context:
            self.authentication.__password
            self.assertTrue("Missing password env variable" in str(context.exception))

    def test_token_is_expired(self):
        self.authentication.set_access_token(self.expired_access_token)
        is_expired = self.authentication.token_is_expired()
        self.assertTrue(is_expired)

    def test_token_is_not_expired(self):
        expire_time = round(time.time() + 3600)
        token_payload = f'{{"exp": {expire_time}}}'
        encode = base64.b64encode(token_payload.encode('ascii'))
        self.authentication.set_access_token(f"_.{encode.decode('ascii')}._")
        is_expired = self.authentication.token_is_expired()
        self.assertFalse(is_expired)

    @patch("expertai.extract.authentication.Authentication.generate_token", return_value="-1RDVOdFM1UHJBar")
    def test_get_access_token(self, patch_generate_token):
        generated_token = self.authentication.get_access_token()
        self.assertEqual(generated_token, self.plain_text_token)

    @patch("os.getenv", return_value="wrong_username")
    def test_authentication_failed(self, patch_getenv):
        with self.assertRaises(Exception) as context:
            self.authentication.__username
            self.assertTrue("Failed authentication with status: 401 and reason: Unauthorized" in str(context.exception))
