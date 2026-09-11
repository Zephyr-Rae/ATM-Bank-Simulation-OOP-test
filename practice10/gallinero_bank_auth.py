from gallinero_bank_account import (
    SavingsAccount,
    StudentAccount
)

import gallinero_bank_storage


def validate_pin(pin):

    if not pin.isdigit():
        return False

    if len(pin) != 4:
        return False

    return True


def register_account(
    name,
    username,
    account_number,
    pin,
    confirm_pin,
    account_type,
    starting_balance
):

    name = name.strip()
    username = username.strip()
    account_number = account_number.strip()
    pin = pin.strip()
    confirm_pin = confirm_pin.strip()

    if name == "":
        return None, "Please enter your name."

    if username == "":
        return None, "Please enter a username."

    if account_number == "":
        return None, "Please enter an account number."

    if gallinero_bank_storage.account_exists(
        account_number
    ):

        return None, "Account number already exists."

    if gallinero_bank_storage.username_exists(
        username
    ):

        return None, "Username is already taken."

    if not validate_pin(pin):

        return None, (
            "PIN must contain exactly "
            "4 digits."
        )

    if pin != confirm_pin:

        return None, (
            "PIN confirmation does not match."
        )

    if starting_balance < 0:

        return None, (
            "Starting balance cannot be negative."
        )

    if account_type == "Savings Account":

        account = SavingsAccount(
            account_number,
            username,
            name,
            pin,
            starting_balance
        )

    else:

        account = StudentAccount(
            account_number,
            username,
            name,
            pin,
            starting_balance
        )

    gallinero_bank_storage.save_account(
        account
    )

    return account, "Registration successful."


def login_account(
    username,
    pin
):

    username = username.strip()
    pin = pin.strip()

    account = (
        gallinero_bank_storage.find_account_by_username(
            username
        )
    )

    if account is None:

        return None, (
            "Invalid username or PIN."
        )

    if not account.verify_pin(pin):

        return None, (
            "Invalid username or PIN."
        )

    return account, "Login successful."


def change_username(account, new_username):

    new_username = new_username.strip()

    if new_username == "":
        return False, "Username cannot be empty."

    if new_username == account.username:
        return False, "That is already your current username."

    if gallinero_bank_storage.username_exists(new_username):
        return False, "That username is already taken."

    account.change_username(new_username)

    gallinero_bank_storage.update_account(account)

    return True, "Username updated successfully."


def change_pin(account, current_pin, new_pin, confirm_new_pin):

    current_pin = current_pin.strip()
    new_pin = new_pin.strip()
    confirm_new_pin = confirm_new_pin.strip()

    if not validate_pin(new_pin):
        return False, "New PIN must contain exactly 4 digits."

    if new_pin != confirm_new_pin:
        return False, "PIN confirmation does not match."

    success = account.change_pin(current_pin, new_pin)

    if not success:
        return False, "Current PIN is incorrect."

    gallinero_bank_storage.update_account(account)

    return True, "PIN updated successfully."