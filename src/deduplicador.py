import unicodedata
from collections import defaultdict

# Constantes de módulo

# frozenset no módulo: busca O(1) e sem realocação a cada chamada de método
_PARTICULAS: frozenset = frozenset({"de", "da", "do", "dos", "das", "e", "di", "del"})
_APOSTROFES: tuple = ("`", "\u2019", "\u02bc")


# Funções puras de módulo (não usam estado de instância)

def _remover_acentos(texto: str) -> str:
    # NFD separa letra+acento em codepoints distintos; categoria Mn são os diacríticos — descartados
    normalizado = unicodedata.normalize("NFD", texto)
    return "".join(c for c in normalizado if unicodedata.category(c) != "Mn")


def _normalizar_apostrofe(texto: str) -> str:
    for variante in _APOSTROFES:
        texto = texto.replace(variante, "'")
    return texto


def _normalizar_tipografia(nome: str) -> str:
    # pipeline: apóstrofe → sem acento → minúsculo; forma canônica única para comparar nomes
    return _remover_acentos(_normalizar_apostrofe(nome)).lower().strip()


def _e_inicial(parte: str) -> bool:
    """Retorna True se `parte` for uma inicial (letra única, com ou sem ponto)."""
    parte = parte.rstrip(".")
    return len(parte) == 1 and parte.isalpha()


def _e_iniciais_agrupadas(parte: str) -> bool:
    """Retorna True se `parte` for iniciais agrupadas (≥2 letras maiúsculas, sem ponto)."""
    return len(parte) >= 2 and parte.isalpha() and parte == parte.upper()


def _validar_nomes(*nomes: str) -> None:
    for nome in nomes:
        # TypeError: None ou tipo não-str (int, list...) passado como nome de autor
        if nome is None:
            raise TypeError("Os nomes não podem ser None")
        if not isinstance(nome, str):
            raise TypeError("Os nomes devem ser do tipo str")
        # ValueError: string vazia ou só espaços não representa um nome válido
        if not nome.strip():
            raise ValueError("Os nomes não podem ser vazios ou conter apenas espaços")


class Deduplicador:
    """
    Classe responsável pela deduplicação de registros de autores em
    repositórios de informações científicas.

    Trata cinco casos de duplicidade:
      Caso 1 – Diferenças de grafia tipográficas (acentuação, apóstrofo, cedilha).
      Caso 2 – Sobrenome + iniciais dos nomes (com ou sem pontos nas iniciais).
      Caso 3 – Omissão de partículas (de/da/do) e uso opcional de ponto em abreviações.
      Caso 4 – Iniciais dos nomes agrupadas (ex.: "SH Guaraldi").
      Caso 5 – IDs diferentes para o mesmo autor; unifica pelo menor ID.
    """

    # Caso 1 – Diferenças de grafia tipográficas
    def sao_equivalentes_tipografia(self, nome1: str, nome2: str) -> bool:
        """
        Verifica se dois nomes são equivalentes apesar de diferenças tipográficas
        como acentuação, cedilha ou variantes de apóstrofo.

        Raises:
            TypeError: se algum dos nomes for None ou não for str.
            ValueError: se algum dos nomes estiver vazio.
        """
        _validar_nomes(nome1, nome2)
        # acentos e variantes de apóstrofe colapsam para a mesma forma; diferença só tipográfica desaparece
        return _normalizar_tipografia(nome1) == _normalizar_tipografia(nome2)
    # Caso 2 – Sobrenome + iniciais dos nomes
    def sao_equivalentes_abreviacao(self, nome_completo: str, nome_abreviado: str) -> bool:
        """
        Verifica se `nome_abreviado` (no formato "Sobrenome I." ou "I. Sobrenome")
        corresponde a `nome_completo`.

        Raises:
            TypeError: se algum dos nomes for None ou não for str.
            ValueError: se algum dos nomes estiver vazio.
        """
        _validar_nomes(nome_completo, nome_abreviado)

        # separa iniciais (ex.: "A.", "M.") dos sobrenomes presentes no nome abreviado
        partes_abrev = nome_abreviado.split()
        iniciais_abrev = [p.rstrip(".").upper() for p in partes_abrev if _e_inicial(p)]
        sobrenomes_abrev = [p for p in partes_abrev if not _e_inicial(p)]

        if not sobrenomes_abrev or not iniciais_abrev:
            return False

        partes_completo = [
            p for p in nome_completo.split() if p.lower() not in _PARTICULAS
        ]

        # com menos de 2 tokens reais não há como extrair iniciais correspondentes
        if len(partes_completo) < 2:
            return False

        # testa cada posição como sobrenome candidato: cobre "Sobrenome I." e "I. Sobrenome"
        for sobrenome_abrev in sobrenomes_abrev:
            for idx, parte in enumerate(partes_completo):
                if _remover_acentos(parte).lower() == _remover_acentos(sobrenome_abrev).lower():
                    primeiros = [p for i, p in enumerate(partes_completo) if i != idx]
                    if [p[0].upper() for p in primeiros] == iniciais_abrev:
                        return True

        return False

    # Caso 3 – Partículas e pontos opcionais em abreviações

    def sao_equivalentes_particulas(self, nome1: str, nome2: str) -> bool:
        """
        Verifica se dois nomes são equivalentes considerando:
          - Omissão opcional das partículas (de, da, do, etc.)
          - Uso opcional de ponto após iniciais abreviadas.

        Raises:
            TypeError: se algum dos nomes for None ou não for str.
            ValueError: se algum dos nomes estiver vazio.
        """
        _validar_nomes(nome1, nome2)

        # remove partícula, ponto e acento em passo único; "de O." e "oliveira" tornam-se equivalentes
        def normalizar_partes(nome: str) -> list:
            return [
                _remover_acentos(p.rstrip("."))
                for p in nome.lower().split()
                if p.rstrip(".") not in _PARTICULAS
            ]

        n1 = normalizar_partes(nome1)
        n2 = normalizar_partes(nome2)

        if len(n1) != len(n2):
            return False

        # compara parte a parte; inicial abreviada é aceita em qualquer lado do par
        for p1, p2 in zip(n1, n2):
            if p1 == p2:
                continue
            if len(p1) == 1 and p2.startswith(p1):
                continue
            if len(p2) == 1 and p1.startswith(p2):
                continue
            return False

        return True

