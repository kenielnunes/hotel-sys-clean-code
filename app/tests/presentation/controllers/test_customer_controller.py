import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from core.presentation.controllers.customer_controller import CustomerController
from core.domain.entities.customer import Customer
from core.presentation.types.customer_types import CustomerRequest


class TestCustomerController:
    @pytest.fixture
    def customer_controller(self):
        return CustomerController()

    @pytest.fixture
    def mock_customer(self):
        return Customer(
            id=1,
            name="Test Customer",
            cpf="123.456.789-00",
            created_at=datetime.now()
        )

    def test_create_customer_success(self, customer_controller, mock_customer):
        # Arrange
        request: CustomerRequest = {
            "name": "Test Customer",
            "cpf": "123.456.789-00"
        }

        with patch.object(
            customer_controller._create_customer_use_case,
            'execute',
            return_value=mock_customer
        ):
            # Act
            response = customer_controller.create(request)

            # Assert
            assert response["status_code"] == 201
            assert response["body"]["id"] == mock_customer.id
            assert response["body"]["name"] == mock_customer.name
            assert response["body"]["cpf"] == mock_customer.cpf

    def test_create_customer_validation_error(self, customer_controller):
        request: CustomerRequest = {
            "name": "",  # Nome inválido
            "cpf": "123.456.789-00"
        }

        with patch.object(
            customer_controller._create_customer_use_case,
            'execute',
            side_effect=ValueError("Nome é obrigatório")
        ):
            response = customer_controller.create(request)

            assert response["status_code"] == 400
            assert "error" in response["body"]
            assert "Nome é obrigatório" in response["body"]["error"]

    def test_create_customer_internal_error(self, customer_controller):
        request: CustomerRequest = {
            "name": "Test Customer",
            "cpf": "123.456.789-00"
        }

        with patch.object(
            customer_controller._create_customer_use_case,
            'execute',
            side_effect=Exception("Erro interno")
        ):
            response = customer_controller.create(request)

            assert response["status_code"] == 500
            assert response["body"]["error"] == "Internal server error"

    def test_create_customer_direct_success(self, customer_controller, mock_customer):
        with patch.object(
            customer_controller._create_customer_use_case,
            'execute',
            return_value=mock_customer
        ):
            result = customer_controller.create_customer(
                name="Test Customer",
                cpf="123.456.789-00"
            )

            assert result == mock_customer
            assert result.id == mock_customer.id
            assert result.name == mock_customer.name
            assert result.cpf == mock_customer.cpf

    def test_create_customer_direct_error(self, customer_controller):
        with patch.object(
            customer_controller._create_customer_use_case,
            'execute',
            side_effect=ValueError("Erro de validação")
        ):
            with pytest.raises(ValueError) as exc_info:
                customer_controller.create_customer(
                    name="Test Customer",
                    cpf="123.456.789-00"
                )
            assert str(exc_info.value) == "Erro de validação"

    def test_list_customers_success(self, customer_controller, mock_customer):
        mock_customers = [mock_customer]
        with patch.object(
            customer_controller._list_customers_use_case,
            'execute',
            return_value=mock_customers
        ):
            result = customer_controller.list_customers()

            assert result == mock_customers
            assert len(result) == 1
            assert result[0].id == mock_customer.id
            assert result[0].name == mock_customer.name
            assert result[0].cpf == mock_customer.cpf

    def test_list_customers_error(self, customer_controller):
        with patch.object(
            customer_controller._list_customers_use_case,
            'execute',
            side_effect=Exception("Erro ao listar clientes")
        ):
            with pytest.raises(Exception) as exc_info:
                customer_controller.list_customers()
            assert str(exc_info.value) == "Erro ao listar clientes"
