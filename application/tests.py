"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- tests.py --

@author: Informed Solutions
"""
import json
import unittest

from django.conf import settings
from django.test import Client


class TestApi(unittest.TestCase):

    def test_search_postcode(self):
        """
        A test for running a postcode search
        :return: a success or fail value to the test runner to be reported on completion (see assert on response code)
        """
        self.client = Client()
        postcode = "WA14 4PA"
        header = {'content-type': 'application/json'}
        response = self.client.get(settings.BASE_URL + 'arc-service/api/v1/addresses/' + postcode + '/',
                                   headers=header)
        self.assertEqual(response.status_code, 200)

    def test_long_search_postcode(self):
        """
        A test for running a postcode search with a postcode that is too long
        :return: a success or fail value to the test runner to be reported on completion (see assert on response code)
        """
        # Test updating the APi Key
        self.client = Client()
        header = {'content-type': 'application/json'}
        payload = {'api_key': settings.OS_API_KEY}
        response = self.client.put(settings.URL_PREFIX + '/api/v1/addresses/api-key/', json.dumps(payload),
                                   'application/json', header=header)
        self.assertEqual(response.status_code, 200)

        postcode = "WA144PAAAAA"

        response = self.client.get(settings.BASE_URL + 'arc-service/api/v1/addresses/' + postcode + '/',
                                   headers=header)
        self.assertEqual(response.status_code, 400)

    def test_short_search_postcode(self):
        """
        A test for running a postcode search with a postcode that is too short
        :return: a success or fail value to the test runner to be reported on completion (see assert on response code)
        """
        # Test updating the APi Key
        self.client = Client()
        header = {'content-type': 'application/json'}
        payload = {'api_key': settings.OS_API_KEY}
        response = self.client.put(settings.URL_PREFIX + '/api/v1/addresses/api-key/', json.dumps(payload),
                                   'application/json', header=header)
        self.assertEqual(response.status_code, 200)

        postcode = "WA144"

        response = self.client.get(settings.BASE_URL + 'arc-service/api/v1/addresses/' + postcode + '/',
                                   headers=header)
        self.assertEqual(response.status_code, 400)

    def test_invalid_search_postcode(self):
        """
        A test for running a postcode search with an invalid postcode (no matches)
        :return: a success or fail value to the test runner to be reported on completion (see assert on response code)
        """
        # Test updating the APi Key
        self.client = Client()
        header = {'content-type': 'application/json'}
        payload = {'api_key': settings.OS_API_KEY}
        response = self.client.put(settings.URL_PREFIX + '/api/v1/addresses/api-key/', json.dumps(payload),
                                   'application/json', header=header)
        self.assertEqual(response.status_code, 200)

        postcode = "1111111"

        response = self.client.get(settings.BASE_URL + 'arc-service/api/v1/addresses/' + postcode + '/',
                                   headers=header)
        self.assertEqual(response.status_code, 400)

    def test_api_key(self):
        """
        Test updating the api key
        :return: a success or fail value to the test runner to be reported on completion (see assert on response code)
        """

        self.client = Client()
        header = {'content-type': 'application/json'}
        payload = {'api_key': '1098701985710937'}
        response = self.client.put(settings.URL_PREFIX + '/api/v1/addresses/api-key/', json.dumps(payload),
                                   'application/json', header=header)
        self.assertEqual(response.status_code, 200)

    def test_empty_api_key(self):
        """
        Test a bad request for updating the api key (cannot be empty)
        :return: a success or fail value to the test runner to be reported on completion (see assert on response code)
        """
        self.client = Client()
        header = {'content-type': 'application/json'}
        payload = {'api_key': ''}
        response = self.client.put(settings.URL_PREFIX + '/api/v1/addresses/api-key/', json.dumps(payload),
                                   'application/json', header=header)
        self.assertEqual(response.status_code, 400)
