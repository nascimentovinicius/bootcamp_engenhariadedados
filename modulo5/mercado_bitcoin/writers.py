import datetime
import os
import json
from typing import List

class DataTypeNotSupportedForIngestionException(Exception):
    def __init__(self, data) -> None:
        self.data = data
        self.message = f"Datatype {type(data)} is not supported for ingestion"
        super().__init__(self.message)

class DataWriter:
    def __init__(self, coin: str, api: str) -> None:
        self.api = api
        self.coin = coin
        self.filename = f"{self.api}/{self.coin}/{str(datetime.datetime.now()).replace(':','-')}.txt"

    def _write_row(self, row: str) -> None:
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        with open(self.filename, 'a') as f:
            f.write(row)

    def write(self, data: [List, dict]):
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + "\n")
        elif isinstance(data, List):
            for item in data:
                self.write(item)
        else:
            raise DataTypeNotSupportedForIngestionException(data)