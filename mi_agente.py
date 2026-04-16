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

class MiAgente(Agente):
    def __init__(self):
        super().__init__(nombre="Explorador de Utilidad v2")
        self.historial_visitas = {}

    def al_iniciar(self):
        self.historial_visitas = {}

    def _predecir_posicion(self, pos, accion):
        f, c = pos
        if accion == 'arriba': return (f - 1, c)
        if accion == 'abajo': return (f + 1, c)
        if accion == 'izquierda': return (f, c - 1)
        if accion == 'derecha': return (f, c + 1)
        return pos

    def decidir(self, percepcion):
        pos_actual = percepcion['posicion']
        self.historial_visitas[pos_actual] = self.historial_visitas.get(pos_actual, 0) + 1
        
        direcciones_meta = percepcion['direccion_meta']
        mejor_accion = 'abajo'
        max_utilidad = float('-inf')

        for accion in self.ACCIONES:
            estado_celda = percepcion[accion]
            if estado_celda is None or estado_celda == 'pared':
                continue
            if estado_celda == 'meta':
                return accion

            futura_pos = self._predecir_posicion(pos_actual, accion)
            num_visitas = self.historial_visitas.get(futura_pos, 0)

            # FUNCIÓN DE UTILIDAD: Premio por dirección, Penalización por pasos/visitas
            utilidad = 100 
            if accion in direcciones_meta:
                utilidad += 50
            utilidad -= (num_visitas * 30) # Penaliza revisitar celdas para minimizar pasos totales

            if utilidad > max_utilidad:
                max_utilidad = utilidad
                mejor_accion = accion

        return mejor_accion


