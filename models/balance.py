class Balance:
    def __init__(self, data) -> None:
        self.asset = data["asset"]
        self.wallet_balance = float(data["walletBalance"])
        self.unrealizedProfit = float(data["unrealizedProfit"])
        self.marginBalance = float(data["marginBalance"])
        self.maintMargin = float(data["maintMargin"])
        self.initialMargin = float(data["initialMargin"])
