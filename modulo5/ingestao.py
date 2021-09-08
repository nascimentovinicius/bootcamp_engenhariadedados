import os
from typing import List
import requests
import logging
import datetime
import json
import time
import ratelimit
from backoff import on_exception, expo
from schedule import repeat, every, run_pending
from abc import ABC, abstractmethod

#url = "https://www.mercadobitcoin.net/api/BTC/day-summary/2021/06/23"
#ret = requests.get(url).json()
#print(ret)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MercadoBitcoinAPI(ABC):

    def __init__(self, coin: str) -> None:
        self.coin = coin
        self.base_endpoint = "https://www.mercadobitcoin.net/api"

    @abstractmethod
    def _get_endpoint(self, **kwargs) -> str:
        pass

    @on_exception(expo, ratelimit.RateLimitException, max_tries=10)
    @ratelimit.limits(calls=29, period=30)
    @on_exception(expo, requests.exceptions.HTTPError, max_time=10)
    def get_data(self, **kwargs) -> dict:
        endpoint = self._get_endpoint(**kwargs)
        logger.info(f"Getting data from endpoint: {endpoint}")
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()

class DaySummaryAPI(MercadoBitcoinAPI):
    type = "day-summary"

    def _get_endpoint(self, date: datetime.date) -> str:
        return f"{self.base_endpoint}/{self.coin}/{self.type}/{date.year}/{date.month}/{date.day}"


class TradesAPI(MercadoBitcoinAPI):
    type = "trades"

    def _get_unix_epoch(self, date: datetime.datetime) -> int:
        return int(date.timestamp())

    def _get_endpoint(self, date_from: datetime.datetime = None, date_to: datetime.datetime = None) -> str:
        if date_from and not date_to:
            unix_date_from = self._get_unix_epoch(date_from)
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}"
        elif date_from and date_to:
            unix_date_from = self._get_unix_epoch(date_from)
            unix_date_to = self._get_unix_epoch(date_to)
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}/{unix_date_to}"
        else:
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}"

        return endpoint

def test_get_data():
    print(DaySummaryAPI(coin="BTC").get_data(date=datetime.date(2021, 6,23)))
    print(TradesAPI(coin="BTC").get_data())
    print(TradesAPI(coin="BTC").get_data(date_from=datetime.datetime(2021,9,1)))
    print(TradesAPI(coin="BTC").get_data(date_from=datetime.datetime(2021,9,1), date_to=datetime.datetime(2021,9,2)))


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

def test_DataWriter():  
    day_summary = DaySummaryAPI(coin="BTC").get_data(date=datetime.date(2021,9,1))
    writer = DataWriter("day_summary.txt")
    writer.write(data=day_summary)


    trades = TradesAPI(coin="BTC").get_data(date_from=datetime.datetime(2021,9,1), date_to=datetime.datetime(2021,9,2))
    writer = DataWriter("trades.txt")
    writer.write(data=trades)


class DataIngestor(ABC):
    def __init__(self, coins: List[str], default_start_date: datetime.date, writer: DataWriter) -> None:
        self.coins = coins
        self.default_start_date = default_start_date
        self.writer = writer
        self._checkpoint = self._load_checkpoint()

    def _get_checkpoint(self):
        if not self._checkpoint:
            return self.default_start_date
        else:
            return self._checkpoint

    @property
    def _checkpoint_filename(self) -> str:
        return f"{self.__class__.__name__}.checkpoint"

    def _write_checkpoint(self):
        with open(self._checkpoint_filename, 'w') as f:
            f.write(f"{self._checkpoint}")

    def _load_checkpoint(self) -> datetime.date:
        try:
            with open(self._checkpoint_filename, 'r') as f:
                return datetime.datetime.strptime(f.read(), "%Y-%m-%d").date()
        except FileNotFoundError:
            return None

    def _update_checkpoint(self, value):
        self._checkpoint = value
        self._write_checkpoint()

    @abstractmethod
    def ingest(self) -> None:
        pass


class DaySummaryIngestor(DataIngestor):
    def __init__(self, coins: List[str], default_start_date: datetime.date, writer: DataWriter) -> None:
        super().__init__(coins, default_start_date, writer)

    def ingest(self) -> None:
        date = self._get_checkpoint()
        if date < datetime.date.today():
            for coin in self.coins:
                api = DaySummaryAPI(coin=coin)
                data = api.get_data(date=date)
                self.writer(coin=coin, api=api.type).write(data)
            self._update_checkpoint(date + datetime.timedelta(days=1))

def test_day_summary_ingestor():
    dsi = DaySummaryIngestor(coins=['BTC','ETH','LTC'], default_start_date=datetime.date(2021,9,1), writer=DataWriter)
    dsi.ingest()


dsi = DaySummaryIngestor(coins=['BTC','ETH','LTC'], default_start_date=datetime.date(2021,8,20), writer=DataWriter)
@repeat(every(1).seconds)
def job():
    dsi.ingest()

while True:
    run_pending()
    time.sleep(1)