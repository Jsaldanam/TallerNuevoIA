"""Punto 1. Distribuciones discretas y decisiones de respuesta."""
import math


def normalize(weights: dict) -> dict:
    """Retorna un diccionario nuevo cuyas probabilidades suman uno.

    Entrada: weights = {resultado: peso}.
    Salida: {resultado: probabilidad}, con las mismas claves.

    Tips:
    - Conserve las claves y su orden; no modifique weights.
    - Rechace pesos negativos, no finitos, diccionarios vacíos y suma cero.
    """
    # TODO: Add your code here
    if len(weights) == 0:
        raise ValueError("El diccionario está vacio")
    sumatl = 0.0
    for llave in weights:
        valor = weights[llave]
        if not math.isfinite(valor):
            raise ValueError("Hay un valor no finito")
        if valor < 0:
            raise ValueError("Hay un peso negativo")
        sumatl += valor
    if sumatl == 0.0:
        raise ValueError("La suma de pesos no puede ser cero")
    resultado = {}
    for llave in weights:
        resultado[llave] = weights[llave] / sumatl
    return resultado

    # FIN DEL BLOQUE DEL ESTUDIANTE


def expected_utility(distribution: dict, utilities: dict) -> float:
    """Calcula sum_s P(s) U(s) para una acción.

    Entradas: distribution = {resultado: probabilidad} y
    utilities = {resultado: utilidad} para una sola acción.
    Salida: un número con la utilidad esperada.

    Tips:
    - distribution ya debe estar normalizada; no normalice utilidades.
    - Ambas tablas deben contener los mismos resultados posibles.
    """
    # Validación de las entradas; no modificar.
    if set(distribution) != set(utilities) or not distribution:
        raise ValueError("Probabilidades y utilidades deben tener las mismas claves")
    if any(not math.isfinite(p) or p < 0 for p in distribution.values()):
        raise ValueError("Distribución inválida")
    if not math.isclose(sum(distribution.values()), 1, abs_tol=1e-9):
        raise ValueError("La distribución debe sumar uno")
    if any(not math.isfinite(u) for u in utilities.values()):
        raise ValueError("Utilidades no finitas")
    # TODO: Add your code here
    utilidadesperada = 0.0
    for estado in distribution:
        p = distribution[estado]
        u = utilities[estado]
        utilidadesperada += p * u

    return utilidadesperada
    # FIN DEL BLOQUE DEL ESTUDIANTE


def best_action(distribution: dict, actions: dict) -> tuple[str, dict]:
    """Retorna (nombre de acción, utilidades esperadas por acción).

    Entradas: distribution = {resultado: probabilidad} y
    actions = {acción: {resultado: utilidad}}.
    Salida: (acción elegida, {acción: utilidad esperada}).

    Tips:
    - actions asocia cada acción con su tabla de utilidades.
    - Reutilice expected_utility y conserve la primera acción en los empates.
    """
    # Validación de las acciones; no modificar.
    if not actions:
        raise ValueError("Se requiere al menos una acción")
    # TODO: Add your code here
    utilidad_t = {}
    for accion in actions:
        tabla_u = actions[accion]
        utilidad_t[accion] = expected_utility(distribution, tabla_u)
    lista_acciones = list(actions.keys())
    mejor_a = lista_acciones[0]
    mejor_u = utilidad_t[mejor_a]
    for accion in actions:
        if utilidad_t[accion] > mejor_u:
            mejor_u = utilidad_t[accion]
            mejor_a = accion
    return mejor_a, utilidad_t
    # FIN DEL BLOQUE DEL ESTUDIANTE
