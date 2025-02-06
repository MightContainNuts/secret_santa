import unittest
from unittest.mock import patch, MagicMock
import json
import random

from app import SecretSanta
class TestSecretSanta(unittest.TestCase):


    @patch('random.choice', return_value='Alice')
    def test_assign_secret_santa(self, mock_random):
        # Set up mock data
        secret_santa = SecretSanta(2025)
        secret_santa.data = {"John": {"non_partner": []}, "Alice": {"non_partner": []}}

        # Test assigning Secret Santa
        partner_1, partner_2 = secret_santa.assign_secret_santa("John")

        self.assertEqual(partner_1, "John")
        self.assertEqual(partner_2, "Alice")

    @patch('builtins.input', side_effect=['John', 'Alice'])
    @patch('random.choice', return_value='Alice')
    def test_add_non_partner_to_list(self, mock_random, mock_input):
        secret_santa = SecretSanta(2025)
        secret_santa.data = {"John": {"non_partner": []}, "Alice": {"non_partner": []}}

        # Test adding a non-partner to a participant's list
        secret_santa._append_non_partner("John", "Alice")

        self.assertIn("Alice", secret_santa.data["John"]["non_partner"])

    @patch('builtins.input', side_effect=['John', 'Alice'])
    @patch('random.choice', return_value='Alice')
    def test_add_new_participant(self, mock_random, mock_input):
        secret_santa = SecretSanta(2025)
        secret_santa.data = {"John": {"non_partner": []}, "Alice": {"non_partner": []}}

        # Test adding a new participant
        secret_santa.add_new_participant()

        self.assertIn("John", secret_santa.data)
        self.assertEqual(secret_santa.data["John"], {"non_partner": []})


    def test_create_santa_list(self):
        secret_santa = SecretSanta(2025)
        secret_santa.data = {"John": {"non_partner": []}, "Alice": {"non_partner": []}}
        secret_santa.assign_secret_santa = MagicMock(return_value=("John", "Alice"))

        # Test creating the Secret Santa list
        santa_list = secret_santa.create_santa_list()

        self.assertEqual(len(santa_list), 2)
        self.assertEqual(santa_list[0], ("John", "Alice"))


if __name__ == '__main__':
    unittest.main()
