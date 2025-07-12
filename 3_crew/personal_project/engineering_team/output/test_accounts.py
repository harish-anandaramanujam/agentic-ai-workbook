import unittest
from datetime import datetime
from accounts import Account

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account('12345', 1000.0)
    
    def test_initialization(self):
        self.assertEqual(self.account.account_id, '12345')
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(self.account.initial_deposit, 1000.0)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0][1], 'DEPOSIT')
        self.assertEqual(self.account.transactions[0][3], 1000.0)
        
    def test_negative_initial_deposit(self):
        with self.assertRaises(ValueError):
            Account('12345', -100)
    
    def test_deposit(self):
        self.account.deposit(500)
        self.assertEqual(self.account.balance, 1500.0)
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[-1][1], 'DEPOSIT')
        
    def test_invalid_deposit(self):
        with self.assertRaises(ValueError):
            self.account.deposit(0)
        with self.assertRaises(ValueError):
            self.account.deposit(-100)
    
    def test_withdraw(self):
        self.account.withdraw(500)
        self.assertEqual(self.account.balance, 500.0)
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[-1][1], 'WITHDRAW')
    
    def test_invalid_withdraw(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(0)
        with self.assertRaises(ValueError):
            self.account.withdraw(-100)
        with self.assertRaises(ValueError):
            self.account.withdraw(2000)
    
    def test_buy_shares(self):
        self.account.buy_shares('AAPL', 2)
        self.assertEqual(self.account.balance, 1000.0 - (150.0 * 2))
        self.assertEqual(self.account.holdings['AAPL'], 2)
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[-1][1], 'BUY')
    
    def test_invalid_buy_shares(self):
        with self.assertRaises(ValueError):
            self.account.buy_shares('AAPL', 0)
        with self.assertRaises(ValueError):
            self.account.buy_shares('AAPL', -1)
        with self.assertRaises(ValueError):
            self.account.buy_shares('AAPL', 10000)
    
    def test_sell_shares(self):
        self.account.buy_shares('AAPL', 2)
        initial_balance = self.account.balance
        self.account.sell_shares('AAPL', 1)
        self.assertEqual(self.account.balance, initial_balance + 150.0)
        self.assertEqual(self.account.holdings['AAPL'], 1)
        self.assertEqual(len(self.account.transactions), 3)
        self.assertEqual(self.account.transactions[-1][1], 'SELL')
    
    def test_sell_all_shares(self):
        self.account.buy_shares('AAPL', 2)
        self.account.sell_shares('AAPL', 2)
        self.assertNotIn('AAPL', self.account.holdings)
    
    def test_invalid_sell_shares(self):
        with self.assertRaises(ValueError):
            self.account.sell_shares('AAPL', 0)
        with self.assertRaises(ValueError):
            self.account.sell_shares('AAPL', -1)
        with self.assertRaises(ValueError):
            self.account.sell_shares('AAPL', 1)
    
    def test_get_portfolio_value(self):
        self.account.buy_shares('AAPL', 2)
        expected_value = self.account.balance + (150.0 * 2)
        self.assertEqual(self.account.get_portfolio_value(), expected_value)
    
    def test_get_profit_or_loss(self):
        self.account.buy_shares('AAPL', 2)
        expected_pnl = (self.account.balance + (150.0 * 2)) - 1000.0
        self.assertEqual(self.account.get_profit_or_loss(), expected_pnl)
    
    def test_get_holdings(self):
        self.account.buy_shares('AAPL', 2)
        holdings = self.account.get_holdings()
        self.assertEqual(holdings['AAPL'], 2)
        self.assertIsInstance(holdings, dict)
    
    def test_get_transaction_history(self):
        history = self.account.get_transaction_history()
        self.assertEqual(len(history), 1)
        self.assertIsInstance(history, list)
    
    def test_get_share_price(self):
        self.assertEqual(Account.get_share_price('AAPL'), 150.0)
        self.assertEqual(Account.get_share_price('TSLA'), 600.0)
        self.assertEqual(Account.get_share_price('UNKNOWN'), 0.0)

if __name__ == '__main__':
    unittest.main()