from lnmarkets import LNMClient


def mark_all_notifications_as_read(client: LNMClient) -> None:
  """
  @see https://docs.lnmarkets.com/api/operations/notificationsmarkallnotificationsasread
  """
  client.request_api('DELETE', '/notifications/all', {}, True)
