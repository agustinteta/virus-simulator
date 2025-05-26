import random
from mesa import Agent

from agents.objeto_fijo import ObjetoFijo
class Persona(Agent):
    def __init__(self, unique_id, model, virus=None):
        super().__init__(unique_id, model)
        self.estado = "S"  # S: Sano, E: Expuesto, I: Infectado, R: Recuperado, D: Muerto
        self.virus = virus
        self.tiempo_infeccion = 0
        self.objetivo = None  # Destino actual de la persona

    def step(self):
        self.mover()             # Todos caminan, incluso los infectados
        self.contagiar()         # Los infectados pueden contagiar vecinos
        self.progresar_enfermedad()  # Evolución del estado

    def mover(self):
        # Obtener vecinos ortogonales y diagonales (Moore)
        vecinos = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        # Filtrar solo celdas que sean parte de una zona, no estén ocupadas por otra Persona, ni sean pared u ObjetoFijo
        posibles = []
        for pos in vecinos:
            # Verifica que la celda sea parte de una zona válida
            if pos in self.model.zonas:
                contenido = self.model.grid.get_cell_list_contents([pos])
                # Verifica que no haya otra Persona ni ObjetoFijo en la celda
                ocupada = any(isinstance(a, Persona) or isinstance(a, ObjetoFijo) for a in contenido)
                # Verifica que no sea una pared (asumiendo que paredes están en self.model.paredes)
                es_pared = hasattr(self.model, "paredes") and pos in self.model.paredes
                if not ocupada and not es_pared:
                    posibles.append(pos)
        if posibles:
            nueva_pos = self.random.choice(posibles)
            self.model.grid.move_agent(self, nueva_pos)
            
    def seleccionar_nuevo_destino(self):
        # Mover entre cafetería, aula, conversatorio aleatoriamente
        zonas = ["cafeteria", "aula", "conversatorio"]
        zona_destino = self.random.choice(zonas)
        posiciones = [a.pos for a in self.model.schedule.agents if isinstance(a, ObjetoFijo) and a.tipo == zona_destino]
        return self.random.choice(posiciones) if posiciones else self.pos

    def mover_hacia(self, destino):
        x, y = self.pos
        dx = 1 if destino[0] > x else -1 if destino[0] < x else 0
        dy = 1 if destino[1] > y else -1 if destino[1] < y else 0
        nueva_pos = (x + dx, y + dy)
        if self.model.grid.out_of_bounds(nueva_pos):
            return
        ocupada = any(isinstance(a, Persona) for a in self.model.grid.get_cell_list_contents([nueva_pos]))
        if not ocupada:
            self.model.grid.move_agent(self, nueva_pos)

    def contagiar(self):
        if self.estado != 'I':
            return
        vecinos = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False)
        for agente in vecinos:
            if isinstance(agente, Persona) and agente.estado == 'S':
                if random.random() < self.virus.prob_contagio:
                    agente.estado = 'E'
                    agente.virus = self.virus

    def progresar_enfermedad(self):
        if self.estado == 'E':
            self.tiempo_infeccion += 1
            if self.tiempo_infeccion >= self.virus.duracion_incubacion:
                self.estado = 'I'
