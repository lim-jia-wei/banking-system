# standard improt
from unittest.mock import patch

# third party import
import pytest

# local import
from bank import Account, Bank, BankApp

# Disable pylint errors for mock_input which are used to mock user input
# pylint: disable=unused-argument


@pytest.fixture(name="bank")
def bank_fixture():
    return Bank()


@pytest.fixture(name="account")
def account_fixture():
    return Account("Test Account", 100.0)


@pytest.fixture(name="bank_app")
def bank_app_fixture(bank):
    return BankApp(bank)


def test_create_account(bank, capsys):
    bank.create_account("Alice", 50.0)
    account = bank.get_account("Alice")
    captured = capsys.readouterr()
    assert account.account_name == "Alice"
    assert account.balance == 50.0
    assert "Account created for Alice with starting balance of $50.00." in captured.out


def test_create_account_already_exist(bank, capsys):
    bank.create_account("Alice", 50.0)
    with pytest.raises(ValueError, match="Account already exists."):
        bank.create_account("Alice", 100.0)  # create an account with the same name


def test_deposit(account, capsys):
    account.deposit(50.0)
    captured = capsys.readouterr()
    assert account.balance == 150.0
    assert "Deposited $50.00 to Test Account's account." in captured.out


@pytest.mark.parametrize(
    "amount",
    [
        (0),  # zero
        (-10),  # negative amount
    ]
)
def test_deposit_invalid_amount(account, amount):
    initial_balance = account.balance
    with pytest.raises(ValueError, match="Deposit amount must be positive."):
        account.deposit(amount)
    assert account.balance == initial_balance


def test_withdraw(account, capsys):
    account.withdraw(50.0)
    captured = capsys.readouterr()
    assert account.balance == 50.0
    assert "Withdrew $50.00 from Test Account's account." in captured.out


@pytest.mark.parametrize(
    "amount",
    [
        (150.0),  # more than balance
        (-10),  # negative amount
        (0),  # zero
    ]
)
def test_withdraw_invalid_amount(account, amount):
    initial_balance = account.balance
    with pytest.raises(ValueError, match="Insufficient funds or invalid amount."):
        account.withdraw(amount)
    assert account.balance == initial_balance


def test_transfer(bank, capsys):
    bank.create_account("Alice", 100.0)
    bank.create_account("Bob", 50.0)
    alice_account = bank.get_account("Alice")
    bob_account = bank.get_account("Bob")
    alice_account.transfer(50.0, bob_account)
    captured = capsys.readouterr()
    assert alice_account.balance == 50.0
    assert bob_account.balance == 100.0
    assert "Transferred $50.00 from Alice's account to Bob's account." in captured.out


@pytest.mark.parametrize(
    "amount",
    [
        (150.0),  # more than balance
        (-10),  # negative amount
        (0),  # zero
    ]
)
def test_transfer_invalid_amount(bank, amount):
    bank.create_account("Alice", 100.0)
    bank.create_account("Bob", 50.0)
    alice_account = bank.get_account("Alice")
    bob_account = bank.get_account("Bob")
    with pytest.raises(ValueError, match="Insufficient funds or invalid amount."):
        alice_account.transfer(amount, bob_account)
    assert alice_account.balance == 100.0
    assert bob_account.balance == 50.0


def test_transfer_to_same_account(bank):
    bank.create_account("Alice", 100.0)
    alice_account = bank.get_account("Alice")
    with pytest.raises(ValueError, match="Unable to transfer funds to the same account."):
        alice_account.transfer(50.0, alice_account)
    assert alice_account.balance == 100.0


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


def test_load_nonexistent_file(bank):
    with pytest.raises(FileNotFoundError, match="File non_existent_file.csv not found."):
        bank.load_from_csv("non_existent_file.csv")


def test_bank_app_print_menu(bank_app, capsys):
    bank_app.print_menu()
    captured = capsys.readouterr()
    assert "Menu:" in captured.out
    assert "1. Create Account" in captured.out
    assert "7. Exit" in captured.out


@patch("builtins.input", side_effect=["1", "Alice", "100", "7"])
def test_bank_app_create_account(mock_input, bank_app, bank, capsys):
    bank_app.run()
    captured = capsys.readouterr()
    assert "Account created for Alice with starting balance of $100.00." in captured.out
    assert bank.get_account("Alice").balance == 100.0


@patch("builtins.input", side_effect=["1", "Alice", "100", "2", "Alice", "50", "7"])
def test_bank_app_deposit(mock_input, bank_app, bank, capsys):
    bank_app.run()
    captured = capsys.readouterr()
    assert "Deposited $50.00 to Alice's account." in captured.out
    assert bank.get_account("Alice").balance == 150.0


@patch("builtins.input", side_effect=["1", "Alice", "100", "3", "Alice", "50", "7"])
def test_bank_app_withdraw(mock_input, bank_app, bank, capsys):
    bank_app.run()
    captured = capsys.readouterr()
    assert "Withdrew $50.00 from Alice's account." in captured.out
    assert bank.get_account("Alice").balance == 50.0


@patch("builtins.input", side_effect=["1", "Alice", "100", "1", "Bob",
                                      "50", "4", "Alice", "Bob", "50", "7"])
def test_bank_app_transfer(mock_input, bank_app, bank, capsys):
    bank_app.run()
    captured = capsys.readouterr()
    assert "Transferred $50.00 from Alice's account to Bob's account." in captured.out
    assert bank.get_account("Alice").balance == 50.0
    assert bank.get_account("Bob").balance == 100.0


@patch("builtins.input", side_effect=["1", "Alice", "100", "5", "7"])
def test_bank_app_save_state(mock_input, bank_app, capsys):
    bank_app.run()
    captured = capsys.readouterr()
    assert "Bank state saved to" in captured.out


@patch("builtins.input", side_effect=["1", "Alice", "100", "5", "6", "7"])
def test_bank_app_load_state(mock_input, bank_app, capsys):
    bank_app.run()
    captured = capsys.readouterr()
    assert "Bank state loaded from" in captured.out


def test_bank_app_exit(bank_app, capsys):
    with patch("builtins.input", side_effect=["7"]):
        bank_app.run()
    captured = capsys.readouterr()
    assert "Exiting the bank system." in captured.out


def test_bank_app_invalid_choice(bank_app, capsys):
    with patch("builtins.input", side_effect=["8", "7"]):
        bank_app.run()
    captured = capsys.readouterr()
    assert "Invalid choice. Please try again." in captured.out


def test_bank_app_get_account_not_found(bank_app, capsys):
    with patch("builtins.input", side_effect=["2", "Charlie", "50", "7"]):
        bank_app.run()
    captured = capsys.readouterr()
    assert "Invalid choice. Please try again." in captured.out


def test_bank_app_get_amount_invalid(bank_app, capsys):
    with patch("builtins.input", side_effect=["2", "Alice", "b", "7"]):
        bank_app.run()
    captured = capsys.readouterr()
    assert "Invalid choice. Please try again." in captured.out
