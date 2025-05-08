import uuid
from dataclasses import dataclass, field


@dataclass
class Book:
    id: str = field(default=str(uuid.uuid4()))
    title: str = field(default="", metadata={"required": True, "max_length": 15})
    author: str = field(default="", metadata={"required": True})


books = [
    Book(
        id=str(uuid.uuid4()),
        title="First Book",
        author="First Author",
    ),
    Book(
        id=str(uuid.uuid4()),
        title="Second Book",
        author="Second Author",
    )
]