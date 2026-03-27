"""Czech bank account number generator."""

from random import choice, randint, random

from bank_codes import BANKS_CZ


def get_part_checksum(number: int):
    """Get checksum of provided bank account number part."""
    weights = (1, 2, 4, 8, 5, 10, 9, 7, 3, 6)
    num_mod = number
    checksum = 0
    index = 0
    while num_mod > 0:
        digit = num_mod % 10
        num_mod = num_mod // 10
        checksum += digit * weights[index]
        index += 1
    return checksum


def generate_account_part(min_digits: int, max_digits: int):
    """Generate part of the bank account number.

    The same rules apply to the prefix and the main part.
    """
    max_value = int("9" * (max_digits - 1))
    min_value = 10**min_digits // 10
    prefix = randint(min_value, max_value) * 10
    checksum = get_part_checksum(prefix)
    to_add = 11 - checksum % 11
    if to_add < 10:
        prefix += to_add
        return prefix
    return None


def generate_full_account():
    """Generate the full bank account number.

    The account number consists of:
        - Prefix (optional, max 6 digits)
        - Main part (max 10 digits)
        - Bank code (4 digits, zero-padded)
    """
    # Prefix (80 % change there isn't one)
    if random() > 0.8:
        while True:
            prefix = generate_account_part(2, 6)
            if prefix:
                break
    else:
        prefix = None

    # Bank account number
    while True:
        acc_num = generate_account_part(1, 10)
        if acc_num:
            break

    # Put it all together
    random_bank = choice(BANKS_CZ)
    full_acc = f"{acc_num}/{random_bank[0]}"
    if prefix:
        full_acc = f"{prefix}-{full_acc}"
    return full_acc


if __name__ == "__main__":
    full_acc = generate_full_account()
    print(full_acc)
