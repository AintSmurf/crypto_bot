import tkinter as tk
from interface.styling import *
from interface.logging_component import Logging
from connectors.binance_futures import BinanceFuturesClient
from interface.trades_component import TradesWatch
from interface.strategy_component import StrategyEditor


class Root(tk.Tk):

    def __init__(self, binance: BinanceFuturesClient) -> None:
        super().__init__()
        # initilaize required varibles
        self.binance = binance
        self.title("Crypto Trading Bot")
        self.configure(bg=BG_COLOR)
        # Divide the window into left and right frames
        self._left_frame = tk.Frame(self, bg=BG_COLOR)
        self._left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._right_frame = tk.Frame(self, bg=BG_COLOR)
        self._right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Set the logging component on bottom, filling the entire bottom area of the left frame
        self._logging_frame = Logging(self._left_frame, bg=BG_COLOR)
        self._logging_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=False)

        # Set the strategy component on top of the left frame
        self._strategy_frame = StrategyEditor(self._left_frame, bg=BG_COLOR)
        self._strategy_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Set the trades component on top of the right frame
        self._trades_frame = TradesWatch(self._right_frame, bg=BG_COLOR)
        self._trades_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self._update_ui_logs()

    def _update_ui_logs(self):
        for log in self.binance.logs:
            if not log["displayed"]:
                self._logging_frame.add_log(log["log"])
                log["displayed"] = True
        self.after(1500, self._update_ui_logs)
