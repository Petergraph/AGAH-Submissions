import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(layout="wide")

st.sidebar.title("Einstellungen")
row_sep = st.sidebar.slider("Abstand zwischen den Reihen (Typen):", 0.5, 5.0, 3.0, 0.1)
vert_offset = st.sidebar.slider("Abstand Unterkategorien (<31/>31 Tage):", 0.1, 2.0, 0.8, 0.1)

# Parameter
height = 0.8
box_width = 1.2

# Typen definieren
types = pd.DataFrame({
    "id": [1, 2],
    "name": ["Erstanwendungs-\nstudien 10", "klassische PK-\nStudien 30"],
    "fill": ["#D2B4DE", "#AED6F1"],
    "y": [1 + row_sep, 1]
})

# Werte
vals = {
    "a": [2, 4],
    "b": [8, 26],
    "c": [46, 44],
    "e": [2, 12],
    "d": [20, 13]
}

# Boxen erstellen
nodes = []
edges = []

for i, row in types.iterrows():
    y0 = row["y"]
    fill = row["fill"]

    x_vals = [1, 2, 2, 3, 4, 5]
    y_offsets = [
        y0,
        y0 + vert_offset,
        y0 - vert_offset,
        y0,
        y0,
        y0
    ]
    labels = [
        row["name"],
        f"< 31 Tage\n{vals['a'][i]}",
        f"> 31 Tage\n{vals['b'][i]}",
        f"Tage ab Validierung\n{vals['c'][i]}",
        f"Keine\nValidierungsprobleme\n{vals['e'][i]}",
        f"Anzahl Rückfragen\n{vals['d'][i]}"
    ]

    for x, y, label in zip(x_vals, y_offsets, labels):
        nodes.append({
            "x": x,
            "y": y,
            "label": label,
            "fill": fill
        })

    # Kanten definieren
    edges += [
        ((1, y0), (2, y0 + vert_offset)),
        ((1, y0), (2, y0 - vert_offset)),
        ((2, y0 + vert_offset), (3, y0)),
        ((2, y0 - vert_offset), (3, y0)),
        ((3, y0), (4, y0)),
        ((4, y0), (5, y0)),
    ]

# Plot
fig, ax = plt.subplots(figsize=(10, 6))

# Boxen zeichnen
for node in nodes:
    rect = patches.FancyBboxPatch(
        (node["x"] - box_width / 2, node["y"] - height / 2),
        box_width, height,
        boxstyle="round,pad=0.02",
        linewidth=1,
        edgecolor='black',
        facecolor=node["fill"]
    )
    ax.add_patch(rect)
    ax.text(node["x"], node["y"], node["label"],
            ha="center", va="center", fontsize=10)

# Kanten zeichnen
for (x0, y0), (x1, y1) in edges:
    ax.annotate("",
        xy=(x1, y1), xytext=(x0, y0),
        arrowprops=dict(arrowstyle="->", lw=1.2)
    )

ax.set_xlim(0.5, 5.5)
ax.set_ylim(0, max(types["y"]) + 1.5)  # genug Platz nach oben
ax.set_aspect('equal')
ax.axis('off')

st.pyplot(fig)

