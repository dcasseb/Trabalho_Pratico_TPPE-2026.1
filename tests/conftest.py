import pytest
from src.deduplicador import Deduplicador


@pytest.fixture
def deduplicador():
    return Deduplicador()
