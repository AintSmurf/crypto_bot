import logging
from utilities.request_utility import RequestsUtility
from utilities.credentials_utility import CredentialsUtility
from helpers.binance_futures_helper import generate_signature
import time
import websocket
import threading
import json

logger = logging.getLogger()


class BinanceFuturesClient:

    def __init__(self, testnet) -> None:
        creds_class = CredentialsUtility()
        self.creds = creds_class.get_api_keys()
        self.headers = {"X-MBX-APIKEY": self.creds["PUBLIC_KEY"]}
        if testnet:
            self.request_utility = RequestsUtility("https://testnet.binancefuture.com")
            self.wss_url = "wss://stream.binancefuture.com/ws"
        else:
            self.request_utility = RequestsUtility("https://fapi.binance.com")
            self.wss_url = "wss://fstream.binance.com"
        self.prices = dict()
        self.connected_event = threading.Event()
        logger.info("Binance Futures Client successfilly initialized")

        # run the websocket on paraller
        self.id = 1
        self.ws = None
        t = threading.Thread(target=self.start_ws)
        t.daemon = True
        t.start()

    # start websocket connection
    def start_ws(self):
        self.ws = websocket.WebSocketApp(
            self.wss_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
        self.ws.run_forever(reconnect=5)

    def on_message(self, ws, message):
        response = json.loads(message)
        if "e" in response:
            if response["e"] == "bookTicker":
                symbol = response["s"]
                if symbol not in self.prices:
                    self.prices[symbol] = {
                        "bid": float(response["b"]),
                        "ask": float(response["a"]),
                    }
                else:
                    self.prices[symbol]["bid"] = float(response["b"])
                    self.prices[symbol]["ask"] = float(response["a"])
                print(self.prices[symbol])

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        logger.info("Binance Futures connection Closed")

    def on_open(self, ws):
        logger.info("Opened connection to Binance Futures")
        self.connected_event.set()
        self.subscribe("BTCUSDT")

    def subscribe(self, symbol: str):
        payload = dict()
        payload["method"] = "SUBSCRIBE"
        payload["params"] = []
        payload["params"].append(symbol.lower() + "@bookTicker")
        payload["id"] = self.id
        self.ws.send(json.dumps(payload))
        self.id += 1

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
        logger.info("Current Balance:\n%s", balances)
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
        logger.info("order ID: %s", response["orderId"])
        logger.info(
            "order placed: symbol:%s, side:%s, quantity:%s, order_type:%s, price:%s",
            symbol,
            side,
            quantity,
            order_type,
            price,
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

    def get_all_orders(self, symbol):
        payload = dict()
        payload["symbol"] = symbol
        payload["timestamp"] = int(time.time() * 1000)
        payload["signature"] = generate_signature(
            payload=payload, api_secret=self.creds["SECRET_KEY"]
        )
        endpoint = "/fapi/v1/allOrders"
        response = self.request_utility.get(
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
