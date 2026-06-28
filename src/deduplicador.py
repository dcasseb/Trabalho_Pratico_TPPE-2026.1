import unicodedata
from collections import defaultdict


PARTICULAS = frozenset({"de", "da", "do", "dos", "das", "di", "del"})
APOSTROFES = ("`", "’", "ʼ")


def remover_acentos(texto):
    normalizado = unicodedata.normalize("NFD", texto)
    return "".join(c for c in normalizado if unicodedata.category(c) != "Mn")


def normalizar_apostrofe(texto):
    for variante in APOSTROFES:
        texto = texto.replace(variante, "'")
    return texto


def normalizar_tipografia(nome):
    return remover_acentos(normalizar_apostrofe(nome)).lower().strip()


def e_inicial(parte):
    parte = parte.rstrip(".")
    return len(parte) == 1 and parte.isalpha()


def e_iniciais_agrupadas(parte):
    return len(parte) >= 2 and parte.isalpha() and parte == parte.upper()


def validar_nomes(*nomes):
    for nome in nomes:
        if nome is None:
            raise TypeError("Os nomes não podem ser None")
        if not isinstance(nome, str):
            raise TypeError("Os nomes devem ser do tipo str")
        if not nome.strip():
            raise ValueError("Os nomes não podem ser vazios ou conter apenas espaços")

class ConjuntosDisjuntos:

    def __init__(self, tamanho):
        self.pai = list(range(tamanho))

    def encontrar(self, x):
        while self.pai[x] != x:
            self.pai[x] = self.pai[self.pai[x]]
            x = self.pai[x]
        return x

    def unir(self, x, y):
        rx, ry = self.encontrar(x), self.encontrar(y)
        if rx != ry:
            self.pai[rx] = ry

class UnificadorIds:

    def __init__(self, deduplicador, registros):
        self.deduplicador = deduplicador
        self.registros = registros
        self.n = len(registros)
        self.conjuntos = ConjuntosDisjuntos(self.n)

    def computar(self):
        self._unir_equivalentes()
        min_id_por_grupo = self._calcular_min_id_por_grupo()
        return [
            (min_id_por_grupo[self.conjuntos.encontrar(i)], self.registros[i][1])
            for i in range(self.n)
        ]

    def _unir_equivalentes(self):
        for i in range(self.n):
            for j in range(i + 1, self.n):
                id_i, nome_i = self.registros[i]
                id_j, nome_j = self.registros[j]
                if id_i != id_j and self.deduplicador._sao_mesmo_autor(nome_i, nome_j):
                    self.conjuntos.unir(i, j)

    def _calcular_min_id_por_grupo(self):
        grupos = defaultdict(list)
        for i in range(self.n):
            grupos[self.conjuntos.encontrar(i)].append(self.registros[i][0])
        return {g: min(ids) for g, ids in grupos.items()}


class Deduplicador:

    def sao_equivalentes_tipografia(self, nome1, nome2):
        validar_nomes(nome1, nome2)
        return self._normalizacoes_sao_iguais(nome1, nome2)

    def _normalizacoes_sao_iguais(self, nome1, nome2):
        return normalizar_tipografia(nome1) == normalizar_tipografia(nome2)

    def sao_equivalentes_abreviacao(self, nome_completo, nome_abreviado):
        validar_nomes(nome_completo, nome_abreviado)

        partes_abrev = nome_abreviado.split()
        iniciais_abrev = [p.rstrip(".").upper() for p in partes_abrev if e_inicial(p)]
        sobrenomes_abrev = [p for p in partes_abrev if not e_inicial(p)]

        if not sobrenomes_abrev or not iniciais_abrev:
            return False

        partes_completo = [
            p for p in nome_completo.split() if p.lower() not in PARTICULAS
        ]

        if len(partes_completo) < 2:
            return False

        for sobrenome_abrev in sobrenomes_abrev:
            for idx, parte in enumerate(partes_completo):
                if remover_acentos(parte).lower() == remover_acentos(sobrenome_abrev).lower():
                    primeiros = [p for i, p in enumerate(partes_completo) if i != idx]
                    if [p[0].upper() for p in primeiros] == iniciais_abrev:
                        return True

        return False

    def sao_equivalentes_particulas(self, nome1, nome2):
        validar_nomes(nome1, nome2)

        def normalizar_partes(nome):
            return [
                remover_acentos(p.rstrip("."))
                for p in nome.lower().split()
                if p.rstrip(".") not in PARTICULAS
            ]

        n1 = normalizar_partes(nome1)
        n2 = normalizar_partes(nome2)

        if len(n1) != len(n2):
            return False

        for p1, p2 in zip(n1, n2):
            if p1 == p2:
                continue
            if len(p1) == 1 and p2.startswith(p1):
                continue
            if len(p2) == 1 and p1.startswith(p2):
                continue
            return False

        return True

    def sao_equivalentes_iniciais_agrupadas(self, nome_completo, nome_abreviado):
        validar_nomes(nome_completo, nome_abreviado)

        partes_abreviado = nome_abreviado.split()
        iniciais_str = None
        outras_partes = []

        for parte in partes_abreviado:
            if e_iniciais_agrupadas(parte):
                iniciais_str = parte.upper()
            else:
                outras_partes.append(parte)

        if not iniciais_str or not outras_partes:
            return False

        sobrenome_abrev = outras_partes[-1]

        partes_completo = [
            p for p in nome_completo.split() if p.lower() not in PARTICULAS
        ]

        if len(partes_completo) < 2:
            return False

        sobrenome_completo = partes_completo[-1]
        primeiros_nomes = partes_completo[:-1]

        if remover_acentos(sobrenome_completo).lower() != remover_acentos(sobrenome_abrev).lower():
            return False

        iniciais_esperadas = "".join(p[0].upper() for p in primeiros_nomes)
        return iniciais_esperadas == iniciais_str

    def unificar_ids(self, registros):
        if registros is None:
            raise TypeError("A lista de registros não pode ser None")
        if not isinstance(registros, list):
            raise TypeError("Os registros devem ser uma lista de tuplas (id, nome)")
        if not registros:
            return []

        return UnificadorIds(self, registros).computar()

    def _sao_mesmo_autor(self, nome1, nome2):
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
            return False
