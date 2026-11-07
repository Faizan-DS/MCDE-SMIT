# Task 06 | Banking Ledger with OOP
from collections import namedtuple
from itertools import count

Transaction = namedtuple("Transaction", ["transaction_id", "action", "amount", "balance_after"])

_next_id = count(1)   


def check_amount(amount):
    if isinstance(amount, bool) or not isinstance(amount, (int, float)) or amount <= 0:
        raise ValueError("Amount must be a number greater than zero")


class Account:
    def __init__(self, account_id, opening_balance=0):
        if isinstance(opening_balance, bool) or not isinstance(opening_balance, (int, float)) or opening_balance < 0:
            raise ValueError("Opening balance cannot be negative")
        self._account_id = account_id
        self._balance = opening_balance
        self._transactions = []

    @property
    def account_id(self):
        return self._account_id

    @property
    def balance(self):           
        return self._balance

    def _record(self, action, amount):
        self._transactions.append(
            Transaction(next(_next_id), action, amount, self._balance))

    def deposit(self, amount, action="deposit"):
        check_amount(amount)
        self._balance += amount
        self._record(action, amount)

    def withdraw(self, amount, action="withdrawal"):
        check_amount(amount)
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        self._record(action, amount)

    def statement(self):
        return tuple(self._transactions)      


class Bank:
    def __init__(self):
        self._accounts = {}

    def add_account(self, account_id, opening_balance=0):
        if account_id in self._accounts:
            raise ValueError("Account already exists: " + str(account_id))
        self._accounts[account_id] = Account(account_id, opening_balance)

    def get_account(self, account_id):
        if account_id not in self._accounts:
            raise ValueError("Account not found: " + str(account_id))
        return self._accounts[account_id]

    def deposit(self, account_id, amount):
        self.get_account(account_id).deposit(amount)

    def withdraw(self, account_id, amount):
        self.get_account(account_id).withdraw(amount)

    def transfer(self, from_id, to_id, amount):
        sender = self.get_account(from_id)        
        receiver = self.get_account(to_id)
        check_amount(amount)
        if from_id == to_id:
            raise ValueError("Cannot transfer to the same account")
        if amount > sender.balance:
            raise ValueError("Insufficient funds")
 
        sender.withdraw(amount, "transfer out to " + str(to_id))
        receiver.deposit(amount, "transfer in from " + str(from_id))

    def statement(self, account_id):
        return self.get_account(account_id).statement()


if __name__ == "__main__":
    bank = Bank()
    bank.add_account("A", 1000)
    bank.add_account("B", 200)
    bank.transfer("A", "B", 350)
    print(bank.get_account("A").balance, bank.get_account("B").balance)   # 650 550

    for bad in [("A", "B", 5000), ("A", "Z", 10), ("A", "B", -5)]:
        try:
            bank.transfer(*bad)
        except ValueError as error:
            print("Rejected:", error)
    print(bank.get_account("A").balance, bank.get_account("B").balance)   # still 650 550

    for t in bank.statement("A"):
        print(t)