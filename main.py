import logging
from connectors.binance_futures import BinanceFuturesClient
from pprint import pprint
from interface.main_window import Root
import tkinter as tk

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
    # initialze binance future client and pass the UI

    binance_futures_client = BinanceFuturesClient(True)
    main_window = Root(binance_futures_client)
    main_window.mainloop()
