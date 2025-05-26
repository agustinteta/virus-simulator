from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from models.model_universidad import UniversidadCOVIDModel
from agents.persona import Persona
from agents.objeto_fijo import ObjetoFijo
from agents.objeto_visual import ZonaVisual


def agent_portrayal(agent):
    if isinstance(agent, ObjetoFijo):
        return {
            "Shape": "rect",
            "Color": "black",
            "Filled": "true",
            "Layer": 2,
            "w": 1,
            "h": 1
        }
    if isinstance(agent, ZonaVisual):
        colores = {
            "cafeteria": "lightblue",
            "aula": "lightgreen",
            "aula_magna": "orange"
        }
        color = colores.get(agent.tipo_zona, "white")
        return {
            "Shape": "rect",
            "Color": color,
            "Filled": "true",
            "Layer": 0,
            "w": 1,
            "h": 1
        }
    if isinstance(agent, Persona):
        colores = {
            "S": "gray",
            "E": "yellow",
            "I": "red"
        }
        color = colores.get(agent.estado, "blue")
        return {
            "Shape": "circle",
            "Color": color,
            "Filled": "true",
            "Layer": 1,
            "r": 0.5
        }

# Dimensiones del grid y visualización
print("Paso 1: Configurando el grid")
grid_width, grid_height = 40, 40
pixel_width, pixel_height = 600, 400

grid = CanvasGrid(agent_portrayal, grid_width, grid_height, pixel_width, pixel_height)

# Gráfico de evolución de la infección
print("Paso 2: Configurando el gráfico")
chart = ChartModule(
    [
        {"Label": "Sano", "Color": "gray"},
        {"Label": "Expuesto", "Color": "yellow"},
        {"Label": "Infectado", "Color": "red"},
    ],
    data_collector_name='datacollector'
)

# Configuración del servidor
print("Paso 3: Configurando el servidor")
server = ModularServer(
    UniversidadCOVIDModel,
    [grid, chart],
    "Simulación Universidad UAA COVID",
    {
        "num_personas": 100,
        "grid_width": grid_width,
        "grid_height": grid_height,
        "duracion_simulacion": 300 # Duración en pasos / 1 paso = 1 minuto
    }
)

print("Paso 4: Configurando el puerto del servidor")
server.port = 8521  # Puerto de ejecución

if __name__ == "__main__":
    try:
        print(f"Servidor iniciado en http://localhost:{server.port}")
        server.launch()
    except KeyboardInterrupt:
        print("Servidor interrumpido con Ctrl+C. Cerrando socket...")
        import sys
        sys.exit(0)