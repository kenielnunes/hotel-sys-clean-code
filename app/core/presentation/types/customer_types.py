from typing import TypedDict, List, Optional
from dataclasses import dataclass


class CustomerRequest(TypedDict):
    name: str
    cpf: str


class CustomerResponse(TypedDict):
    id: int
    name: str
    cpf: str


class CustomerListResponse(TypedDict):
    status_code: int
    body: List[CustomerResponse]


class CustomerSingleResponse(TypedDict):
    status_code: int
    body: CustomerResponse


class CustomerErrorResponse(TypedDict):
    status_code: int
    body: dict[str, str]


@dataclass
class CustomerUpdateRequest:
    name: Optional[str] = None
    cpf: Optional[str] = None
