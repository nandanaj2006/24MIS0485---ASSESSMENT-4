import datetime

class DigitalWallet:
    def __init__(self, account_id, pin, daily_limit=50000.0):
        self.account_id = account_id
        self.pin = pin
        self.balance = 0.0
        self.daily_limit = daily_limit
        self.history = []
        self.failed_pin_attempts = 0
        self.is_locked = False
        self.daily_transferred = {}

    def authenticate(self, pin):
        if self.is_locked:
            return False, "Account is locked due to security reasons."
        if self.pin != pin:
            self.failed_pin_attempts += 1
            if self.failed_pin_attempts >= 3:
                self.is_locked = True
                return False, "Account locked: Multiple failed PIN attempts."
            return False, "Invalid PIN."
        self.failed_pin_attempts = 0
        return True, "Authenticated."

    def deposit(self, amount):
        if amount <= 0:
            return False, "Deposit amount must be positive."
        self.balance += amount
        self.history.append({"type": "DEPOSIT", "amount": amount, "timestamp": datetime.datetime.now(), "status": "SUCCESS"})
        return True, f"Deposited {amount}. Current Balance: {self.balance}"

    def withdraw(self, amount, pin):
        auth, msg = self.authenticate(pin)
        if not auth:
            return False, msg
        if amount <= 0:
            return False, "Withdrawal amount must be positive."
        if amount > self.balance:
            return False, "Insufficient balance."
        
        today = datetime.date.today().isoformat()
        if self.daily_transferred.get(today, 0.0) + amount > self.daily_limit:
            return False, "Daily transaction limit exceeded."

        # Fraud checks
        now = datetime.datetime.now()
        ten_mins_ago = now - datetime.timedelta(minutes=10)
        recent_txs = [t for t in self.history if t["timestamp"] >= ten_mins_ago]
        if len(recent_txs) >= 5:
            return False, "FRAUD SUSPECTED: More than 5 transactions in 10 minutes."
        if amount > 100000:
            return False, "FRAUD SUSPECTED: Large transaction threshold triggered."

        self.balance -= amount
        self.daily_transferred[today] = self.daily_transferred.get(today, 0.0) + amount
        self.history.append({"type": "WITHDRAWAL", "amount": amount, "timestamp": now, "status": "SUCCESS"})
        return True, f"Withdrew {amount}. Current Balance: {self.balance}"

    def transfer(self, target_wallet, amount, pin):
        auth, msg = self.authenticate(pin)
        if not auth:
            return False, msg
        if amount <= 0:
            return False, "Transfer amount must be positive."
        if amount > self.balance:
            return False, "Insufficient balance."

        today = datetime.date.today().isoformat()
        if self.daily_transferred.get(today, 0.0) + amount > self.daily_limit:
            return False, "Daily transaction limit exceeded."

        self.balance -= amount
        target_wallet.balance += amount
        self.daily_transferred[today] = self.daily_transferred.get(today, 0.0) + amount
        
        now = datetime.datetime.now()
        self.history.append({"type": "TRANSFER_OUT", "target": target_wallet.account_id, "amount": amount, "timestamp": now, "status": "SUCCESS"})
        target_wallet.history.append({"type": "TRANSFER_IN", "from": self.account_id, "amount": amount, "timestamp": now, "status": "SUCCESS"})
        return True, f"Transferred {amount} to {target_wallet.account_id}."
