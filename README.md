# bank-generator-cz

Generator of valid Czech bank account numbers with the most current actual bank codes.

## Installation

### Include in your project using uv

```bash
uv add bank-generator-cz
```

### Install using pip

```bash
pip install bank-generator-cz
```

## Usage

```python
from bank_generator_cz.account import BankAccount

account = BankAccount.generate_random()
account_str = str(account)

print(f"This bank account is valid: {account.is_valid()}")
print(f"\t- Full string form: {str(account)}")
print(f"\t- Prefix: {account.prefix}")
print(f"\t- Main part: {account.account_number}")
print(f"\t- Bank code: {account.bank_code}")
```
