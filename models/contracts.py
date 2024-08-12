class Contracts:

    def __init__(self, data) -> None:
        self.symbol = data["symbol"]
        self.baseAsset = data["baseAsset"]
        self.quoteAsset = data["quoteAsset"]
        self.status = data["status"]
