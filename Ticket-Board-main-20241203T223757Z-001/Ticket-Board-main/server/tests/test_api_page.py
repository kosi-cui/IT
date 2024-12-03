import unittest
from server.api_page import clean_string, reimage_ticket, get_all_reimage_tickets
from server.agent import Agent
from dotenv import load_dotenv
import os

class TestApiPage(unittest.TestCase):
    def test_clean_string(self):
        expected = 'test'
        actual = clean_string('<p>test</p>')
        print("=-=-=-=-=-=-=-=-=-=-")
        print(f'Testing function: clean_string')
        print(f'Expected output: {expected}')
        print(f'Actual output: {actual}')
        print("=-=-=-=-=-=-=-=-=-=-\n")
        self.assertEqual(actual, expected)

    def test_reimage_ticket(self):
        expected = {
            "title": "Test-Device",
            "agent": "Ethan Gray",
            "created_at": "03/20/2024",
            "tasks": ["Label Device", "Decrypt Bitlocker",
                      "Create a Data Backup", "Upgrade Hardware",
                      "Configure BIOS", "Load the Image",
                      "Verify Computer Name/Installed Software", "Update Windows and BIOS",
                      "Load Data Backup", "Encrypt Bitlocker"]
        }
        agent = Agent(os.getenv('API_KEY'), os.getenv('HELPDESK_URL'))
        actual = reimage_ticket(30412, agent)
        print("=-=-=-=-=-=-=-=-=-=-")
        print(f'Testing function: reimage_ticket')
        print(f'Expected output: {expected}')
        print(f'Actual output: {actual}')
        print("=-=-=-=-=-=-=-=-=-=-\n")
        self.assertDictEqual(actual, expected)

    def test_reimage_tickets(self):
        actual = get_all_reimage_tickets()
        print("=-=-=-=-=-=-=-=-=-=-")
        print(f'Testing function: reimage_tickets')
        print(f'Actual output: {len(actual)}')
        print("=-=-=-=-=-=-=-=-=-=-\n")
        self.assertIsInstance(actual, list)