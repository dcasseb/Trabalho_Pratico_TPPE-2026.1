from src.deduplicador import Deduplicador

d = Deduplicador()

print("Caso 1:",
      d.sao_equivalentes_tipografia(
          "Monica Hirata Sant`anna",
          "Mônica Hirata Sant'anna"
      ))

print("Caso 2:",
      d.sao_equivalentes_abreviacao(
          "Ana de Mattos Seabra",
          "Seabra A. M."
      ))

print("Caso 3:",
      d.sao_equivalentes_particulas(
          "Luiz de Oliveira de Souza",
          "Luiz Oliveira Souza"
      ))

print("Caso 4:",
      d.sao_equivalentes_iniciais_agrupadas(
          "Sérgio Henrique Guaraldi",
          "SH Guaraldi"
      ))