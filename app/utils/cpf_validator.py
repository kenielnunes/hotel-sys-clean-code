import re

import re

def cpf_validator(cpf: str) -> bool:
    # Remove non-digit characters
    digits_only = re.sub(r'\D', '', cpf)

    # Must be 11 digits
    if len(digits_only) != 11:
        return False

    # Eliminate obvious invalid CPFs like 111.111.111-11
    if digits_only == digits_only[0] * 11:
        return False

    # Helper to calculate each verification digit
    def calculate_digit(digits: str, factor: int) -> int:
        total = sum(int(d) * (factor - idx) for idx, d in enumerate(digits))
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder

    first_digit = calculate_digit(digits_only[:9], 10)
    second_digit = calculate_digit(digits_only[:10], 11)

    return digits_only[-2:] == f"{first_digit}{second_digit}"



def _strip_non_digits(value: str) -> str:
    return re.sub(r"\D", "", value)


def _has_valid_length(cpf: str) -> bool:
    return len(cpf) == 11


def _is_blacklisted(cpf: str) -> bool:
    return cpf == cpf[0] * len(cpf)


def _calculate_check_digit(cpf: str, weights: range, extra_digit: int = 0) -> int:
    numbers = [int(digit) for digit in cpf[: len(weights)]]
    if extra_digit:
        numbers.append(extra_digit)

    total = sum(d * w for d, w in zip(numbers, weights))
    remainder = (total * 10) % 11
    return 0 if remainder == 10 else remainder
