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
    "Simulación UAA - COVID",
    {
        "num_personas": 200,
        "num_infectados": 3,
        "grid_width": grid_width,
        "grid_height": grid_height,
        "duracion_simulacion": 300 # Duración en pasos / 1 paso = 1 minuto
    }
)


server.max_steps = 300  # Duración máxima de la simulación en pasos
server.description = """Simulación de propagación de COVID-19 en la Universidad Atlantida Argentina, con zonas específicas y 
agentes que representan personas y objetos fijos. El modelo incluye un virus con características específicas y permite observar 
la evolución de la infección a lo largo del tiempo.

La simulación muestra cómo las personas interactúan en diferentes zonas (aula, cafetería, aula magna) y cómo se propaga el virus
entre ellas. Los estados de las personas son: Sano (S), Expuesto (E) e Infectado (I).

Desarrollado por Sanabria Sebastian, Ortiz Isaias y Teta Gustavo, para la materia de Teoria de Modelos y Sistemas en la Universidad Atlantida Argentina.
"""

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