import pytest
from src.deduplicador import Deduplicador


@pytest.mark.caso3
class TestParticulasEPontos:

    @pytest.fixture(autouse=True)
    def _setup(self, deduplicador):
        self.ded = deduplicador

    @pytest.mark.parametrize(
        "nome1, nome2",
        [
            ("Luiz de Oliveira de Souza", "Luiz Oliveira Souza"),
            ("Veronica de Oliveira Moreira", "Veronica Oliveira Moreira"),
            ("Ana de Mattos Seabra", "Ana Mattos Seabra"),
            ("Luiz de Oliveira de Souza", "Luiz de O. de Souza"),
            ("Luiz Oliveira Souza", "Luiz de O. de Souza"),
            ("Monica Hirata Sant'anna", "Monica Hirata Sant'anna"),
        ],
    )
    def test_equivalentes_particulas(self, nome1, nome2):
        assert self.ded.sao_equivalentes_particulas(nome1, nome2) is True

    @pytest.mark.parametrize(
        "nome1, nome2",
        [
            ("Luiz de Oliveira de Souza", "Luiz de Oliveira de Castro"),
            ("Luiz de Oliveira de Souza", "Luiz Souza"),
            ("Luiz de Oliveira de Souza", "Luiz de A. de Souza"),
        ],
    )
    def test_nao_equivalentes_particulas(self, nome1, nome2):
        assert self.ded.sao_equivalentes_particulas(nome1, nome2) is False

    def test_excecao_nome1_none(self):
        with pytest.raises(TypeError):
            self.ded.sao_equivalentes_particulas(None, "Luiz Oliveira Souza")

    def test_excecao_nome2_none(self):
        with pytest.raises(TypeError):
            self.ded.sao_equivalentes_particulas("Luiz de Oliveira de Souza", None)

    def test_excecao_nome1_vazio(self):
        with pytest.raises(ValueError):
            self.ded.sao_equivalentes_particulas("", "Luiz Oliveira Souza")

    def test_excecao_nome2_vazio(self):
        with pytest.raises(ValueError):
            self.ded.sao_equivalentes_particulas("Luiz de Oliveira de Souza", "  ")
