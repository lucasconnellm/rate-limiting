from datetime import datetime
from typing import Optional

from exceptions.base import CustomException


class LimitExceededException(CustomException):
    next_allowed: Optional[datetime]

    def __init__(self, *args: object, next_allowed: Optional[datetime] = None):
        self.next_allowed = next_allowed
        super().__init__(*args)
