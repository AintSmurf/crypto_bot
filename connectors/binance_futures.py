import logging
from utilities.request_utility import RequestsUtility
from utilities.credentials_utility import CredentialsUtility
from helpers.binance_futures_helper import *
from models.candle import Candle
from models.balance import Balance
from models.contracts import Contracts
import time
import websocket
import threading
import json

logger = logging.getLogger()


class BinanceFuturesClient:

    def __init__(self, testnet: bool) -> None:
        # generate keys for api connection
        creds_class = CredentialsUtility()
        self.creds = creds_class.get_api_keys()
        # prepare the biance url
        self.headers = {"X-MBX-APIKEY": self.creds["PUBLIC_KEY"]}
        if testnet:
            self.request_utility = RequestsUtility("https://testnet.binancefuture.com")
            self.wss_url = "wss://stream.binancefuture.com/ws"
        else:
            self.request_utility = RequestsUtility("https://fapi.binance.com")
            self.wss_url = "wss://fstream.binance.com"
        # verify initializion
        logger.info("Binance Futures Client successfilly initialized")

        # initilaize contracts balances prices logs for later use
        self.contracts = self.get_contracts()
        self.balances = self.get_balances()
        self.prices = dict()
        self.logs = []

        # create threading for the websocket
        self.connected_event = threading.Event()
        # run the websocket on paraller
        self.ws_id = 1
        self.ws = None
        t = threading.Thread(target=self._start_ws)
        t.daemon = True
        t.start()

    # start websocket connection
    def _start_ws(self):
        self.ws = websocket.WebSocketApp(
            self.wss_url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
        )
        # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
        while True:
            try:
                self.ws.run_forever(reconnect=5)
            except Exception as err:
                logger.error("connection to websocket failed\nreason: %s", err)

    def _add_log(self, msg):
        logger.info("%s", msg)
        self.logs.append({"log": msg, "displayed": False})

    def _on_message(self, ws, message: str):
        response = json.loads(message)
        if "e" in response:
            if response["e"] == "bookTicker":
                symbol = response["s"]
                logger.info(
                    "successfully extracted the message from the websocket: %s", symbol
                )
                if symbol not in self.prices:
                    self.prices[symbol] = {
                        "bid": float(response["b"]),
                        "ask": float(response["a"]),
                    }
                else:
                    self.prices[symbol]["bid"] = float(response["b"])
                    self.prices[symbol]["ask"] = float(response["a"])

    def _on_error(self, ws, error: str):
        print(error)

    def _on_close(self, ws, close_status_code: int, close_msg: str):
        logger.info("Binance Futures connection Closed")

    def _on_open(self, ws):
        logger.info("Opened connection to Binance Futures")
        self.subscribe(list(self.contracts.values()), "bookTicker")

    def subscribe(self, contracts: typing.List[Contracts], channel: str):
        payload = dict()
        payload["method"] = "SUBSCRIBE"
        payload["params"] = []
        for contract in contracts:
            payload["params"].append(contract.symbol.lower() + "@" + channel)
        payload["id"] = self.ws_id
        try:
            self.ws.send(json.dumps(payload))

        except Exception as err:
            logger.error("Failed to subsucribe to the websocket ...\nreason: %s", err)
        self.ws_id += 1

    # get the contracts from binance futures
    def get_contracts(self) -> typing.Dict[str, Contracts]:
        endpoint = "/fapi/v1/exchangeInfo"
        contracts = dict()
        response = self.request_utility.get(endpoint=endpoint)
        for contract_data in response["symbols"]:
            contracts[contract_data["pair"]] = Contracts(contract_data)
        return contracts

    # get historical candles based on the interval and symbol
    def get_historical_candles(
        self, contract: Contracts, interval: int, start_time: str, end_time: str
    ) -> list[Candle]:
        payload = dict()
        candles = []
        logger.info(
            "Retriving Historical candles \nfrom:%s to:%s\nsymbol:%s , interval:%s",
            start_time,
            end_time,
            contract.symbol,
            interval,
        )
        payload["symbol"] = contract.symbol
        payload["interval"] = interval
        if start_time:
            payload["startTime"] = date_to_timestamp(start_time)
        if end_time:
            payload["endTime"] = date_to_timestamp(end_time)
        endpoint = "/fapi/v1/klines"
        response = self.request_utility.get(endpoint=endpoint, payload=payload)
        for c in response:
            candles.append(Candle(c))
        return candles

    def get_bid_ask(self, contract: Contracts) -> typing.Dict[str, int]:
        payload = dict()
        endpoint = "/fapi/v1/ticker/bookTicker"
        payload["symbol"] = contract.symbol
        response = self.request_utility.get(endpoint=endpoint, payload=payload)
        if contract.symbol not in self.prices:
            self.prices[contract.symbol] = {
                "bid": float(response["bidPrice"]),
                "ask": float(response["askPrice"]),
            }
        else:
            self.prices[contract.symbol]["bid"] = float(response["bidPrice"])
            self.prices[contract.symbol]["ask"] = float(response["askPrice"])
        return self.prices[contract.symbol]

    def get_balances(self) -> typing.Dict[str, Balance]:
        logger.info("retriving wallet balance ..")
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
            bl = Balance(balance)
            balances[bl.asset] = bl.wallet_balance
        logger.info("Current Balance:\n%s", balances)
        return balances

    def place_order(
        self,
        contract: Contracts,
        side: str,
        quantity: float,
        order_type: str,
        price: None,
        tif: None,
    ):
        payload = dict()
        payload["symbol"] = contract.symbol
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
            contract.symbol,
            side,
            quantity,
            order_type,
            price,
        )
        return response

    def cancel_order(self, contract: Contracts, order_id: int):
        payload = dict()
        payload["symbol"] = contract.symbol
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

    def get_all_orders(self, contract: Contracts):
        payload = dict()
        payload["symbol"] = contract.symbol
        payload["timestamp"] = int(time.time() * 1000)
        payload["signature"] = generate_signature(
            payload=payload, api_secret=self.creds["SECRET_KEY"]
        )
        endpoint = "/fapi/v1/allOrders"
        response = self.request_utility.get(
            endpoint=endpoint, payload=payload, headers=self.headers
        )
        return response

    def get_order_status(self, contract: Contracts, order_id: int):
        payload = dict()
        payload["symbol"] = contract.symbol
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
