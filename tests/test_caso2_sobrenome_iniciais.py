import pytest
from src.deduplicador import Deduplicador


@pytest.mark.caso2
class TestSobrenomeIniciais:
    """
    Suite – Caso 2: Sobrenome + iniciais dos nomes.

    Verifica que nomes completos e suas versões abreviadas no formato
    "Sobrenome I." ou "I. Sobrenome" (com ou sem pontos nas iniciais)
    são reconhecidos como equivalentes.
    """

    @pytest.fixture(autouse=True)
    def _setup(self, deduplicador):
        self.ded = deduplicador

# Testes parametrizados – pares equivalentes (dataset 1 e 2)

    @pytest.mark.parametrize(
        "nome_completo, nome_abreviado",
        [
            # Dataset 1 – dados do enunciado (sobrenome primeiro)
            ("Ana de Mattos Seabra", "Seabra A. M."),
            ("Cassius de Souza", "Souza C."),
            ("Veronica de Oliveira Moreira", "Moreira V. O."),
            # Dataset 2 – iniciais antes do sobrenome e sem pontos
            ("Ana de Mattos Seabra", "A. M. Seabra"),
            ("Cassius de Souza", "C. Souza"),
            ("Luiz de Oliveira de Souza", "Souza L. O."),
            ("Monica Hirata Sant'anna", "M. H. Sant'anna"),
        ],
    )
    def test_abreviacao_equivalente(self, nome_completo: str, nome_abreviado: str):
        # existe: indexadores como Scopus gravam "Seabra A. M."; deve unificar ao nome completo
        assert self.ded.sao_equivalentes_abreviacao(nome_completo, nome_abreviado) is True

# Testes parametrizados – pares NÃO equivalentes
    @pytest.mark.parametrize(
        "nome_completo, nome_abreviado",
        [
            # Sobrenome diferente
            ("Ana de Mattos Seabra", "Silva A. M."),
            # Iniciais não correspondem
            ("Cassius de Souza", "Souza A."),
            # Abreviado sem iniciais (não é abreviação)
            ("Ana de Mattos Seabra", "Seabra"),
            # Nome completo passado como abreviado
            ("Ana de Mattos Seabra", "Ana de Mattos Seabra"),
        ],
    )
    def test_abreviacao_nao_equivalente(self, nome_completo: str, nome_abreviado: str):
        # existe: sobrenome ou iniciais errados não podem gerar falso-positivo no algoritmo
        assert self.ded.sao_equivalentes_abreviacao(nome_completo, nome_abreviado) is False

# Testes de exceção

    def test_excecao_nome_completo_none(self):
        # TypeError: nome completo None não pode ser decomposto em partes
        with pytest.raises(TypeError):
            self.ded.sao_equivalentes_abreviacao(None, "Seabra A. M.")

    def test_excecao_nome_abreviado_none(self):
        # TypeError: abreviado None impede extração de iniciais
        with pytest.raises(TypeError):
            self.ded.sao_equivalentes_abreviacao("Ana de Mattos Seabra", None)

    def test_excecao_nome_vazio(self):
        # ValueError: vazio não tem partes para comparar
        with pytest.raises(ValueError):
            self.ded.sao_equivalentes_abreviacao("", "Seabra A. M.")

    def test_excecao_abreviado_vazio(self):
        # ValueError: abreviado vazio não contém nem inicial nem sobrenome
        with pytest.raises(ValueError):
            self.ded.sao_equivalentes_abreviacao("Ana de Mattos Seabra", "")
