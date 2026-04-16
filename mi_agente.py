"""
mi_agente.py — Aquí defines tu agente.
╔══════════════════════════════════════════════╗
║  ✏️  EDITA ESTE ARCHIVO                      ║
╚══════════════════════════════════════════════╝

Tu agente debe:
    1. Heredar de la clase Agente
    2. Implementar el método decidir(percepcion)
    3. Retornar: 'arriba', 'abajo', 'izquierda' o 'derecha'

Lo que recibes en 'percepcion':
───────────────────────────────
percepcion = {
    'posicion':       (3, 5),          # Tu fila y columna actual
    'arriba':         'libre',         # Qué hay arriba
    'abajo':          'pared',         # Qué hay abajo
    'izquierda':      'libre',         # Qué hay a la izquierda
    'derecha':        None,            # None = fuera del mapa

    # OPCIONAL — brújula hacia la meta.
    # No es percepción real del entorno, es información global.
    # Usarla hace el ejercicio más fácil. No usarla es más realista.
    'direccion_meta': ('abajo', 'derecha'),
}

Valores posibles de cada dirección:
    'libre'  → puedes moverte ahí
    'pared'  → bloqueado
    'meta'   → ¡la meta! ve hacia allá
    None     → borde del mapa, no puedes ir

Si tu agente retorna un movimiento inválido (hacia pared o
fuera del mapa), simplemente se queda en su lugar.
"""

from entorno import Agente
import random

class MiAgente(Agente):
    def __init__(self):
        super().__init__(nombre="Explorador de Utilidad v1")

    def decidir(self, percepcion):
        direcciones_meta = percepcion['direccion_meta']
        mejores_acciones = []
        max_utilidad = float('-inf')

        for accion in self.ACCIONES:
            estado_celda = percepcion[accion]
            
            if estado_celda is None or estado_celda == 'pared':
                continue

            if estado_celda == 'meta':
                return accion

            # FUNCIÓN DE UTILIDAD BÁSICA
            utilidad = 0
            if accion in direcciones_meta:
                utilidad += 50  # Premio por ir en la dirección correcta

            if utilidad > max_utilidad:
                max_utilidad = utilidad
                mejores_acciones = [accion]
            elif utilidad == max_utilidad:
                mejores_acciones.append(accion)

        return random.choice(mejores_acciones) if mejores_acciones else 'abajo'


