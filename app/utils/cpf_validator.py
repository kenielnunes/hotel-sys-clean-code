import re
from typing import List


def _calculate_verification_digit(digits: str, factor: int) -> int:
    total = sum(int(digit) * (factor - idx) for idx, digit in enumerate(digits))
    remainder = total % 11
    return 0 if remainder < 2 else 11 - remainder


def _is_blacklisted_cpf(digits: str) -> bool:
    return digits == digits[0] * 11


def cpf_validator(cpf: str) -> bool:
    digits_only = re.sub(r'\D', '', cpf)
    
    if len(digits_only) != 11 or _is_blacklisted_cpf(digits_only):
        return False
        
    first_digit = _calculate_verification_digit(digits_only[:9], 10)
    second_digit = _calculate_verification_digit(digits_only[:10], 11)
    
    return digits_only[-2:] == f"{first_digit}{second_digit}"
