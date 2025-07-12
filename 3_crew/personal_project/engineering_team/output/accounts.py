class Account:
    def __init__(self, account_id: str, initial_deposit: float):
        if initial_deposit < 0:
            raise ValueError("Initial deposit cannot be negative.")
        self.account_id = account_id
        self.balance = initial_deposit
        self.initial_deposit = initial_deposit
        self.transactions = [(self._current_time(), 'DEPOSIT', 'Initial deposit', initial_deposit)]
        self.holdings = {}

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.transactions.append((self._current_time(), 'DEPOSIT', '', amount))

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        self.transactions.append((self._current_time(), 'WITHDRAW', '', amount))

    def buy_shares(self, symbol: str, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        price = self.get_share_price(symbol)
        total_cost = price * quantity
        if total_cost > self.balance:
            raise ValueError("Insufficient funds to buy shares.")
        self.balance -= total_cost
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity
        self.transactions.append((self._current_time(), 'BUY', f"{quantity} {symbol}", total_cost))

    def sell_shares(self, symbol: str, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            raise ValueError("Insufficient shares to sell.")
        price = self.get_share_price(symbol)
        total_proceeds = price * quantity
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        self.balance += total_proceeds
        self.transactions.append((self._current_time(), 'SELL', f"{quantity} {symbol}", total_proceeds))

    def get_portfolio_value(self) -> float:
        holdings_value = sum(self.get_share_price(symbol) * qty for symbol, qty in self.holdings.items())
        return self.balance + holdings_value

    def get_profit_or_loss(self) -> float:
        return self.get_portfolio_value() - self.initial_deposit

    def get_holdings(self) -> dict:
        return dict(self.holdings)

    def get_transaction_history(self) -> list:
        return list(self.transactions)

    @staticmethod
    def get_share_price(symbol: str) -> float:
        prices = {
            'AAPL': 150.0,
            'TSLA': 600.0,
            'GOOGL': 2800.0,
        }
        return prices.get(symbol.upper(), 0.0)

    @staticmethod
    def _current_time():
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')