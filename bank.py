# standard import
import csv
from typing import Dict, Optional


class Account:
    """
    A class to represent a bank account.

    Attributes
    ----------
    account_name : str
        Name of the account holder.
    balance : float
        Current balance of the account.

    Methods
    -------
    deposit(deposit_amount: float) -> None
        Deposits a specified amount to the account.
    withdraw(withdrawal_amount: float) -> None
        Withdraws a specified amount from the account.
    transfer(transfer_amount: float, target_account: 'Account') -> None
        Transfers a specified amount to another account.
    """

    def __init__(self, account_name: str, balance: float = 0.0) -> None:
        """
        Constructs all the necessary attributes for the account object.

        Parameters
        ----------
        account_name : str
            Name of the account holder.
        balance : float, optional
            Initial balance of the account (default is 0.0).
        """
        self.account_name: str = account_name
        self.balance: float = balance

    def deposit(self, deposit_amount: float) -> None:
        """
        Deposits a specified amount to the account.

        Parameters
        ----------
        deposit_amount : float
            Amount to be deposited.

        Raises
        ------
        ValueError
            If the deposit amount is not positive.
        """
        if deposit_amount > 0:
            self.balance += deposit_amount
            print(f"Deposited ${deposit_amount:.2f} to {self.account_name}'s account.")
        else:
            raise ValueError("Deposit amount must be positive.")

    def withdraw(self, withdrawal_amount: float) -> None:
        """
        Withdraws a specified amount from the account.

        Parameters
        ----------
        withdrawal_amount : float
            Amount to be withdrawn.

        Raises
        ------
        ValueError
            If the withdrawal amount is greater than the balance or not positive.
        """
        if 0 < withdrawal_amount <= self.balance:
            self.balance -= withdrawal_amount
            print(f"Withdrew ${withdrawal_amount:.2f} from {self.account_name}'s account.")
        else:
            raise ValueError("Insufficient funds or invalid amount.")

    def transfer(self, transfer_amount: float, target_account: 'Account') -> None:
        """
        Transfers a specified amount to another account.

        Parameters
        ----------
        transfer_amount : float
            Amount to be transferred.
        target_account : Account
            The target account to which the amount is to be transferred.

        Raises
        ------
        ValueError
            If the transfer amount is greater than the balance, not positive, or the target account is the same as the current account.
        """
        if 0 < transfer_amount <= self.balance:
            if self.account_name != target_account.account_name:
                self.balance -= transfer_amount
                target_account.deposit(transfer_amount)
                print(f"Transferred ${transfer_amount:.2f} from {
                      self.account_name}'s account to {target_account.account_name}'s account.")
            else:
                raise ValueError("Unable to transfer funds to the same account.")
        else:
            raise ValueError("Insufficient funds or invalid amount.")


