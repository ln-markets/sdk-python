import json
from typing import List, TypedDict
from lnmarkets import LNMClient
from lnmarkets.notifications.types import Notification


def get_all_notifications(client: LNMClient) -> List[Notification]:
  """
  @see https://docs.lnmarkets.com/api/operations/notificationsfetchnotifications
  """
  return json.loads(client.request_api('GET', '/notifications', {}, True))