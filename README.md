# Simple Banking System

A Python-based simple banking system that allows users to create accounts, deposit and withdraw money, transfer funds between accounts, and save/load state to/from CSV files.

## Setup

Follow these instructions to set up the project on your local machine.

1. Install Python 3.8+ onto your machine ([Download Python](https://www.python.org/downloads/)).

2. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/lim-jia-wei/banking-system.git
   cd banking-system
   ```

2. Set up a virtual environment (optional):
   ```bash
    python -m venv venv

    # On macOS and Linux:
    source venv/bin/activate

    # On Windows:
    .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
    pip install -r requirements.txt
   ```

## Usage

1. Run the Banking System app through your preferred CLI:
   ```bash
    python bank.py
   ```

2. Run Unit Tests:
   ```bash
    pytest test_bank.py
   ```