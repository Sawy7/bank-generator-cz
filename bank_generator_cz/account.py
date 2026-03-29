"""Czech bank account number generator."""

from random import choice, randint, random

from bank_generator_cz.bank_codes import BANKS_CZ


class BankAccount:
    """Czech bank account."""

    CHECKSUM_WEIGHTS = (1, 2, 4, 8, 5, 10, 9, 7, 3, 6)

    def __init__(self, account_number: int, bank_code: str, prefix: int | None = None):
        """Create Czech bank account object."""
        self.prefix = prefix
        self.account_number = account_number
        self.bank_code = bank_code

    def __str__(self):
        """Return full string representation of bank account number."""
        str_rep = f"{self.account_number}/{self.bank_code}"
        if self.prefix:
            str_rep = f"{self.prefix}-{str_rep}"
        return str_rep

    @classmethod
    def _get_part_checksum(cls, number: int):
        """Get checksum of provided bank account number part."""
        num_mod = number
        checksum = 0
        index = 0
        while num_mod > 0:
            digit = num_mod % 10
            num_mod = num_mod // 10
            checksum += digit * cls.CHECKSUM_WEIGHTS[index]
            index += 1
        return checksum

    @classmethod
    def _is_part_valid(cls, number: int):
        return cls._get_part_checksum(number) % 11 == 0

    @classmethod
    def _generate_account_part(cls, min_digits: int, max_digits: int):
        """Generate part of the bank account number.

        The same rules apply to the prefix and the main part.
        """
        max_value = int("9" * (max_digits - 1))
        min_value = 10**min_digits // 10
        prefix = randint(min_value, max_value) * 10
        checksum = cls._get_part_checksum(prefix)
        to_add = 11 - checksum % 11
        if to_add < 10:
            prefix += to_add
            return prefix
        return None

    @classmethod
    def generate_random(cls, include_prefix: bool | None = None):
        """Generate the full bank account number.

        The account number consists of:
            - Prefix (optional, max 6 digits)
            - Main part (max 10 digits)
            - Bank code (4 digits, zero-padded)

        Args:
            include_prefix: Whether to include prefix in the bank account number.
                Will be respected if set, otherwise random if None.
        """
        # Prefix (80 % change there isn't one)
        if include_prefix or include_prefix is None and random() > 0.8:
            while True:
                prefix = cls._generate_account_part(2, 6)
                if prefix:
                    break
        else:
            prefix = None

        # Bank account number
        while True:
            account_number = cls._generate_account_part(1, 10)
            if account_number:
                break

        bank_code = choice(BANKS_CZ)[0]
        return cls(prefix=prefix, account_number=account_number, bank_code=bank_code)

    def is_valid(self, check_bank_code: bool = False):
        """Check if bank account number is valid.

        Args:
            check_bank_code: Whether to check if bank code in on the official ČNB list.
        """
        return (
            (not self.prefix or self._is_part_valid(self.prefix))
            and self._is_part_valid(self.account_number)
            and (not check_bank_code or self.bank_code in BANKS_CZ)
        )


if __name__ == "__main__":
    account = BankAccount.generate_random()
    print(account)
