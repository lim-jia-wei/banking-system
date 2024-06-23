import pytest
from bank import Account, Bank


@pytest.fixture(name="bank")
def bank_fixture():
    return Bank()


@pytest.fixture(name="account")
def account_fixture():
    return Account("Test Account", 100.0)


def test_create_account(bank, capsys):
    bank.create_account("Alice", 50.0)
    account = bank.get_account("Alice")
    captured = capsys.readouterr()
    assert account.account_name == "Alice"
    assert account.balance == 50.0
    assert "Account created for Alice." in captured.out


def test_create_account_already_exist(bank, capsys):
    bank.create_account("Alice", 50.0)
    bank.create_account("Alice", 100.0)  # create an account with the same name
    captured = capsys.readouterr()
    assert "Account already exists." in captured.out


def test_deposit(account, capsys):
    account.deposit(50.0)
    captured = capsys.readouterr()
    assert account.balance == 150.0
    assert "Deposited $50.0 to Test Account's account." in captured.out


def test_deposit_invalid_amount(account, capsys):
    initial_balance = account.balance
    account.deposit(-10.0)
    captured = capsys.readouterr()
    assert account.balance == initial_balance
    assert "Deposit amount must be positive." in captured.out


def test_withdraw(account, capsys):
    account.withdraw(50.0)
    captured = capsys.readouterr()
    assert account.balance == 50.0
    assert "Withdrew $50.0 from Test Account's account." in captured.out


@pytest.mark.parametrize(
    "amount",
    [
        (150.0),  # more than balance
        (-10),  # negative amount
    ]
)
def test_withdraw_invalid_amount(account, amount, capsys):
    initial_balance = account.balance
    account.withdraw(amount)  # more than balance
    captured = capsys.readouterr()
    assert account.balance == initial_balance
    assert "Insufficient funds or invalid amount." in captured.out


def test_transfer(bank, capsys):
    bank.create_account("Alice", 100.0)
    bank.create_account("Bob", 50.0)
    alice_account = bank.get_account("Alice")
    bob_account = bank.get_account("Bob")
    alice_account.transfer(50.0, bob_account)
    captured = capsys.readouterr()
    assert alice_account.balance == 50.0
    assert bob_account.balance == 100.0
    assert "Transferred $50.0 from Alice's account to Bob's account." in captured.out


@pytest.mark.parametrize(
    "amount",
    [
        (150.0),  # more than balance
        (-10),  # negative amount
    ]
)
def test_transfer_invalid_amount(bank, amount, capsys):
    bank.create_account("Alice", 100.0)
    bank.create_account("Bob", 50.0)
    alice_account = bank.get_account("Alice")
    bob_account = bank.get_account("Bob")
    alice_account.transfer(amount, bob_account)  # more than balance
    captured = capsys.readouterr()
    assert alice_account.balance == 100.0
    assert bob_account.balance == 50.0
    assert "Insufficient funds or invalid amount." in captured.out


def test_save_load_csv(bank, tmp_path, capsys):
    bank.create_account("Alice", 100.0)
    file_path = tmp_path / "bank_state.csv"

    bank.save_to_csv(file_path)
    captured = capsys.readouterr()
    assert "Bank state saved to" in captured.out

    bank.accounts = {}  # clear the bank state

    bank.load_from_csv(file_path)
    captured = capsys.readouterr()
    alice_account = bank.get_account("Alice")
    assert alice_account.balance == 100.0
    assert "Bank state loaded from" in captured.out
