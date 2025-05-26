from models.model_universidad import UniversidadCOVIDModel
from agents.persona import Persona

modelo = UniversidadCOVIDModel(num_personas=100, grid_width=40, grid_height=40, duracion_simulacion=300)
for i in range(300):
    modelo.step()
estados = {"Sano": 0, "Expuesto": 0, "Infectado": 0}
for agente in modelo.schedule.agents:
    if isinstance(agente, Persona):
        estados[agente.estado] += 1
print(estados)