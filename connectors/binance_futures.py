import logging
from utilities.request_utility import RequestsUtility
from utilities.credentials_utility import CredentialsUtility
from helpers.binance_futures_helper import generate_signature
import time

logger = logging.getLogger()


class BinanceFuturesClient:

    def __init__(self, testnet) -> None:
        creds_class = CredentialsUtility()
        self.creds = creds_class.get_api_keys()
        self.headers = {"X-MBX-APIKEY": self.creds["PUBLIC_KEY"]}
        if testnet:
            self.request_utility = RequestsUtility("https://testnet.binancefuture.com")
        else:
            self.request_utility = RequestsUtility("https://fapi.binance.com")
        self.prices = dict()
        logger.info("Binance Futures Client successfilly initialized")

    # get the contracts from binance futures
    def get_contracts(self):
        endpoint = "/fapi/v1/exchangeInfo"
        contracts = []
        response = self.request_utility.get(endpoint=endpoint)
        for contract in response["symbols"]:
            contracts.append(contract["pair"])
        return contracts

    # get historical candles based on the interval and symbol
    def get_historical_candles(self, symbol, interval):
        payload = dict()
        candles = []
        endpoint = "/fapi/v1/klines"
        payload["symbol"] = symbol
        payload["interval"] = interval
        response = self.request_utility.get(endpoint=endpoint, payload=payload)
        for candle in response:
            candles.append(
                [
                    candle[0],
                    float(candle[1]),
                    float(candle[2]),
                    float(candle[3]),
                    float(candle[4]),
                    float(candle[5]),
                ]
            )
        return candles

    def get_bid_ask(self, symbol):
        payload = dict()
        endpoint = "/fapi/v1/ticker/bookTicker"
        payload["symbol"] = symbol
        response = self.request_utility.get(endpoint=endpoint, payload=payload)
        if symbol not in self.prices:
            self.prices[symbol] = {
                "bid": float(response["bidPrice"]),
                "ask": float(response["askPrice"]),
            }
        else:
            self.prices[symbol]["bid"] = float(response["bidPrice"])
            self.prices[symbol]["ask"] = float(response["askPrice"])
        return self.prices[symbol]

    def get_balances(self):
        payload = dict()
        balances = dict()
        payload["timestamp"] = int(time.time() * 1000)
        payload["signature"] = generate_signature(
            payload=payload, api_secret=self.creds["SECRET_KEY"]
        )
        endpoint = "/fapi/v3/account"
        response = self.request_utility.get(
            endpoint=endpoint, payload=payload, headers=self.headers
        )
        for balance in response["assets"]:
            balances[balance["asset"]] = balance["walletBalance"]
        return balances

    def place_order(self, symbol, side, quantity, order_type, price=None, tif=None):
        payload = dict()
        payload["symbol"] = symbol
        payload["side"] = side
        payload["quantity"] = quantity
        payload["type"] = order_type
        if price:
            payload["price"] = price
        if tif:
            payload["timeInForce"] = tif
        payload["timestamp"] = int(time.time() * 1000)
        payload["signature"] = generate_signature(
            payload=payload, api_secret=self.creds["SECRET_KEY"]
        )
        endpoint = "/fapi/v1/order"
        response = self.request_utility.post(
            endpoint=endpoint, payload=payload, headers=self.headers
        )
        return response

    def cancel_order(self, symbol, order_id):
        payload = dict()
        payload["symbol"] = symbol
        payload["orderId"] = order_id
        payload["timestamp"] = int(time.time() * 1000)
        payload["signature"] = generate_signature(
            payload=payload, api_secret=self.creds["SECRET_KEY"]
        )
        endpoint = "/fapi/v1/order"
        response = self.request_utility.delete(
            endpoint=endpoint, payload=payload, headers=self.headers
        )
        return response

    def get_order_status(self, symbol, order_id):
        payload = dict()
        payload["symbol"] = symbol
        payload["orderId"] = order_id
        payload["timestamp"] = int(time.time() * 1000)
        payload["signature"] = generate_signature(
            payload=payload, api_secret=self.creds["SECRET_KEY"]
        )
        endpoint = "/fapi/v1/order"
        response = self.request_utility.get(
            endpoint=endpoint, payload=payload, headers=self.headers
        )
        return response
