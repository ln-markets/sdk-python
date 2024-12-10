from lnmarkets import UUID
from typing import TypedDict, Any


class Notification(TypedDict):
  creation_ts: int
  data: Any
  event: str
  id: UUID
