import pytest
from src.deduplicador import Deduplicador


@pytest.mark.caso5
class TestIdsDiferentes:

    @pytest.fixture(autouse=True)
    def _setup(self, deduplicador):
        self.ded = deduplicador

    def test_unificar_ids_mesmo_nome_tipografia(self):
        registros = [
            (31298, "Raphael Goncalves Viana"),
            (433094, "Raphael Gonçalves Viana"),
            (549243, "Raphael Gonçalves Viana"),
            (608297, "Raphael Gonçalves Viana"),
            (746938, "Raphael Gonçalves Viana"),
        ]
        resultado = self.ded.unificar_ids(registros)
        ids_resultantes = [r[0] for r in resultado]
        assert all(id_ == 31298 for id_ in ids_resultantes)

    def test_unificar_ids_com_cedilha_e_acento(self):
        registros = [
            (899639, "Lilian Luíza Viana Vieira"),
            (243351, "Lílian Luíza Viana Vieira"),
            (663795, "Lílian Luíza Viana Vieira"),
        ]
        resultado = self.ded.unificar_ids(registros)
        ids_resultantes = [r[0] for r in resultado]
        assert all(id_ == 243351 for id_ in ids_resultantes)

    @pytest.mark.parametrize(
        "registros, ids_esperados",
        [
            (
                [
                    (31298, "Raphael Goncalves Viana"),
                    (433094, "Raphael Gonçalves Viana"),
                    (28371, "Cassius de Souza"),
                    (746936, "Cassius Souza"),
                ],
                [31298, 31298, 28371, 28371],
            ),
            (
                [(100, "Ana de Mattos Seabra")],
                [100],
            ),
        ],
    )
    def test_unificar_ids_grupos_independentes(self, registros, ids_esperados):
        resultado = self.ded.unificar_ids(registros)
        assert [r[0] for r in resultado] == ids_esperados

    def test_unificar_ids_lista_vazia(self):
        assert self.ded.unificar_ids([]) == []

    def test_excecao_registros_none(self):
        with pytest.raises(TypeError):
            self.ded.unificar_ids(None)

    def test_excecao_registros_nao_lista(self):
        with pytest.raises(TypeError):
            self.ded.unificar_ids("Raphael Goncalves Viana")
