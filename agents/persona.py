import random
from mesa import Agent

from agents.objeto_fijo import ObjetoFijo
class Persona(Agent):
    def __init__(self, unique_id, model, virus=None):
        super().__init__(unique_id, model)
        self.estado = "S"  # S: Sano, E: Expuesto, I: Infectado, R: Recuperado, D: Muerto
        self.virus = virus
        self.tiempo_infeccion = 0

    def step(self):
        self.mover()             # Todos caminan, incluso los infectados
        self.contagiar()         # Los infectados pueden contagiar vecinos
        self.progresar_enfermedad()  # Evolución del estado


    def mover(self):
        if not self.objetivo or self.pos == self.objetivo:
            self.objetivo = self.seleccionar_nuevo_destino()
        self.mover_hacia(self.objetivo)

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