class Bank:
    """
    A class to represent a bank containing multiple accounts.

    Attributes
    ----------
    accounts : Dict[str, Account]
        A dictionary mapping account names to Account objects.

    Methods
    -------
    create_account(account_name: str, starting_balance: float = 0.0) -> None
        Creates a new account with a specified starting balance.
    get_account(account_name: str) -> Optional[Account]
        Retrieves an account by name.
    save_to_csv(filename: str) -> None
        Saves the current state of the bank to a CSV file.
    load_from_csv(filename: str) -> None
        Loads the state of the bank from a CSV file.
    """

    def __init__(self) -> None:
        """
        Constructs all the necessary attributes for the bank object.
        """
        self.accounts: Dict[str, Account] = {}

    def create_account(self, account_name: str, starting_balance: float = 0.0) -> None:
        """
        Creates a new account with a specified starting balance.

        Parameters
        ----------
        account_name : str
            Name of the account holder.
        starting_balance : float, optional
            Initial balance of the account (default is 0.0).

        Raises
        ------
        ValueError
            If the account already exists.
        """
        if account_name not in self.accounts:
            self.accounts[account_name] = Account(account_name, starting_balance)
            print(f"Account created for {account_name} with starting balance of ${
                  starting_balance:.2f}.")
        else:
            raise ValueError("Account already exists.")

    def get_account(self, account_name: str) -> Optional[Account]:
        """
        Retrieves an account by name.

        Parameters
        ----------
        account_name : str
            Name of the account holder.

        Returns
        -------
        Optional[Account]
            The account object if found, None otherwise.
        """
        return self.accounts.get(account_name, None)

    def save_to_csv(self, filename: str) -> None:
        """
        Saves the current state of the bank to a CSV file.

        Parameters
        ----------
        filename : str
            The name of the file where the bank state will be saved.
        """
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Name', 'Balance'])
            for bank_account in self.accounts.values():
                writer.writerow([bank_account.account_name, f"{bank_account.balance:.2f}"])
        print(f"Bank state saved to {filename}.")

    def load_from_csv(self, filename: str) -> None:
        """
        Loads the state of the bank from a CSV file.

        Parameters
        ----------
        filename : str
            The name of the file from which the bank state will be loaded.

        Raises
        ------
        FileNotFoundError
            If the file is not found.
        """
        try:
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header
                for row in reader:
                    account_name, balance = row
                    self.accounts[account_name] = Account(account_name, float(balance))
            print(f"Bank state loaded from {filename}.")
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File {filename} not found.") from e


class BankApp:
    """
    A class to represent the bank application.

    Attributes
    ----------
    bank : Bank
        An instance of the Bank class.

    Methods
    -------
    print_menu() -> None
        Prints the menu of available actions.
    get_account() -> Account
        Prompts the user to enter an account name and retrieves the corresponding account.
    get_amount() -> float
        Prompts the user to enter an amount and returns it as a float.
    run() -> None
        Runs the main loop of the bank application.
    """

    def __init__(self, my_bank: Bank) -> None:
        """
        Constructs all the necessary attributes for the bank application.

        Parameters
        ----------
        my_bank : Bank
            An instance of the Bank class.
        """
        self.bank = my_bank

    def print_menu(self) -> None:
        """
        Prints the menu of available actions.
        """
        print("\nMenu:")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Save State")
        print("6. Load State")
        print("7. Exit")

    def get_account(self) -> Account:
        """
        Prompts the user to enter an account name and retrieves the corresponding account.

        Returns
        -------
        Account
            The account object corresponding to the entered account name.

        Raises
        ------
        ValueError
            If the account is not found.
        """
        name = input("Enter account name: ")
        account = self.bank.get_account(name)
        if not account:
            raise ValueError("Account not found.")
        return account

    def get_amount(self) -> float:
        """
        Prompts the user to enter an amount and returns it as a float.

        Returns
        -------
        float
            The amount entered by the user.

        Raises
        ------
        ValueError
            If the entered amount is not a valid number.
        """
        try:
            amount = float(input("Enter amount: "))
            return amount
        except ValueError as e:
            raise ValueError("Amount is invalid. Please input only numeric value.") from e

    def run(self) -> None:
        """
        Runs the main loop of the bank application.
        """
        while True:
            self.print_menu()
            choice = input("Choose an option: ")

            try:
                if choice == "1":
                    name = input("Enter account name: ")
                    amount = self.get_amount()
                    self.bank.create_account(name, amount)
                elif choice == "2":
                    account = self.get_account()
                    amount = self.get_amount()
                    account.deposit(amount)
                elif choice == "3":
                    account = self.get_account()
                    amount = self.get_amount()
                    account.withdraw(amount)
                elif choice == "4":
                    from_account = self.get_account()
                    to_account = self.get_account()
                    amount = self.get_amount()
                    from_account.transfer(amount, to_account)
                elif choice == "5":
                    self.bank.save_to_csv("bank_state.csv")
                elif choice == "6":
                    self.bank.load_from_csv("bank_state.csv")
                elif choice == "7":
                    print("Exiting the bank system.")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError as e:
                print(e)


if __name__ == '__main__':
    bank = Bank()
    bank.load_from_csv("bank_state.csv")
    app = BankApp(bank)
    app.run()
