from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agents.persona import Persona
from virus import Virus


# Función auxiliar para contar agentes en cierto estado
def contar_estado(modelo, estado):
    return sum(1 for agente in modelo.schedule.agents if agente.estado == estado)


class EpidemiaModel(Model):
    def __init__(self, N, width, height, virus):
        self.num_agentes = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        for i in range(self.num_agentes):
            if i == 0:
                agente = Persona(i, self, virus=virus)
            else:
                agente = Persona(i, self)
            self.schedule.add(agente)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agente, (x, y))

        # Inicializar el DataCollector
        self.datacollector = DataCollector(
            model_reporters={
                "S": lambda m: contar_estado(m, "S"),
                "E": lambda m: contar_estado(m, "E"),
                "I": lambda m: contar_estado(m, "I"),
                "R": lambda m: contar_estado(m, "R"),
                "D": lambda m: contar_estado(m, "D"),
            }
        )

        self.datacollector.collect(self)  # Colectar datos del estado inicial

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
