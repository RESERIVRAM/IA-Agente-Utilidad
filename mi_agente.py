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
    """
    Agente basado en utilidad para navegación en mapa con paredes.
    """

    def __init__(self):
        super().__init__(nombre="Explorador de Utilidad")
        # Memoria para contar cuántas veces hemos pasado por cada celda
        self.historial_visitas = {}

    def al_iniciar(self):
        """Reinicia la memoria al empezar una nueva simulación."""
        self.historial_visitas = {}

    def decidir(self, percepcion):
        """
        Decide el movimiento evaluando la UTILIDAD de cada opción.
        La utilidad considera la distancia a la meta y el número de pasos (penalizando retrocesos).
        """
        pos_actual = percepcion['posicion']
        # Registramos la visita a la posición actual
        self.historial_visitas[pos_actual] = self.historial_visitas.get(pos_actual, 0) + 1
        
        direcciones_meta = percepcion['direccion_meta']
        mejores_acciones = []
        max_utilidad = float('-inf')

        for accion in self.ACCIONES:
            estado_celda = percepcion[accion]
            
            # 1. Ignorar movimientos imposibles
            if estado_celda is None or estado_celda == 'pared':
                continue

            # 2. Prioridad máxima: La Meta
            if estado_celda == 'meta':
                return accion

            # 3. Calcular Utilidad
            futura_pos = self._predecir_posicion(pos_actual, accion)
            num_visitas = self.historial_visitas.get(futura_pos, 0)

            # --- MEDIDA DE UTILIDAD (Número de pasos) ---
            utilidad = 100 
            
            # Bono: Acercarnos geográficamente a la meta
            if accion in direcciones_meta:
                utilidad += 50
            
            # Costo: Penalización por pasos (visitas). 
            # Minimiza el número de pasos totales al priorizar caminos inexplorados
            utilidad -= (num_visitas * 30)
            # ---------------------------

            if utilidad > max_utilidad:
                max_utilidad = utilidad
                mejores_acciones = [accion]
            elif utilidad == max_utilidad:
                mejores_acciones.append(accion)

        return mejores_acciones[0] if mejores_acciones else 'abajo'

    def _predecir_posicion(self, pos, accion):
        """Calcula la coordenada resultante de un movimiento."""
        f, c = pos
        if accion == 'arriba': return (f - 1, c)
        if accion == 'abajo': return (f + 1, c)
        if accion == 'izquierda': return (f, c - 1)
        if accion == 'derecha': return (f, c + 1)
        return pos
