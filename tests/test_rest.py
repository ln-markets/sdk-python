import unittest
import os
from dotenv import load_dotenv

from lnmarkets import LNMClient
from lnmarkets.user import get_user

load_dotenv()

class TestRest(unittest.TestCase):
  def test_rest(self):
    client = LNMClient({
      'network': 'testnet',
      'key': os.getenv('LNM_API_KEY'),
      'secret': os.getenv('LNM_API_SECRET'),
      'passphrase': os.getenv('LNM_API_PASSPHRASE'),
    })
    
    user_info = get_user(client)
    
    self.assertRegex(user_info['uid'], r'^[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}$')


if __name__ == '__main__':
  unittest.main()
