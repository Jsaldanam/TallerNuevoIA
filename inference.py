"""Punto 2. Inferencia exacta por enumeración."""
from algorithms.probability import normalize


def enumeration_ask(network, query: str, evidence: dict) -> dict:
    """Calcula P(query | evidence) sobre la conjunta factorizada.

    Entradas: network es la red; query es el nombre de la
    variable consultada; evidence es {nombre de variable: 0 o 1}.
    Salida: {0: probabilidad, 1: probabilidad}.

    Tips:
    - Recorra network.variables en orden topológico.
    - Para una variable fijada multiplique su probabilidad; para una oculta
      sume las dos alternativas 0 y 1. Normalice al terminar.
    - Use copias del evento y no modifique evidence.
    - network.probability(variable, valor, evento) consulta la CPT;
      el evento debe contener los valores de todos los padres.
    - Puede usar una función auxiliar recursiva. Al terminar el recorrido,
      el producto sin factores restantes vale 1.
    - Evidencia imposible: ValueError. Consulta observada: distribución puntual
      solo si la evidencia es posible.
    """
    # Valida nombres de variables y dominio de la evidencia.
    network.validate_query(query, evidence)

    # TODO: Add your code here
    def enumerate_all(variables_rest: list, evento: dict) -> float:
        if len(variables_rest) == 0:
            return 1.0
        primera = variables_rest[0]
        demas = variables_rest[1:]
        if primera in evento:
            valor = evento[primera]
            prob = network.probability(primera, valor, evento)
            return prob * enumerate_all(demas, evento)
        else:
            total = 0.0
            for valor in [0, 1]:
                copia_evento = dict(evento)
                copia_evento[primera] = valor
                prob = network.probability(primera, valor, copia_evento)
                total += prob * enumerate_all(demas, copia_evento)
            return total
    if query in evidence:
        prob_evidencia = enumerate_all(network.variables, dict(evidence))
        if prob_evidencia == 0.0:
            raise ValueError("La evidencia es imposible, probabilidad cero.")
        valor_obs = evidence[query]
        if valor_obs == 1:
            return {0: 0.0, 1: 1.0}
        else:
            return {0: 1.0, 1: 0.0}
    pesos = {}
    for valor in [0, 1]:
        evento_ext = dict(evidence)
        evento_ext[query] = valor
        pesos[valor] = enumerate_all(network.variables, evento_ext)
    if pesos[0] == 0.0 and pesos[1] == 0.0:
        raise ValueError("La evidencia es imposible, probabilidad cero.")
    return normalize(pesos)
    # FIN DEL BLOQUE DEL ESTUDIANTE
