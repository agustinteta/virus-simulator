from mesa import Agent

class ZonaVisual(Agent):
    def __init__(self, unique_id, model, tipo_zona):
        super().__init__(unique_id, model)
        self.tipo_zona = tipo_zona

    def step(self):
        pass  # No hace nada