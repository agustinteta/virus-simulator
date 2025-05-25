from virus import Virus
from models.modelo import EpidemiaModel

virus_covid = Virus("COVID-19", prob_contagio=0.25, duracion_incubacion=3, duracion_infeccion=10, prob_muerte=0.02)
modelo = EpidemiaModel(N=100, width=10, height=10, virus=virus_covid)

for i in range(20):
    modelo.step()

estados = {"S": 0, "E": 0, "I": 0, "R": 0, "D": 0}
for agente in modelo.schedule.agents:
    estados[agente.estado] += 1

print(estados)
