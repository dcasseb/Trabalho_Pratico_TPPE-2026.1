import pytest
from src.deduplicador import Deduplicador


@pytest.mark.caso5
class TestIdsDiferentes:
    """
    Suite – Caso 5: IDs diferentes para o mesmo autor.

    Verifica que registros com IDs distintos que representam o mesmo autor
    são unificados sob o menor ID do grupo.
    """

    @pytest.fixture(autouse=True)
    def _setup(self, deduplicador):
        self.ded = deduplicador

# Testes de unificação de IDs – dataset 1

    def test_unificar_ids_mesmo_nome_tipografia(self):
        # existe: mesmo autor pode ter até 5 entradas vindas de fontes diferentes; todas devem cair no menor ID
        """
        Dataset 1: Raphael Gonçalves Viana aparece com 5 IDs distintos.
        Todos devem ser unificados para o menor ID (31298).
        """
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

# Testes de unificação de IDs – dataset 2

    def test_unificar_ids_com_cedilha_e_acento(self):
        # existe: cobre Caso 5 combinado com Caso 1 — IDs distintos E grafia diferente
        """
        Dataset 2: Lílian Luíza Viana Vieira com IDs distintos.
        Devem ser unificados para o menor ID (243351).
        """
        registros = [
            (899639, "Lilian Luíza Viana Vieira"),
            (243351, "Lílian Luíza Viana Vieira"),
            (663795, "Lílian Luíza Viana Vieira"),
        ]
        resultado = self.ded.unificar_ids(registros)
        ids_resultantes = [r[0] for r in resultado]
        assert all(id_ == 243351 for id_ in ids_resultantes)

# Testes de comportamento com grupos independentes

    @pytest.mark.parametrize(
        "registros, ids_esperados",
        [
            # Dois grupos distintos: Raphael e Cassius não se confundem
            (
                [
                    (31298, "Raphael Goncalves Viana"),
                    (433094, "Raphael Gonçalves Viana"),
                    (28371, "Cassius de Souza"),
                    (746936, "Cassius Souza"),
                ],
                [31298, 31298, 28371, 28371],
            ),
            # Registro único não é alterado
            (
                [(100, "Ana de Mattos Seabra")],
                [100],
            ),
        ],
    )
    def test_unificar_ids_grupos_independentes(self, registros, ids_esperados):
        # existe: dois autores distintos na mesma publicação não devem ser mesclados entre si
        resultado = self.ded.unificar_ids(registros)
        assert [r[0] for r in resultado] == ids_esperados

    # Testes de lista vazia
    def test_unificar_ids_lista_vazia(self):
        # borda: lista vazia deve retornar vazia sem exceção
        assert self.ded.unificar_ids([]) == []

    # Testes de exceção
    def test_excecao_registros_none(self):
        # TypeError: None não é lista; rejeitado antes de qualquer iteração
        with pytest.raises(TypeError):
            self.ded.unificar_ids(None)

    def test_excecao_registros_nao_lista(self):
        # TypeError: string, dict ou qualquer não-lista também é rejeitado
        with pytest.raises(TypeError):
            self.ded.unificar_ids("Raphael Goncalves Viana")
