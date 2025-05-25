from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from models.modelo import EpidemiaModel
from agents.persona import Persona
from virus import Virus

# (1) Definir cómo se dibuja cada agente
def agent_portrayal(agent):
    if agent.estado == "S":
        color = "blue"
    elif agent.estado == "E":
        color = "orange"
    elif agent.estado == "I":
        color = "red"
    elif agent.estado == "R":
        color = "green"
    elif agent.estado == "D":
        color = "black"
    else:
        color = "gray"

    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "r": 0.5,
        "Color": color,
        "Layer": 0
    }
    return portrayal

# (2) Crear los módulos de visualización
grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)
chart = ChartModule([
    {"Label": "S", "Color": "blue"},
    {"Label": "E", "Color": "orange"},
    {"Label": "I", "Color": "red"},
    {"Label": "R", "Color": "green"},
    {"Label": "D", "Color": "black"},
])

# (3) Virus de prueba (podés reemplazar con tu lógica de selección)
virus = Virus(
    nombre="COVID-19",
    prob_contagio=0.25,
    duracion_incubacion=3,
    duracion_infeccion=10,
    prob_muerte=0.02
)

# (4) Crear el servidor
server = ModularServer(
    EpidemiaModel,
    [grid, chart],
    "Simulación Epidemia",
    {"N": 200, "width": 20, "height": 20, "virus": virus}
)

server.port = 8521

# (5) Ejecutar y cerrar correctamente
if __name__ == "__main__":
    try:
        print(f"Servidor iniciado en http://localhost:{server.port}")
        server.launch()
    except KeyboardInterrupt:
        print("Servidor interrumpido con Ctrl+C. Cerrando socket...")
        import sys
        sys.exit(0)
