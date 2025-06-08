from models.model_universidad import UniversidadCOVIDModel
from agents.persona import Persona

modelo = UniversidadCOVIDModel(num_personas=200, grid_width=40, grid_height=40, duracion_simulacion=300, num_infectados=3)
for i in range(modelo.duracion_simulacion):
    modelo.step()
estados = {"S": 0, "E": 0, "I": 0}
for agente in modelo.schedule.agents:
    if isinstance(agente, Persona):
        estados[agente.estado] += 1
print(estados)