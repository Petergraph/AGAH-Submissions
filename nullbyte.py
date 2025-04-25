import streamlit as st
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("Interaktives Flow-Chart: Erstanwendungen & PK-Studien")

# Seitenleiste mit Reglern
with st.sidebar:
    st.header("Einstellungen")
    row_sep = st.slider("Abstand zwischen Reihen", 0.5, 5.0, 3.0, step=0.1)
    vert_offset = st.slider("Abstand <31 / >31 Tage", 0.1, 2.0, 0.8, step=0.1)
    box_width = st.slider("Box-Breite", 0.5, 2.0, 1.2, step=0.1)
    box_height = st.slider("Box-Höhe", 0.3, 2.0, 0.8, step=0.1)
    font_size = st.slider("Schriftgröße", 8, 24, 12)
    title_margin = st.slider("Titelabstand", 0, 50, 10)

# Daten für Typen
types = [
    {"name": "Erstanwendungs-\nstudien 10", "fill": "#D2B4DE", "y": 1 + row_sep},
    {"name": "klassische PK-\nStudien 30", "fill": "#AED6F1", "y": 1}
]

vals = {
    "a": [2, 4],    # <31 Tage
    "b": [8, 26],   # >31 Tage
    "c": [46, 44],  # Tage ab Validierung
    "e": [2, 12],   # Keine Validierungsprobleme
    "d": [20, 13]   # Rückfragen
}

fig = go.Figure()

for i, typ in enumerate(types):
    y0 = typ["y"]
    x_vals = [1, 2, 2, 3, 4, 5]
    y_vals = [
        y0,
        y0 + vert_offset,
        y0 - vert_offset,
        y0,
        y0,
        y0
    ]
    labels = [
        typ["name"],
        f"< 31 Tage\n{vals['a'][i]}",
        f"> 31 Tage\n{vals['b'][i]}",
        f"Tage ab Validierung\n{vals['c'][i]}",
        f"Keine Validierungsprobleme\n{vals['e'][i]}",
        f"Anzahl Rückfragen\n{vals['d'][i]}"
    ]

    for x, y, label in zip(x_vals, y_vals, labels):
        fig.add_shape(
            type="rect",
            x0=x - box_width/2,
            x1=x + box_width/2,
            y0=y - box_height/2,
            y1=y + box_height/2,
            line=dict(color="black"),
            fillcolor=typ["fill"]
        )
        fig.add_annotation(
            x=x, y=y,
            text=label.replace("\n", "<br>"),
            showarrow=False,
            font=dict(size=font_size),
            align="center"
        )

    # Linien (Pfeile)
    fig.add_annotation(x=2, y=y0 + vert_offset, ax=1, ay=y0,
                       showarrow=True, arrowhead=2)
    fig.add_annotation(x=2, y=y0 - vert_offset, ax=1, ay=y0,
                       showarrow=True, arrowhead=2)
    fig.add_annotation(x=3, y=y0, ax=2, ay=y0 + vert_offset,
                       showarrow=True, arrowhead=2)
    fig.add_annotation(x=3, y=y0, ax=2, ay=y0 - vert_offset,
                       showarrow=True, arrowhead=2)
    fig.add_annotation(x=4, y=y0, ax=3, ay=y0,
                       showarrow=True, arrowhead=2)
    fig.add_annotation(x=5, y=y0, ax=4, ay=y0,
                       showarrow=True, arrowhead=2)

# Layout
fig.update_layout(
    height=600,
    margin=dict(t=title_margin+40, b=20, l=20, r=20),
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    showlegend=False,
    title=dict(
        text="Studien-Design",
        font=dict(size=24),
        x=0.5,
        y=1,
        xanchor="center",
        yanchor="top"
    )
)

st.plotly_chart(fig, use_container_width=True)
