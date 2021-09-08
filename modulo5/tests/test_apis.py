import datetime
from mercado_bitcoin.apis import DaySummaryAPI, TradesAPI, MercadoBitcoinAPI
import pytest
import requests
from unittest.mock import mock_open, patch

class TestDaySummaryAPI:
    def test_get_endpoint_ETH(self):
        date = datetime.date(2021,6,21)
        api = DaySummaryAPI(coin='ETH')
        actual = api._get_endpoint(date=date)
        expected = "https://www.mercadobitcoin.net/api/ETH/day-summary/2021/6/21"
        assert actual == expected

    @pytest.mark.parametrize(
        "coin, date, expected",
        [
            ("BTC", datetime.date(2021,6,21), "https://www.mercadobitcoin.net/api/BTC/day-summary/2021/6/21")
            ,("ETH", datetime.date(2021,6,21), "https://www.mercadobitcoin.net/api/ETH/day-summary/2021/6/21")
            ,("ETH", datetime.date(2020,7,21), "https://www.mercadobitcoin.net/api/ETH/day-summary/2020/7/21")
        ]
    )
    def test_get_endpoint(self, coin, date, expected):
        api = DaySummaryAPI(coin=coin)
        actual = api._get_endpoint(date=date)
        assert actual == expected

class TestTradesAPI:
    @pytest.mark.parametrize(
        "coin, date_from, date_to, expected",
        [
            ("TEST", datetime.datetime(2019,1,1), datetime.datetime(2019,1,2)
                , 'https://www.mercadobitcoin.net/api/TEST/trades/1546311600/1546398000'),
            ("TEST", datetime.datetime(2019,1,2), datetime.datetime(2019,7,20)
                , 'https://www.mercadobitcoin.net/api/TEST/trades/1546398000/1563591600'),
            ("TEST", datetime.datetime(2019,1,1), None
                , 'https://www.mercadobitcoin.net/api/TEST/trades/1546311600'),
            ("TEST", None, None
                , 'https://www.mercadobitcoin.net/api/TEST/trades'),
            ("TEST", None, datetime.datetime(2019,7,20)
                , 'https://www.mercadobitcoin.net/api/TEST/trades')
        ]
    )
    def test_get_endpoint(self, coin, date_from, date_to, expected):
        actual = TradesAPI(coin=coin)._get_endpoint(date_from=date_from, date_to=date_to)
        assert actual == expected

    @pytest.mark.parametrize(
        "date_from, date_to, expected",
        [
            (datetime.datetime(2019,7,20), datetime.datetime(2019,1,1)
                , 'https://www.mercadobitcoin.net/api/TEST/trades'),
        ]
    )
    def test_get_endpoint_date_from_greater_than_date_to(self, date_from, date_to, expected):
        with pytest.raises(RuntimeError):
            TradesAPI(coin="TEST")._get_endpoint(date_from=date_from, date_to=date_to)
        

    @pytest.mark.parametrize(
        "date, expected",
        [
            (datetime.datetime(2019,1,1), 1546311600),
            (datetime.datetime(2019,1,1,0,0,5), 1546311605),
            (datetime.datetime(2019,1,2), 1546398000),
            (datetime.datetime(2019,7,20), 1563591600),
            (datetime.datetime(2019,10,1,0,0,5), 1569898805),
        ]
    )
    def test_get_unix_epoch(self, date, expected):
        actual = TradesAPI(coin="TEST")._get_unix_epoch(date=date)
        assert actual == expected

@pytest.fixture()
@patch("mercado_bitcoin.apis.MercadoBitcoinAPI.__abstractmethods__", set())
def fixture_mercadobitcoinapi():
    return MercadoBitcoinAPI(coin="TEST")

def mocked_requests_get(*args, **kwargs):
    class MockResponse(requests.Response):
        def __init__(self, json_data, status_code):
            super().__init__()
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def raise_for_status(self) -> None:
            if self.status_code != 200:
                raise Exception

    if args[0] == 'valid_endpoint':
        return MockResponse(json_data={"foo": "bar"}, status_code=200)
    else:
        return MockResponse(json_data=None, status_code=404)


@patch("mercado_bitcoin.apis.MercadoBitcoinAPI.__abstractmethods__", set())
class TestMercadoBitcoinAPI:

    @patch("requests.get")
    @patch("mercado_bitcoin.apis.MercadoBitcoinAPI._get_endpoint", return_value="valid_endpoint")
    def test_get_data_requests_is_called(self, mock_get_endpoint, mock_requests, fixture_mercadobitcoinapi):
        fixture_mercadobitcoinapi.get_data()
        mock_requests.assert_called_once_with("valid_endpoint")

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("mercado_bitcoin.apis.MercadoBitcoinAPI._get_endpoint", return_value="valid_endpoint")
    def test_get_data_with_valid_endpoint(self, mock_get_endpoint, mock_requests, fixture_mercadobitcoinapi):
        actual = fixture_mercadobitcoinapi.get_data()
        expected = {"foo": "bar"}
        assert actual == expected

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("mercado_bitcoin.apis.MercadoBitcoinAPI._get_endpoint", return_value="invalid_endpoint")
    def test_get_data_with_invalid_endpoint(self, mock_get_endpoint, mock_requests, fixture_mercadobitcoinapi):
        with pytest.raises(Exception):
            fixture_mercadobitcoinapi.get_data()