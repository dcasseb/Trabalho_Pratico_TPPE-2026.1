import pytest
from src.deduplicador import Deduplicador


@pytest.mark.caso1
class TestDiferencasGrafia:
    """
    Suite – Caso 1: Diferenças de grafia tipográficas.

    Verifica que nomes que diferem apenas em acentuação, cedilha ou
    variante de apóstrofo são reconhecidos como equivalentes e que
    nomes efetivamente distintos não são.
    """

    @pytest.fixture(autouse=True)
    def _setup(self, deduplicador):
        self.ded = deduplicador

# Testes parametrizados – pares equivalentes (dataset 1 e 2)

    @pytest.mark.parametrize(
        "nome1, nome2",
        [
            # Dataset 1 – dados do enunciado
            ("Monica Hirata Sant`anna", "Mônica Hirata Sant'anna"),
            ("Sergio Henrique Guaraldi", "Sérgio Henrique Guaraldi"),
            ("Veronica de Oliveira Moreira", "Verônica de Oliveira Moreira"),
            ("Lilian Luiza Viana Vieira", "Lílian Luíza Viana Vieira"),
            # Dataset 2 – variações adicionais
            ("Monica Hirata Sant'anna", "Mônica Hirata Sant\u2019anna"),
            ("Cassius de Souza", "Cassius de Souza"),
            ("Raphael Goncalves Viana", "Raphael Gonçalves Viana"),
            ("Vanilda Cristina Junior", "Vanilda Cristina Júnior"),
        ],
    )
    def test_nomes_equivalentes_tipografia(self, nome1: str, nome2: str):
        # existe: diferença só de acento/apóstrofe não deve criar dois autores distintos no repositório
        assert self.ded.sao_equivalentes_tipografia(nome1, nome2) is True

# Testes parametrizados – pares NÃO equivalentes


    @pytest.mark.parametrize(
        "nome1, nome2",
        [
            ("Ana de Mattos Seabra", "Ana de Oliveira Seabra"),
            ("Monica Hirata Santanna", "Joana Hirata Sant'anna"),
            ("Carlos Silva", "Carlos Santos"),
            ("Sérgio Guaraldi", "Sérgio Henrique Guaraldi"),
        ],
    )
    def test_nomes_nao_equivalentes_tipografia(self, nome1: str, nome2: str):
        # existe: nomes com sobrenomes realmente distintos não podem ser falso-positivos
        assert self.ded.sao_equivalentes_tipografia(nome1, nome2) is False

# Testes de exceção

    def test_excecao_nome1_none(self):
        # TypeError: None não é str; a API deve falhar antes de tentar processar o texto
        with pytest.raises(TypeError):
            self.ded.sao_equivalentes_tipografia(None, "Ana de Mattos Seabra")

    def test_excecao_nome2_none(self):
        # TypeError: mesmo comportamento quando None está no segundo argumento
        with pytest.raises(TypeError):
            self.ded.sao_equivalentes_tipografia("Ana de Mattos Seabra", None)

    def test_excecao_nome1_vazio(self):
        # ValueError: string vazia não representa nome de autor
        with pytest.raises(ValueError):
            self.ded.sao_equivalentes_tipografia("", "Ana de Mattos Seabra")

    def test_excecao_nome2_apenas_espacos(self):
        # ValueError: espaços em branco também são rejeitados como entrada inválida
        with pytest.raises(ValueError):
            self.ded.sao_equivalentes_tipografia("Ana de Mattos Seabra", "   ")
