from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from agents.persona import Persona
from agents.objeto_fijo import ObjetoFijo
from agents.objeto_visual import ZonaVisual
from agents.virus import Virus

class UniversidadCOVIDModel(Model):
    def __init__(self, num_personas=10, grid_width=300, grid_height=300, duracion_simulacion=300):
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
        self.zonas = {}


        self._crear_zonas(grid_width, grid_height)
        self._crear_personas(num_personas)


    def _crear_zonas(self, width, height):
        print("Creando zonas en el grid...")

        # Paredes: borde del grid
        # Crear paredes solo una vez por celda (evita duplicados en esquinas)
        for x in range(width):
            self.grid.place_agent(ObjetoFijo(self.next_id(), self, "pared"), (x, 0))  # Borde superior
            self.grid.place_agent(ObjetoFijo(self.next_id(), self, "pared"), (x, height - 1))  # Borde inferior
        for y in range(1, height - 1):
            self.grid.place_agent(ObjetoFijo(self.next_id(), self, "pared"), (0, y))  # Borde izquierdo
            self.grid.place_agent(ObjetoFijo(self.next_id(), self, "pared"), (width - 1, y))  # Borde derecho

        # Aula: arriba izquierda (x: 0-18, y: 0-17)
        for x in range(0, 19):
            for y in range(0, 18):
                self.zonas[(x, y)] = "aula"
                self.grid.place_agent(ZonaVisual(self.next_id(), self, "aula"), (x, y))

        # Cafetería: arriba derecha (x: 19-39, y: 0-17)
        for x in range(19, 40):
            for y in range(0, 18):
                self.zonas[(x, y)] = "cafeteria"
                self.grid.place_agent(ZonaVisual(self.next_id(), self, "cafeteria"), (x, y))

        # Aula Magna: abajo (x: 0-39, y: 18-39)
        for x in range(0, 40):
            for y in range(18, 40):
                self.zonas[(x, y)] = "aula_magna"
                self.grid.place_agent(ZonaVisual(self.next_id(), self, "aula_magna"), (x, y))

        # Pared vertical interna entre Aula y Cafetería (x=19, y=0-17), dejando hueco de puerta (y=9-11)
        for y in range(0, 18):
            if y not in (9, 10, 11):  # Deja espacio para una "puerta"
                self.grid.place_agent(ObjetoFijo(self.next_id(), self, "pared"), (19, y))

        # Pared horizontal interna entre zonas superiores y Aula Magna (y=18, x=0-39), dejando hueco de puerta (x=28-30)
        for x in range(0, 40):
            if x not in (28, 29, 30):  # Deja espacio para una "puerta"
                self.grid.place_agent(ObjetoFijo(self.next_id(), self, "pared"), (x, 18))

        print("Zonas creadas según el plano.")


    def _crear_personas(self, num):
        print(f"Creando {num} personas en el modelo...")

        # Solo celdas que pertenecen a una zona (habitaciones)
        celdas_zona = list(self.zonas.keys())

        if len(celdas_zona) < num:
            raise ValueError("No hay suficientes celdas en las habitaciones para colocar todas las personas.")

        self.random.shuffle(celdas_zona)

        for i in range(num):
            estado = 'I' if i == 0 else 'S'
            virus = self.virus_covid if estado == 'I' else None
            agente = Persona(self.next_id(), self, virus=virus)
            agente.estado = estado
            self.schedule.add(agente)

            # Elegir una celda libre en zona y colocar al agente
            x, y = celdas_zona.pop()
            self.grid.place_agent(agente, (x, y))


    def contar_por_estado(self, estado):
        return sum(1 for a in self.schedule.agents if isinstance(a, Persona) and a.estado == estado)


    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)


    def next_id(self):
        self.next_id_val += 1
        return self.next_id_val