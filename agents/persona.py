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
        if self.estado != 'D':
            self.mover()
            self.progresar_enfermedad()
            self.contagiar()

    def mover(self):
        vecinos = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        destino = self.random.choice(vecinos)
        agentes_destino = self.model.grid.get_cell_list_contents([destino])
        if not any(isinstance(a, ObjetoFijo) for a in agentes_destino):
            self.model.grid.move_agent(self, destino)

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
                self.tiempo_infeccion = 0
        elif self.estado == 'I':
            self.tiempo_infeccion += 1
            if self.tiempo_infeccion >= self.virus.duracion_infeccion:
                if random.random() < self.virus.prob_muerte:
                    self.estado = 'D'
                else:
                    self.estado = 'R'
