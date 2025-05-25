from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from agents.persona import Persona
from agents.objeto_fijo import ObjetoFijo
from virus import Virus

class UniversidadCOVIDModel(Model):
    def __init__(self, num_personas=600, grid_width=30, grid_height=20, duracion_simulacion=300):
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
        self.virus_covid = Virus("COVID-19", prob_contagio=0.65, duracion_incubacion=300, duracion_infeccion=300, prob_muerte=0)
        self.next_id_val = 0

        self._crear_zonas(grid_width, grid_height)
        self._crear_personas(num_personas)

    def _crear_zonas(self, width, height):
        # Cafetería: zona izquierda
        for x in range(0, 10):
            for y in range(0, height):
                cafeteria = ObjetoFijo(self.next_id(), self, "cafeteria")
                self.grid.place_agent(cafeteria, (x, y))
        # Aula: zona central
        for x in range(10, 20):
            for y in range(0, height):
                aula = ObjetoFijo(self.next_id(), self, "aula")
                self.grid.place_agent(aula, (x, y))
        # Conversatorio: zona derecha
        for x in range(20, width):
            for y in range(0, height):
                conversatorio = ObjetoFijo(self.next_id(), self, "conversatorio")
                self.grid.place_agent(conversatorio, (x, y))

    def _crear_personas(self, num):
        for i in range(num):
            estado = 'E' if i == 0 else 'S'
            virus = self.virus_covid if estado == 'E' else None
            agente = Persona(self.next_id(), self, virus=virus)
            agente.estado = estado
            self.schedule.add(agente)
            while True:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                # Solo colocar personas en celdas sin otro agente fijo
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