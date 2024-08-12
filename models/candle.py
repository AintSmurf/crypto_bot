from helpers.binance_futures_helper import timestamp_to_date


class Candle:

    def __init__(self, data) -> None:
        self.open_time = timestamp_to_date(data[0])
        self.open = float(data[1])
        self.high = float(data[2])
        self.low = float(data[3])
        self.close = float(data[4])
        self.volume = float(data[5])
        self.close_time = timestamp_to_date(data[6])
        self.quote_volume = float(data[7])
        self.count = float(data[8])
