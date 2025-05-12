from mesa import Agent

class Persona(Agent):
    def __init__(self, unique_id, model, virus=None):
        super().__init__(unique_id, model)
        self.estado = "S"
        self.virus = None
        self.tiempo_infeccion = 0

        if virus:
            self.infectar(virus)

    def infectar(self, virus):
        self.estado = "E"
        self.virus = virus
        self.tiempo_infeccion = 0

    def step(self):
        if self.estado in ["E", "I"]:
            self.tiempo_infeccion += 1

            if self.estado == "E" and self.tiempo_infeccion >= self.virus.duracion_incubacion:
                self.estado = "I"
                self.tiempo_infeccion = 0

            elif self.estado == "I":
                vecinos = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False)
                for v in vecinos:
                    if v.estado == "S" and self.random.random() < self.virus.prob_contagio:
                        v.infectar(self.virus)

                if self.tiempo_infeccion >= self.virus.duracion_infeccion:
                    self.estado = "D" if self.random.random() < self.virus.prob_muerte else "R"
                    self.virus = None
