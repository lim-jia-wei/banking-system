# standard import
import csv
from typing import Dict, Optional


class Account:
    def __init__(self, account_name: str, balance: float = 0.0) -> None:
        self.account_name: str = account_name
        self.balance: float = balance

    def deposit(self, deposit_amount: float) -> None:
        if deposit_amount > 0:
            self.balance += deposit_amount
            print(f"Deposited ${deposit_amount:.2f} to {self.account_name}'s account.")
        else:
            raise ValueError("Deposit amount must be positive.")

    def withdraw(self, withdrawal_amount: float) -> None:
        if 0 < withdrawal_amount <= self.balance:
            self.balance -= withdrawal_amount
            print(f"Withdrew ${withdrawal_amount:.2f} from {self.account_name}'s account.")
        else:
            raise ValueError("Insufficient funds or invalid amount.")

    def transfer(self, transfer_amount: float, target_account: 'Account') -> None:
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

    def __str__(self) -> str:
        return f"Account({self.account_name}, Balance: ${self.balance:.2f})"


class Bank:
    def __init__(self) -> None:
        self.accounts: Dict[str, Account] = {}

    def create_account(self, account_name: str, starting_balance: float = 0.0) -> None:
        if account_name not in self.accounts:
            self.accounts[account_name] = Account(account_name, starting_balance)
            print(f"Account created for {account_name}.")
        else:
            raise ValueError("Account already exists.")

    def get_account(self, account_name: str) -> Optional[Account]:
        return self.accounts.get(account_name, None)

    def save_to_csv(self, filename: str) -> None:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Name', 'Balance'])
            for bank_account in self.accounts.values():
                writer.writerow([bank_account.account_name, f"{bank_account.balance:.2f}"])
        print(f"Bank state saved to {filename}.")

    def load_from_csv(self, filename: str) -> None:
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

    def __str__(self) -> str:
        return "\n".join(str(account) for account in self.accounts.values())


class BankApp:
    def __init__(self, my_bank: Bank) -> None:
        self.bank = my_bank

    def print_menu(self) -> None:
        print("\nMenu:")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Save State")
        print("6. Load State")
        print("7. Exit")

    def get_account(self) -> Account:
        name = input("Enter account name: ")
        account = self.bank.get_account(name)
        if not account:
            raise ValueError("Account not found.")
        return account

    def get_amount(self) -> float:
        try:
            amount = float(input("Enter amount: "))
            return amount
        except ValueError as e:
            raise ValueError("Amount is invalid. Please input only numeric value.") from e

    def run(self) -> None:
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
