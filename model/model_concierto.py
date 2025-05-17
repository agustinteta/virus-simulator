from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from agents.persona import Persona
from agents.objeto_fijo import ObjetoFijo
from virus import Virus

class ConciertoCOVIDModel(Model):
    def __init__(self, num_personas=10000, grid_width=105, grid_height=75, duracion_simulacion=150):
        self.grid = MultiGrid(grid_width, grid_height, torus=False)
        self.schedule = RandomActivation(self)
        self.duracion_simulacion = duracion_simulacion
        self.datacollector = DataCollector(
            model_reporters={
                "Sano": lambda m: self.contar_por_estado("S"),
                "Expuesto": lambda m: self.contar_por_estado("E"),
                "Infectado": lambda m: self.contar_por_estado("I"),
            }
        )
        self.virus_covid = Virus("COVID-19", prob_contagio=0.05, duracion_incubacion=5, duracion_infeccion=50, prob_muerte=0)
        self.next_id_val = 0

        self._crear_zonas(grid_width, grid_height)
        self._crear_personas(num_personas)

    def _crear_zonas(self, width, height):
        # ejemplo escenario y entradas escalables según dimensiones
        for x in range(width//2 - 7, width//2 + 8):
            for y in range(height - 5, height):
                escenario = ObjetoFijo(self.next_id(), self, "escenario")
                self.grid.place_agent(escenario, (x, y))
        entradas = [(0, 0), (width-1, 0), (0, height-1), (width-1, height-1)]
        for pos in entradas:
            entrada = ObjetoFijo(self.next_id(), self, "entrada")
            self.grid.place_agent(entrada, pos)

    def _crear_personas(self, num):
        for i in range(num):
            estado = 'E' if i == 0 else 'S'  # Uno expuesto inicial
            virus = self.virus_covid if estado == 'E' else None
            agente = Persona(self.next_id(), self, virus=virus)
            agente.estado = estado
            self.schedule.add(agente)
            while True:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                if not any(isinstance(a, ObjetoFijo) for a in self.grid.get_cell_list_contents([(x, y)])):
                    self.grid.place_agent(agente, (x, y))
                    break

    def contar_por_estado(self, estado):
        return sum(1 for a in self.schedule.agents if isinstance(a, Persona) and a.estado == estado)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    def next_id(self):
        self.next_id_val += 1
        return self.next_id_val