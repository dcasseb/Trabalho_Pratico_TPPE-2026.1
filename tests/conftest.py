import pytest
from src.deduplicador import Deduplicador


@pytest.fixture
def deduplicador():
    """Instância compartilhada de Deduplicador para todos os testes."""
    return Deduplicador()
