import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import io
import streamlit.components.v1 as components

# Streamlit-Page-Config
st.set_page_config(layout="wide")
st.title("FIH vs PK-Studien")

# Feste Parameter
row_sep = 3.0         # Abstand zwischen den Reihen (Typen)
vert_offset = 0.8     # Abstand Unterkategorien (<31/>31 Tage)
title_margin = 10     # Abstand des Titels nach unten
box_spacing = 0.3     # Abstand zwischen den Boxen
box_width = 1.2
height = 0.8

# Typen-Daten
types = [
    {"name": "Erstanwendungs-
studien 10", "fill": "#D2B4DE", "y": 1 + row_sep},
    {"name": "klassische PK-
Studien 30",    "fill": "#AED6F1", "y": 1}
]

# Werte für Kategorien
vals = {
    "a": [2, 4],    # <31 Tage
    "b": [8, 26],   # >31 Tage
    "c": [46, 44],  # Tage ab Validierung
    "e": [2, 12],   # Keine Validierungsprobleme
    "d": [20, 13]   # Anzahl Rückfragen
}

# Knoten generieren
nodes = []
for i, typ in enumerate(types):
    y0 = typ["y"]
    x_vals = [1, 2, 2, 3, 4, 5]
    y_offsets = [
        y0,
        y0 + vert_offset + box_spacing,
        y0 - vert_offset - box_spacing,
        y0, y0, y0
    ]
    labels = [
        typ["name"],
        f"< 31 Tage
{vals['a'][i]}",
        f"> 31 Tage
{vals['b'][i]}",
        f"Tage ab Validierung
{vals['c'][i]}",
        f"Keine
Validierungsprobleme
{vals['e'][i]}",
        f"Anzahl Rückfragen
{vals['d'][i]}"
    ]
    for x, y, label in zip(x_vals, y_offsets, labels):
        nodes.append({
            "x": x, "y": y,
            "label": label, "fill": typ["fill"],
            "xmin": x - box_width/2,
            "xmax": x + box_width/2,
            "ymin": y - height/2,
            "ymax": y + height/2
        })

# Plot erstellen
fig, ax = plt.subplots(figsize=(12, 8))
for node in nodes:
    rect = Rectangle((node["xmin"], node["ymin"]), box_width, height,
                     facecolor=node["fill"], edgecolor="black", linewidth=0.8)
    ax.add_patch(rect)
    ax.text(node["x"], node["y"], node["label"], ha="center", va="center",
            fontsize=11, wrap=True)

# Titel und Achsen
t = fig.suptitle("FIH vs PK-Studien", fontsize=20)
t.set_y(1 - title_margin/(fig.get_figheight()*fig.dpi))
ax.set_xlim(0.5, 5.5)
ymin = min(n['ymin'] for n in nodes) - 0.5
ymax = max(n['ymax'] for n in nodes) + 0.5
ax.set_ylim(ymin, ymax)
ax.axis("off")
plt.tight_layout()

# SVG in-memory erzeugen
buffer = io.BytesIO()
fig.savefig(buffer, format='svg', bbox_inches='tight')
svg_data = buffer.getvalue().decode('utf-8')

# SVG inline anzeigen
components.html(svg_data, height=600)

# Download-Button fürs SVG
st.download_button(
    label="SVG herunterladen",
    data=svg_data,
    file_name="studien_design.svg",
    mime="image/svg+xml"
)
```python
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Streamlit-Page-Config
st.set_page_config(layout="wide")
st.title("FIH vs PK-Studien")

# Feste Parameter
row_sep = 3.0         # Abstand zwischen den Reihen (Typen)
vert_offset = 0.8     # Abstand Unterkategorien (<31/>31 Tage)
title_margin = 10     # Abstand des Titels nach unten
box_spacing = 0.3     # Abstand zwischen den Boxen
box_width = 1.2
height = 0.8

# Typen-Daten
types = [
    {"name": "Erstanwendungs-\nstudien 10", "fill": "#D2B4DE", "y": 1 + row_sep},
    {"name": "klassische PK-\nStudien 30", "fill": "#AED6F1", "y": 1}
]

# Werte für Kategorien
vals = {
    "a": [2, 4],    # <31 Tage
    "b": [8, 26],   # >31 Tage
    "c": [46, 44],  # Tage ab Validierung
    "e": [2, 12],   # Keine Validierungsprobleme
    "d": [20, 13]   # Anzahl Rückfragen
}

# Knoten generieren
nodes = []
for i, typ in enumerate(types):
    y0 = typ["y"]
    x_vals = [1, 2, 2, 3, 4, 5]
    y_offsets = [
        y0,
        y0 + vert_offset + box_spacing,
        y0 - vert_offset - box_spacing,
        y0,
        y0,
        y0
    ]
    labels = [
        typ["name"],
        f"< 31 Tage\n{vals['a'][i]}",
        f"> 31 Tage\n{vals['b'][i]}",
        f"Tage ab Validierung\n{vals['c'][i]}",
        f"Keine\nValidierungsprobleme\n{vals['e'][i]}",
        f"Anzahl Rückfragen\n{vals['d'][i]}"
    ]
    for x, y, label in zip(x_vals, y_offsets, labels):
        node = {
            "x": x,
            "y": y,
            "label": label,
            "fill": typ["fill"],
            "xmin": x - box_width/2,
            "xmax": x + box_width/2,
            "ymin": y - height/2,
            "ymax": y + height/2
        }
        nodes.append(node)

# Plot anlegen
fig, ax = plt.subplots(figsize=(12, 8))
for node in nodes:
    rect = Rectangle(
        (node["xmin"], node["ymin"]),
        box_width, height,
        facecolor=node["fill"], edgecolor="black", linewidth=0.8
    )
    ax.add_patch(rect)
    ax.text(
        node["x"], node["y"], node["label"],
        ha="center", va="center", fontsize=11, wrap=True
    )

# Titel und Achsen
t = fig.suptitle("FIH vs PK-Studien", fontsize=20)
# Abstand für Titel nach unten anpassen
t.set_y(1 - title_margin / (fig.get_figheight() * fig.dpi))
ax.set_xlim(0.5, 5.5)
ymin = min(node["ymin"] for node in nodes) - 0.5
ymax = max(node["ymax"] for node in nodes) + 0.5
ax.set_ylim(ymin, ymax)
ax.axis("off")
plt.tight_layout()

# Darstellung in Streamlit
st.pyplot(fig)