# Caso 4 – Iniciais agrupadas + sobrenome

    def sao_equivalentes_iniciais_agrupadas(self, nome_completo: str, nome_abreviado: str) -> bool:
        """
        Verifica se `nome_abreviado` com iniciais agrupadas (ex.: "SH Guaraldi")
        corresponde a `nome_completo` (ex.: "Sérgio Henrique Guaraldi").

        Raises:
            TypeError: se algum dos nomes for None ou não for str.
            ValueError: se algum dos nomes estiver vazio.
        """
        _validar_nomes(nome_completo, nome_abreviado)

        partes_abreviado = nome_abreviado.split()
        iniciais_str = None
        outras_partes = []

        # localiza o token de iniciais agrupadas (≥2 maiúsculas sem ponto), ex.: "SH", "VC"
        for parte in partes_abreviado:
            if _e_iniciais_agrupadas(parte):
                iniciais_str = parte.upper()
            else:
                outras_partes.append(parte)

        if not iniciais_str or not outras_partes:
            return False

        sobrenome_abrev = outras_partes[-1]

        partes_completo = [
            p for p in nome_completo.split() if p.lower() not in _PARTICULAS
        ]

        if len(partes_completo) < 2:
            return False

        sobrenome_completo = partes_completo[-1]
        primeiros_nomes = partes_completo[:-1]

        if _remover_acentos(sobrenome_completo).lower() != _remover_acentos(sobrenome_abrev).lower():
            return False

        iniciais_esperadas = "".join(p[0].upper() for p in primeiros_nomes)
        return iniciais_esperadas == iniciais_str

# Caso 5 – IDs diferentes para o mesmo autor

    def unificar_ids(self, registros: list) -> list:
        """
        Recebe uma lista de tuplas (id, nome) referentes a uma publicação e
        unifica os IDs de registros que representam o mesmo autor, adotando
        o menor ID do grupo.

        Args:
            registros: lista de tuplas (int, str) — (id_autor, nome_autor).

        Returns:
            Nova lista de tuplas com os IDs unificados.

        Raises:
            TypeError: se `registros` for None ou não for uma lista.
        """
        if registros is None:
            raise TypeError("A lista de registros não pode ser None")
        if not isinstance(registros, list):
            raise TypeError("Os registros devem ser uma lista de tuplas (id, nome)")
        if not registros:
            return []

        # Union-Find: garante transitividade dos grupos sem comparar todas as tríades (evita O(n³))
        n = len(registros)
        pai = list(range(n))

        def encontrar(x: int) -> int:
            # path compression: achata a árvore a cada busca, mantendo operações quase O(1)
            while pai[x] != x:
                pai[x] = pai[pai[x]]
                x = pai[x]
            return x

        def unir(x: int, y: int) -> None:
            rx, ry = encontrar(x), encontrar(y)
            if rx != ry:
                pai[rx] = ry

        for i in range(n):
            for j in range(i + 1, n):
                id_i, nome_i = registros[i]
                id_j, nome_j = registros[j]
                if id_i != id_j and self._sao_mesmo_autor(nome_i, nome_j):
                    unir(i, j)

        grupos: dict = defaultdict(list)
        for i in range(n):
            grupos[encontrar(i)].append(registros[i][0])

        min_id_por_grupo = {g: min(ids) for g, ids in grupos.items()}
        return [(min_id_por_grupo[encontrar(i)], registros[i][1]) for i in range(n)]

    def _sao_mesmo_autor(self, nome1: str, nome2: str) -> bool:
        """Combina todos os critérios para verificar equivalência entre dois nomes."""
        try:
            return (
                self.sao_equivalentes_tipografia(nome1, nome2)
                or self.sao_equivalentes_abreviacao(nome1, nome2)
                or self.sao_equivalentes_abreviacao(nome2, nome1)
                or self.sao_equivalentes_particulas(nome1, nome2)
                or self.sao_equivalentes_iniciais_agrupadas(nome1, nome2)
                or self.sao_equivalentes_iniciais_agrupadas(nome2, nome1)
            )
        except (TypeError, ValueError):
            # nome None ou vazio no registro não propaga exceção; registro é tratado como autor distinto
            return False
