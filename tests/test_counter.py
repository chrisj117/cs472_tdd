"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app

# we need to import the file that contains the status codes
from src import status

import json


class CounterTest(TestCase):
    """Counter tests"""

    def setUp(self):
        self.client = app.test_client()

    def test_create_a_counter(self):
        """It should create a counter"""
        client = app.test_client()
        result = client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    # Steps are from professor's github writeup
    def test_update_a_counter(self):
        """It should successfully increment a counter"""
        # Make a call to Create a counter.
        result = self.client.post('/counters/test')
        # Ensure that it returned a successful return code.
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        # Check the counter value as a baseline.
        baseline = result.data
        # Make a call to Update the counter that you just created.
        updated = self.client.put('/counters/test')
        # Ensure that it returned a successful return code.
        self.assertEqual(updated.status_code, status.HTTP_200_OK)
        # Check that the counter value is one more than the baseline you measured in step 3.
        newCount = updated.data
        old = json.loads(baseline)
        new = json.loads(newCount)
        self.assertEqual(old['test']+1, new['test'])

    def test_read_a_counter(self):
        """It should successfully read a counter"""
        # Create a counter
        result = self.client.post('/counters/test2')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        # Read from the counter
        read = self.client.get('/counters/test2')
        # Status should be 200_OK and no values should be changed
        self.assertEqual(read.status_code, status.HTTP_200_OK)
        self.assertEqual(read.data, result.data)
        # Bad get call should return 404
        badRead = self.client.get('/counters/test3')
        self.assertEqual(badRead.status_code, status.HTTP_404_NOT_FOUND)
