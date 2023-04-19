from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from bson import ObjectId
from dateutil import parser


@dataclass
class News:
    source: str
    title: str
    summary: str
    author: str
    published_time: datetime
    link: str
    category: str

    _id: Optional[str] = None

    def __post_init__(self):
        self._id = str(ObjectId())
        self.published_time = (
            parser.isoparse(self.published_time)
            if isinstance(self.published_time, str)
            else self.published_time
        )
