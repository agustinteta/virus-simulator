from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from models.model_universidad import UniversidadCOVIDModel
from agents.persona import Persona
from agents.objeto_fijo import ObjetoFijo

def agent_portrayal(agent):
    if isinstance(agent, ObjetoFijo):
        color = {
            "cafeteria": "lightblue",
            "aula": "lightgreen",
            "conversatorio": "orange"
        }.get(agent.tipo, "black")

        return {
            "Shape": "rect",
            "Color": color,
            "Filled": "true",
            "Layer": 0,
            "w": 1,
            "h": 1
        }

    if isinstance(agent, Persona):
        color = {
            "S": "gray",
            "E": "yellow",
            "I": "red"
        }.get(agent.estado, "blue")

        return {
            "Shape": "circle",
            "Color": color,
            "Filled": "true",
            "Layer": 1,
            "r": 0.5
        }

# Dimensiones del grid y visualización
grid_width, grid_height = 30, 20
pixel_width, pixel_height = 600, 400

grid = CanvasGrid(agent_portrayal, grid_width, grid_height, pixel_width, pixel_height)

# Gráfico de evolución de la infección
chart = ChartModule(
    [
        {"Label": "Sano", "Color": "gray"},
        {"Label": "Expuesto", "Color": "yellow"},
        {"Label": "Infectado", "Color": "red"},
    ],
    data_collector_name='datacollector'
)

# Configuración del servidor
server = ModularServer(
    UniversidadCOVIDModel,
    [grid, chart],
    "Simulación Universidad UAA COVID",
    {
        "num_personas": 600,
        "grid_width": grid_width,
        "grid_height": grid_height,
        "duracion_simulacion": 300 # Duración en pasos / 1 paso = 1 minuto
    }
)

server.port = 8521  # Puerto de ejecución

if __name__ == "__main__":
    try:
        print(f"Servidor iniciado en http://localhost:{server.port}")
        server.launch()
    except KeyboardInterrupt:
        print("Servidor interrumpido con Ctrl+C. Cerrando socket...")
        import sys
        sys.exit(0)