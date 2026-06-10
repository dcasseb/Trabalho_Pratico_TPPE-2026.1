import pytest
from src.deduplicador import Deduplicador


@pytest.mark.caso2
class TestSobrenomeIniciais:

    @pytest.fixture(autouse=True)
    def _setup(self, deduplicador):
        self.ded = deduplicador

    @pytest.mark.parametrize(
        "nome_completo, nome_abreviado",
        [
            ("Ana de Mattos Seabra", "Seabra A. M."),
            ("Cassius de Souza", "Souza C."),
            ("Veronica de Oliveira Moreira", "Moreira V. O."),
            ("Ana de Mattos Seabra", "A. M. Seabra"),
            ("Cassius de Souza", "C. Souza"),
            ("Luiz de Oliveira de Souza", "Souza L. O."),
            ("Monica Hirata Sant'anna", "M. H. Sant'anna"),
        ],
    )
    def test_abreviacao_equivalente(self, nome_completo, nome_abreviado):
        assert self.ded.sao_equivalentes_abreviacao(nome_completo, nome_abreviado) is True

    @pytest.mark.parametrize(
        "nome_completo, nome_abreviado",
        [
            ("Ana de Mattos Seabra", "Silva A. M."),
            ("Cassius de Souza", "Souza A."),
            ("Ana de Mattos Seabra", "Seabra"),
            ("Ana de Mattos Seabra", "Ana de Mattos Seabra"),
        ],
    )
    def test_abreviacao_nao_equivalente(self, nome_completo, nome_abreviado):
        assert self.ded.sao_equivalentes_abreviacao(nome_completo, nome_abreviado) is False

    def test_excecao_nome_completo_none(self):
        with pytest.raises(TypeError):
            self.ded.sao_equivalentes_abreviacao(None, "Seabra A. M.")

    def test_excecao_nome_abreviado_none(self):
        with pytest.raises(TypeError):
            self.ded.sao_equivalentes_abreviacao("Ana de Mattos Seabra", None)

    def test_excecao_nome_vazio(self):
        with pytest.raises(ValueError):
            self.ded.sao_equivalentes_abreviacao("", "Seabra A. M.")

    def test_excecao_abreviado_vazio(self):
        with pytest.raises(ValueError):
            self.ded.sao_equivalentes_abreviacao("Ana de Mattos Seabra", "")
