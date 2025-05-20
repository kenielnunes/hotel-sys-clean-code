import pytest
from core.presentation.controllers.customer_controller import CustomerController
from core.presentation.types.customer_types import CustomerRequest


@pytest.fixture
def customer_controller():
    return CustomerController()


@pytest.mark.parametrize(
    "valid_customer",
    [
        {"name": "John Doe", "cpf": "529.982.247-25"},
        {"name": "Jane Smith", "cpf": "168.995.350-09"},
    ],
)
def test_create_customer_success(customer_controller, valid_customer):
    # Act
    response = customer_controller.create(valid_customer)

    # Assert
    assert response["status_code"] == 201
    assert response["body"]["name"] == valid_customer["name"]
    assert response["body"]["cpf"] == valid_customer["cpf"]
    assert response["body"]["id"] is not None


@pytest.mark.parametrize(
    "invalid_customer",
    [
        {"name": "John Doe", "cpf": "123.456.789-00"},  # invalid checksum
        {"name": "Jane Smith", "cpf": "111.111.111-11"},  # blacklisted
        {"name": "Bob Wilson", "cpf": "00000000000"},  # blacklisted
    ],
)
def test_create_customer_with_invalid_cpf(customer_controller, invalid_customer):
    # Act
    response = customer_controller.create(invalid_customer)

    # Assert
    assert response["status_code"] == 400
    assert "error" in response["body"]


@pytest.mark.parametrize(
    "invalid_request",
    [
        {"cpf": "529.982.247-25"},  # missing name
        {"name": "John Doe"},  # missing cpf
        {},  # empty request
    ],
)
def test_create_customer_with_missing_fields(customer_controller, invalid_request):
    # Act
    response = customer_controller.create(invalid_request)

    # Assert
    assert response["status_code"] == 400
    assert "error" in response["body"]


def test_create_duplicate_customer(customer_controller):
    # Arrange
    customer_data = {"name": "John Doe", "cpf": "529.982.247-25"}

    # Act
    first_response = customer_controller.create(customer_data)
    second_response = customer_controller.create(customer_data)

    # Assert
    assert first_response["status_code"] == 201
    assert second_response["status_code"] == 400
    assert "error" in second_response["body"]
    assert "already exists" in second_response["body"]["error"].lower()
