import unittest
from unittest.mock import patch

class Account:
    def __init__(self, username: str, initial_deposit: float):
        self.username = username
        self.balance = initial_deposit
        self.holdings = {}
        self.transactions = []

    def deposit(self, amount: float):
        self.balance += amount
        self.transactions.append(f"Deposited: ${amount:.2f}")

    def withdraw(self, amount: float):
        if self.balance - amount < 0:
            raise ValueError("Insufficient funds for withdrawal.")
        self.balance -= amount
        self.transactions.append(f"Withdrew: ${amount:.2f}")

    def buy_shares(self, symbol: str, quantity: int):
        share_price = get_share_price(symbol)
        total_cost = share_price * quantity
        if total_cost > self.balance:
            raise ValueError("Insufficient funds to buy shares.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        self.balance -= total_cost
        self.transactions.append(f"Bought {quantity} shares of {symbol} at ${share_price:.2f} each.")

    def sell_shares(self, symbol: str, quantity: int):
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            raise ValueError("Not enough shares to sell.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        
        share_price = get_share_price(symbol)
        total_value = share_price * quantity
        
        self.holdings[symbol] -= quantity
        self.balance += total_value
        self.transactions.append(f"Sold {quantity} shares of {symbol} at ${share_price:.2f} each.")

    def portfolio_value(self) -> float:
        total_value = self.balance
        for symbol, quantity in self.holdings.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def profit_loss(self) -> float:
        return self.portfolio_value() - self.balance - sum(get_share_price(sym) * qty for sym, qty in self.holdings.items())

    def report_holdings(self) -> dict:
        return self.holdings

    def report_profit_loss(self) -> float:
        return self.profit_loss()

    def list_transactions(self) -> list:
        return self.transactions

def get_share_price(symbol: str) -> float:
    prices = {
        "AAPL": 150.00,
        "TSLA": 600.00,
        "GOOGL": 2800.00,
    }
    return prices.get(symbol, 0.0)

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account("test_user", 1000.00)
    
    def test_initialization(self):
        self.assertEqual(self.account.username, "test_user")
        self.assertEqual(self.account.balance, 1000.00)
        self.assertEqual(self.account.holdings, {})
        self.assertEqual(self.account.transactions, [])
    
    def test_deposit(self):
        self.account.deposit(500.00)
        self.assertEqual(self.account.balance, 1500.00)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0], "Deposited: $500.00")
    
    def test_withdraw_sufficient_funds(self):
        self.account.withdraw(500.00)
        self.assertEqual(self.account.balance, 500.00)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0], "Withdrew: $500.00")
    
    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(1500.00)
    
    @patch('__main__.get_share_price', return_value=150.00)
    def test_buy_shares_success(self, mock_get_share_price):
        self.account.buy_shares("AAPL", 2)
        self.assertEqual(self.account.balance, 1000.00 - (150.00 * 2))
        self.assertEqual(self.account.holdings, {"AAPL": 2})
        self.assertEqual(len(self.account.transactions), 1)
    
    @patch('__main__.get_share_price', return_value=150.00)
    def test_buy_shares_insufficient_funds(self, mock_get_share_price):
        with self.assertRaises(ValueError):
            self.account.buy_shares("AAPL", 10)
    
    @patch('__main__.get_share_price', return_value=150.00)
    def test_buy_shares_invalid_quantity(self, mock_get_share_price):
        with self.assertRaises(ValueError):
            self.account.buy_shares("AAPL", 0)
    
    @patch('__main__.get_share_price', return_value=150.00)
    def test_sell_shares_success(self, mock_get_share_price):
        self.account.buy_shares("AAPL", 4)
        self.account.sell_shares("AAPL", 2)
        self.assertEqual(self.account.balance, 1000.00 - (150.00 * 4) + (150.00 * 2))
        self.assertEqual(self.account.holdings, {"AAPL": 2})
        self.assertEqual(len(self.account.transactions), 2)
    
    @patch('__main__.get_share_price', return_value=150.00)
    def test_sell_shares_insufficient_shares(self, mock_get_share_price):
        self.account.buy_shares("AAPL", 2)
        with self.assertRaises(ValueError):
            self.account.sell_shares("AAPL", 3)
    
    @patch('__main__.get_share_price', return_value=150.00)
    def test_sell_shares_invalid_quantity(self, mock_get_share_price):
        self.account.buy_shares("AAPL", 2)
        with self.assertRaises(ValueError):
            self.account.sell_shares("AAPL", 0)
    
    @patch('__main__.get_share_price', return_value=150.00)
    def test_portfolio_value(self, mock_get_share_price):
        self.account.buy_shares("AAPL", 2)
        expected_value = 1000.00 - (150.00 * 2) + (150.00 * 2)
        self.assertEqual(self.account.portfolio_value(), expected_value)
    
    @patch('__main__.get_share_price', return_value=150.00)
    def test_profit_loss(self, mock_get_share_price):
        self.account.buy_shares("AAPL", 2)
        self.assertEqual(self.account.profit_loss(), 0.0)
    
    def test_report_holdings(self):
        with patch('__main__.get_share_price', return_value=150.00):
            self.account.buy_shares("AAPL", 2)
            self.assertEqual(self.account.report_holdings(), {"AAPL": 2})
    
    def test_report_profit_loss(self):
        with patch('__main__.get_share_price', return_value=150.00):
            self.account.buy_shares("AAPL", 2)
            self.assertEqual(self.account.report_profit_loss(), 0.0)
    
    def test_list_transactions(self):
        self.account.deposit(500.00)
        self.account.withdraw(200.00)
        self.assertEqual(len(self.account.list_transactions()), 2)
        self.assertEqual(self.account.list_transactions()[0], "Deposited: $500.00")
        self.assertEqual(self.account.list_transactions()[1], "Withdrew: $200.00")

class TestGetSharePrice(unittest.TestCase):
    def test_get_share_price_known(self):
        self.assertEqual(get_share_price("AAPL"), 150.00)
        self.assertEqual(get_share_price("TSLA"), 600.00)
        self.assertEqual(get_share_price("GOOGL"), 2800.00)
    
    def test_get_share_price_unknown(self):
        self.assertEqual(get_share_price("UNKNOWN"), 0.0)

if __name__ == '__main__':
    unittest.main()