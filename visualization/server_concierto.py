from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from model.model_concierto import ConciertoCOVIDModel
from agents.persona import Persona
from agents.objeto_fijo import ObjetoFijo

def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}

    if isinstance(agent, Persona):
        color = {
            "S": "blue",
            "E": "orange",
            "I": "red",
            "R": "green",
            "D": "black"
        }.get(agent.estado, "gray")
        portrayal["Color"] = color
        portrayal["Layer"] = 1
    elif isinstance(agent, ObjetoFijo):
        portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
        if agent.tipo == "escenario":
            portrayal["Color"] = "gray"
        elif agent.tipo == "entrada":
            portrayal["Color"] = "yellow"

    return portrayal

model_params = {
    "num_personas": UserSettableParameter('slider', "Cantidad de personas", 10000, 1000, 70000, 1000),
    "grid_width": UserSettableParameter('slider', "Ancho del estadio (m)", 105, 50, 150, 5),
    "grid_height": UserSettableParameter('slider', "Alto del estadio (m)", 75, 30, 100, 5),
    "duracion_simulacion": UserSettableParameter('slider', "Duración (minutos)", 150, 30, 300, 10),
}

grid = CanvasGrid(agent_portrayal, 105, 75, 1050, 750)
chart = ChartModule([
    {"Label": "Sano", "Color": "blue"},
    {"Label": "Expuesto", "Color": "orange"},
    {"Label": "Infectado", "Color": "red"},
])

server = ModularServer(
    ConciertoCOVIDModel,
    [grid, chart],
    "Simulación COVID-19 en Estadio Monumental",
    model_params
)
server.port = 8521

if __name__ == "__main__":
    try:
        print(f"Servidor iniciado en http://localhost:{server.port}")
        server.launch()
    except KeyboardInterrupt:
        print("Servidor interrumpido con Ctrl+C. Cerrando socket...")
        import sys
        sys.exit(0)