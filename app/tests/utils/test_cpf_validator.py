import pytest
from utils.cpf_validator import cpf_validator


@pytest.mark.parametrize(
    "valid_cpf",
    [
        "529.982.247-25",
        "52998224725",
        "168.995.350-09",
    ],
)
def test_valid_cpfs(valid_cpf):
    assert cpf_validator(valid_cpf) is True


@pytest.mark.parametrize(
    "invalid_cpf",
    [
        "123.456.789-00",  # invalid checksum
        "111.111.111-11",  # blacklisted
        "00000000000",  # blacklisted
        "529.982.247",  # too short
        "abc.def.ghi-jk",  # not digits
    ],
)
def test_invalid_cpfs(invalid_cpf):
    assert cpf_validator(invalid_cpf) is False
