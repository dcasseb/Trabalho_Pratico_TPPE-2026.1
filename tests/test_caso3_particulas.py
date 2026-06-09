import pytest
from src.deduplicador import Deduplicador


@pytest.mark.caso3
class TestParticulasEPontos:
    """
    Suite – Caso 3: Partículas de/da/do e pontos opcionais em abreviações.

    Verifica que nomes com e sem partículas (de, da, do, dos) e com e sem
    ponto após iniciais são reconhecidos como equivalentes.
    """

    @pytest.fixture(autouse=True)
    def _setup(self, deduplicador):
        self.ded = deduplicador

# Testes parametrizados – pares equivalentes (dataset 1 e 2)

    @pytest.mark.parametrize(
        "nome1, nome2",
        [
            # Dataset 1 – omissão das partículas "de"
            ("Luiz de Oliveira de Souza", "Luiz Oliveira Souza"),
            ("Veronica de Oliveira Moreira", "Veronica Oliveira Moreira"),
            ("Ana de Mattos Seabra", "Ana Mattos Seabra"),
            # Dataset 2 – combinação de partícula omitida e ponto opcional
            ("Luiz de Oliveira de Souza", "Luiz de O. de Souza"),
            ("Luiz Oliveira Souza", "Luiz de O. de Souza"),
            ("Monica Hirata Sant'anna", "Monica Hirata Sant'anna"),
        ],
    )
    def test_equivalentes_particulas(self, nome1: str, nome2: str):
        # existe: bases como Scopus omitem "de"; registros com e sem partícula devem coincidir
        assert self.ded.sao_equivalentes_particulas(nome1, nome2) is True

# Testes parametrizados – pares NÃO equivalentes
    @pytest.mark.parametrize(
        "nome1, nome2",
        [
            # Sobrenome diferente
            ("Luiz de Oliveira de Souza", "Luiz de Oliveira de Castro"),
            # Nomes com número diferente de partes após remover partículas
            ("Luiz de Oliveira de Souza", "Luiz Souza"),
            # Iniciais incompatíveis
            ("Luiz de Oliveira de Souza", "Luiz de A. de Souza"),
        ],
    )
    def test_nao_equivalentes_particulas(self, nome1: str, nome2: str):
        # existe: diferença real nos nomes não pode ser absorvida pela remoção de partículas
        assert self.ded.sao_equivalentes_particulas(nome1, nome2) is False

# Testes de exceção

    def test_excecao_nome1_none(self):
        # TypeError: None impede split e remoção de partículas
        with pytest.raises(TypeError):
            self.ded.sao_equivalentes_particulas(None, "Luiz Oliveira Souza")

    def test_excecao_nome2_none(self):
        # TypeError: mesmo comportamento para o segundo argumento
        with pytest.raises(TypeError):
            self.ded.sao_equivalentes_particulas("Luiz de Oliveira de Souza", None)

    def test_excecao_nome1_vazio(self):
        # ValueError: sem tokens, a lista normalizada fica vazia
        with pytest.raises(ValueError):
            self.ded.sao_equivalentes_particulas("", "Luiz Oliveira Souza")

    def test_excecao_nome2_vazio(self):
        # ValueError: só espaços também é rejeitado como entrada inválida
        with pytest.raises(ValueError):
            self.ded.sao_equivalentes_particulas("Luiz de Oliveira de Souza", "  ")
