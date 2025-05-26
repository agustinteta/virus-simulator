# Simulador de Virus en Universidad

Este proyecto simula la propagación de un virus en una población dentro de una universidad, utilizando el framework [Mesa](https://mesa.readthedocs.io/en/stable/). El modelo permite observar cómo se comporta la infección en diferentes espacios (aula, cafetería, aula magna) y bajo distintas condiciones.

## Descripción

- **Espacios simulados:** Aula, Cafetería y Aula Magna, conectados por paredes y puertas internas.
- **Agentes:** Personas (alumnos/docentes) que se mueven entre las zonas y pueden contagiarse.
- **Visualización:** El entorno y los agentes se muestran en tiempo real, diferenciando zonas y estados de salud.
- **Personalización:** Puedes ajustar el tamaño de la población, dimensiones del grid y duración de la simulación.

## Requisitos

- Python 3.8+
- Mesa (`pip install mesa`)

## Instalación

```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

## Uso

### Para correr el backend (solo simulación, sin visualización):

```bash
python main.py
```

### Para visualizar la simulación en el navegador:

```bash
python -m visualization.server_universidad
```

Luego abre tu navegador en [http://localhost:8521](http://localhost:8521).

## Estructura del proyecto

- `agents/` — Definición de los agentes (personas, paredes, zonas visuales).
- `models/` — Lógica del modelo y creación de zonas.
- `visualization/` — Servidor y visualización interactiva con Mesa.
- `requirements.txt` — Dependencias del proyecto.

## Personalización

Puedes modificar los parámetros de la simulación (cantidad de personas, tamaño del grid, duración, etc.) directamente en el archivo `visualization/server_universidad.py` o en el modelo.

## Créditos

Proyecto desarrollado por Ortiz Isaias, Sanabria Sebastias y Teta Agustin, para la materia Teoría de Sistemas y Modelos.

---

¡Explora cómo se propaga un virus en diferentes escenarios universitarios y experimenta con tus propios parámetros!