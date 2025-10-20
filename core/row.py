import uuid
from typing import List, Any

class Row:
    def __init__(self, table, values: List[Any]):
        self.table = table
        self.values = values
        self.id = uuid.uuid4().hex

    def __getitem__(self, item):
        return self.values[item]