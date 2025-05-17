from mesa import Agent

class ObjetoFijo(Agent):
    def __init__(self, unique_id, model, tipo):
        super().__init__(unique_id, model)
        self.tipo = tipo