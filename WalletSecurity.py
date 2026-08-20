import unittest
import datetime
from concurrent.futures import ThreadPoolExecutor
from DigitalWallet import DigitalWallet

class TestWalletSecurity(unittest.TestCase):
    def setUp(self):
        self.w1 = DigitalWallet("ACC101", "1234", daily_limit=5000)
        self.w2 = DigitalWallet("ACC102", "5678")
        self.w1.deposit(10000)

    def test_normal_transaction(self):
        success, _ = self.w1.withdraw(1000, "1234")
        self.assertTrue(success)
        self.assertEqual(self.w1.balance, 9000)

    def test_insufficient_balance(self):
        success, msg = self.w2.withdraw(500, "5678")
        self.assertFalse(success)
        self.assertEqual(msg, "Insufficient balance.")

    def test_daily_limit(self):
        self.w1.withdraw(4000, "1234")
        success, msg = self.w1.withdraw(2000, "1234")
        self.assertFalse(success)
        self.assertEqual(msg, "Daily transaction limit exceeded.")

    def test_multiple_failed_pins(self):
        self.w1.authenticate("0000")
        self.w1.authenticate("0000")
        success, msg = self.w1.authenticate("0000")
        self.assertFalse(success)
        self.assertTrue(self.w1.is_locked)

    def test_suspicious_frequency(self):
        for _ in range(5):
            self.w1.history.append({"type": "W", "amount": 10, "timestamp": datetime.datetime.now(), "status": "SUCCESS"})
        success, msg = self.w1.withdraw(100, "1234")
        self.assertFalse(success)
        self.assertIn("FRAUD SUSPECTED", msg)

    def test_negative_amount(self):
        success, msg = self.w1.deposit(-500)
        self.assertFalse(success)

    def test_concurrent_transactions(self):
        def attempt_withdraw(amt):
            return self.w1.withdraw(amt, "1234")
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(attempt_withdraw, [1000]*5))
        self.assertEqual(len(results), 5)

if __name__ == "__main__":
    unittest.main()
