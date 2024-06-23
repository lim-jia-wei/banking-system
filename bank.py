import csv
from typing import Dict, Optional


class Account:
    def __init__(self, account_name: str, balance: float = 0.0) -> None:
        self.account_name: str = account_name
        self.balance: float = balance

    def deposit(self, deposit_amount: float) -> None:
        if deposit_amount > 0:
            self.balance += deposit_amount
            print(f"Deposited ${deposit_amount} to {self.account_name}'s account.")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, withdrawal_amount: float) -> None:
        if 0 < withdrawal_amount <= self.balance:
            self.balance -= withdrawal_amount
            print(f"Withdrew ${withdrawal_amount} from {self.account_name}'s account.")
        else:
            print("Insufficient funds or invalid amount.")

    def transfer(self, transfer_amount: float, target_account: 'Account') -> None:
        if 0 < transfer_amount <= self.balance:
            self.balance -= transfer_amount
            target_account.deposit(transfer_amount)
            print(f"Transferred ${transfer_amount} from {self.account_name}'s account to {
                  target_account.account_name}'s account.")
        else:
            print("Insufficient funds or invalid amount.")

    def __str__(self) -> str:
        return f"Account({self.account_name}, Balance: ${self.balance})"


class Bank:
    def __init__(self) -> None:
        self.accounts: Dict[str, Account] = {}

    def create_account(self, account_name: str, starting_balance: float = 0.0) -> None:
        if account_name not in self.accounts:
            self.accounts[account_name] = Account(
                account_name, starting_balance)
            print(f"Account created for {account_name}.")
        else:
            print("Account already exists.")

    def get_account(self, account_name: str) -> Optional[Account]:
        return self.accounts.get(account_name, None)

    def save_to_csv(self, filename: str) -> None:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Name', 'Balance'])
            for bank_account in self.accounts.values():
                writer.writerow([bank_account.account_name, bank_account.balance])
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
        except FileNotFoundError:
            print(f"File {filename} not found.")

    def __str__(self) -> str:
        return "\n".join(str(account) for account in self.accounts.values())


if __name__ == '__main__':
    bank = Bank()
    bank.load_from_csv("bank_state.csv")

    def print_menu():
        print("\nMenu:")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Save State")
        print("6. Load State")
        print("7. Exit")

    while True:
        print_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter account name: ")
            try:
                amount = float(input("Enter the starting balance: "))
                bank.create_account(name, amount)
            except ValueError:
                print("Amount is invalid. Please input only numeric value.")

        elif choice == "2":
            name = input("Enter account name: ")
            try:
                amount = float(input("Enter deposit amount: "))
                account = bank.get_account(name)
                if account:
                    account.deposit(amount)
                else:
                    print("Account not found.")
            except ValueError:
                print("Amount is invalid. Please input only numeric value.")

        elif choice == "3":
            name = input("Enter account name: ")
            try:
                amount = float(input("Enter withdrawal amount: "))
                account = bank.get_account(name)
                if account:
                    account.withdraw(amount)
                else:
                    print("Account not found.")
            except ValueError:
                print("Amount is invalid. Please input only numeric value.")

        elif choice == "4":
            from_name = input("Enter your account name: ")
            to_name = input("Enter target account name: ")
            try:
                amount = float(input("Enter transfer amount: "))
                from_account = bank.get_account(from_name)
                to_account = bank.get_account(to_name)
                if from_account and to_account:
                    from_account.transfer(amount, to_account)
                else:
                    print("One or both accounts not found.")
            except ValueError:
                print("Amount is invalid. Please input only numeric value.")

        elif choice == "5":
            bank.save_to_csv("bank_state.csv")

        elif choice == "6":
            bank.load_from_csv("bank_state.csv")

        elif choice == "7":
            print("Exiting the bank system.")
            break

        else:
            print("Invalid choice. Please try again.")
