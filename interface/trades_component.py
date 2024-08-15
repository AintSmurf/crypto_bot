import tkinter as tk
from interface.styling import *
import typing


class TradesWatch(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.headers = [
            "time",
            "symbol",
            "exchange",
            "startegy",
            "side",
            "quantity",
            "status",
            "pnl",
        ]

        self._table_frame = tk.Frame(self, bg=BG_COLOR)
        self._table_frame.pack(side=tk.TOP)
        self.body_widgets = dict()

        for idx, h in enumerate(self.headers):
            header = tk.Label(
                self._table_frame,
                text=h.capitalize(),
                bg=BG_COLOR,
                fg=FG_COLOR_STEEL_BLUE,
                font=GLOBAL_FONT,
            )
            header.grid(row=0, column=idx)
        for h in self.headers:
            self.body_widgets[h] = dict()
            if h in ["status", "pnl"]:
                self.body_widgets[h + "_var"] = dict()
        self.body_index = 1

    def add_trade(self, data: typing.Dict):
        b_index = self.body_index
        # time
        t_index = data["time"]
        self.body_widgets["time"][t_index] = tk.Label(
            self._table_frame,
            text=data["time"],
            bg=BG_COLOR,
            fg=FG_COLOR_WHITE,
            font=GLOBAL_FONT,
        )
        self.body_widgets["time"][t_index].grid(row=b_index, column=0)

        # symbol
        self.body_widgets["symbol"][t_index] = tk.Label(
            self._table_frame,
            text=data["symbol"],
            bg=BG_COLOR,
            fg=FG_COLOR_WHITE,
            font=GLOBAL_FONT,
        )
        self.body_widgets["symbol"][t_index].grid(row=b_index, column=1)

        # exchange
        self.body_widgets["exchange"][t_index] = tk.Label(
            self._table_frame,
            text=data["exchange"],
            bg=BG_COLOR,
            fg=FG_COLOR_WHITE,
            font=GLOBAL_FONT,
        )
        self.body_widgets["exchange"][t_index].grid(row=b_index, column=2)

        # strategy
        self.body_widgets["startegy"][t_index] = tk.Label(
            self._table_frame,
            text=data["startegy"],
            bg=BG_COLOR,
            fg=FG_COLOR_WHITE,
            font=GLOBAL_FONT,
        )
        self.body_widgets["startegy"][t_index].grid(row=b_index, column=3)

        # side
        self.body_widgets["side"][t_index] = tk.Label(
            self._table_frame,
            text=data["side"],
            bg=BG_COLOR,
            fg=FG_COLOR_WHITE,
            font=GLOBAL_FONT,
        )
        self.body_widgets["side"][t_index].grid(row=b_index, column=4)

        # quantity
        self.body_widgets["quantity"][t_index] = tk.Label(
            self._table_frame,
            text=data["quantity"],
            bg=BG_COLOR,
            fg=FG_COLOR_WHITE,
            font=GLOBAL_FONT,
        )
        self.body_widgets["quantity"][t_index].grid(row=b_index, column=5)

        # status
        self.body_widgets["status_var"][t_index] = tk.StringVar()
        self.body_widgets["status"][t_index] = tk.Label(
            self._table_frame,
            textvariable=self.body_widgets["status_var"][t_index],
            bg=BG_COLOR,
            fg=FG_COLOR_WHITE,
            font=GLOBAL_FONT,
        )
        self.body_widgets["status"][t_index].grid(row=b_index, column=6)

        # pnl
        self.body_widgets["pnl_var"][t_index] = tk.StringVar()
        self.body_widgets["pnl"][t_index] = tk.Label(
            self._table_frame,
            textvariable=self.body_widgets["pnl_var"][t_index],
            bg=BG_COLOR,
            fg=FG_COLOR_WHITE,
            font=GLOBAL_FONT,
        )
        self.body_widgets["pnl"][t_index].grid(row=b_index, column=7)
        self.body_index += 1
