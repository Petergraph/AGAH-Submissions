import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Feste Parameter
row_sep = 3.0         # Abstand zwischen den Reihen (Typen)
vert_offset = 0.8     # Abstand Unterkategorien (<31/>31 Tage)
title_margin = 10     # Abstand des Titels nach unten
box_spacing = 0.3     # Abstand zwischen den Boxen

# Typen (entspricht types-DataFrame)
types = [
    {
        "name": "Erstanwendungs-\nstudien 10",
        "fill": "#D2B4DE",
        "y": 1 + row_sep
    },
    {
        "name": "klassische PK-\nStudien 30",
        "fill": "#AED6F1",
        "y": 1
    }
]

# Werte für Kategorien
vals = {
    "a": [2, 4],    # <31 Tage
    "b": [8, 26],   # >31 Tage
    "c": [46, 44],  # Tage ab Validierung
    "e": [2, 12],   # Keine Validierungsprobleme
    "d": [20, 13]   # Anzahl Rückfragen
}

height = 0.8
box_width = 1.2

# Knoten erstellen
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
            "width": box_width,
            "height": height
        }
        node["xmin"] = node["x"] - node["width"]/2
        node["xmax"] = node["x"] + node["width"]/2
        node["ymin"] = node["y"] - node["height"]/2
        node["ymax"] = node["y"] + node["height"]/2
        nodes.append(node)

# Plot anlegen
fig, ax = plt.subplots(figsize=(12, 8))

# Boxen zeichnen
for node in nodes:
    rect = Rectangle(
        (node["xmin"], node["ymin"]),
        node["width"], node["height"],
        facecolor=node["fill"],
        edgecolor="black",
        linewidth=0.8
    )
    ax.add_patch(rect)
    ax.text(
        node["x"], node["y"], node["label"],
        ha="center", va="center",
        fontsize=11, wrap=True
    )

# Titel
plt.title("FIH vs PK-Studien", fontsize=20, pad=title_margin)

# Achsen anpassen
ax.set_xlim(0.5, 5.5)
ymin = min(node["ymin"] for node in nodes) - 0.5
ymax = max(node["ymax"] for node in nodes) + 0.5
ax.set_ylim(ymin, ymax)
ax.axis("off")
plt.tight_layout()

# Direkt als SVG speichern
plt.savefig("studien_design.svg", format="svg", bbox_inches="tight")

# Optional: anzeigen
plt.show()

