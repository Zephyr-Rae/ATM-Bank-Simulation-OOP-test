class Account:

    def __init__(self, account_number, username, account_name, pin, starting_balance):
        self.account_number = account_number
        self.username = username
        self.account_name = account_name
        self._pin = pin
        self._balance = starting_balance

    def check_balance(self):
        return self._balance

    def get_pin(self):
        return self._pin

    def verify_pin(self, pin):
        return self._pin == pin

    def change_username(self, new_username):
        self.username = new_username
        return True

    def change_pin(self, current_pin, new_pin):
        if self._pin != current_pin:
            return False
        self._pin = new_pin
        return True

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return True
        else:
            return False

    def withdraw(self, amount):
        if amount > 0 and amount <= self._balance:
            self._balance -= amount
            return True
        else:
            return False

    def get_account_type(self):
        return "Account"


class SavingsAccount(Account):
    def get_account_type(self):
        return "Savings Account"


class StudentAccount(Account):
    def get_account_type(self):
        return "Student Account"
