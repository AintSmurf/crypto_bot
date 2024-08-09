import tkinter as tk
import logging
from connectors.binance_futures import BinanceFuturesClient
from pprint import pprint

# import logging to store logs in info.log also log info on the terminal
logger = logging.getLogger()

# set up stream handler for terminal logs
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(levelname)s :: %(message)s")
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

# set up file handler for logs to debug later on
file_handler = logging.FileHandler("info.log")
file_handler.setFormatter(stream_handler)
file_handler.setLevel(logging.DEBUG)

# add created habdlers to the logger
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

# starting point
if __name__ == "__main__":
    # initialze binance future client
    binance_futures_client = BinanceFuturesClient(True)
    # binance_futures_contracts = binance_futures_client.get_contracts()
    # binance_futures_client.get_bid_ask("BTCUSDT")
    # binance_futures_client.get_historical_candles("BTCUSDT", "15m")
    # print(binance_futures_client.get_balances())
    # pprint(
    #     binance_futures_client.place_order(
    #         "BTCUSDT", "BUY", 0.008, "LIMIT", 60298.9, "GTC"
    #     )
    # )
    # pprint(binance_futures_client.get_order_status("BTCUSDT", 4053290335))
    # pprint(binance_futures_client.cancel_order("BTCUSDT", 4053290335))

    # initalize new tkinter window
    main_window = tk.Tk()
    main_window.mainloop()
