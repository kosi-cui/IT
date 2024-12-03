import unittest
from server.agent import Agent
from dotenv import load_dotenv
import os

class TestAgent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        load_dotenv()  # take environment variables from .env.
        cls.agent = Agent(os.getenv('API_KEY'), os.getenv('HELPDESK_URL'))

    def test_tasksGetRequest(self):
        # You can now use self.agent in your tests
        ticket_id = 30412
        response = self.agent.tasksGetRequest(ticket_id)
        expected = "Label Device"
        print("=-=-=-=-=-=-=-=-=-=-")
        print(f'Testing function: tasksGetRequest')
        print(f'Expected output: {expected}')
        print(f'Actual output: {response[0]}')
        print("=-=-=-=-=-=-=-=-=-=-\n")
        possible = ["Label Device", "Decrypt Bitlocker", "Create a Data Backup", "Upgrade Hardware", "Configure BIOS", "Load the Image", "Verify Computer Name/Installed Software", "Update Windows and BIOS", "Load Data Backup", "Encrypt Bitlocker"]
        self.assertIn(response[0], possible)