{\rtf1\ansi\ansicpg1252\deff0\nouicompat\deflang1031{\fonttbl{\f0\fnil\fcharset0 Calibri;}}
{\*\generator Riched20 10.0.19041}\viewkind4\uc1 
\pard\sa200\sl276\slmult1\f0\fs22\lang7 import streamlit as st\par
import plotly.graph_objects as go\par
\par
st.set_page_config(layout="wide")\par
\par
st.title("Interaktives Flow-Chart: Erstanwendungen & PK-Studien")\par
\par
# Seitenleiste mit Reglern\par
with st.sidebar:\par
    st.header("Einstellungen")\par
    row_sep = st.slider("Abstand zwischen Reihen", 0.5, 5.0, 3.0, step=0.1)\par
    vert_offset = st.slider("Abstand <31 / >31 Tage", 0.1, 2.0, 0.8, step=0.1)\par
    box_width = st.slider("Box-Breite", 0.5, 2.0, 1.2, step=0.1)\par
    box_height = st.slider("Box-H\'f6he", 0.3, 2.0, 0.8, step=0.1)\par
    font_size = st.slider("Schriftgr\'f6\'dfe", 8, 24, 12)\par
    title_margin = st.slider("Titelabstand", 0, 50, 10)\par
\par
# Daten f\'fcr Typen\par
types = [\par
    \{"name": "Erstanwendungs-\\nstudien 10", "fill": "#D2B4DE", "y": 1 + row_sep\},\par
    \{"name": "klassische PK-\\nStudien 30", "fill": "#AED6F1", "y": 1\}\par
]\par
\par
vals = \{\par
    "a": [2, 4],    # <31 Tage\par
    "b": [8, 26],   # >31 Tage\par
    "c": [46, 44],  # Tage ab Validierung\par
    "e": [2, 12],   # Keine Validierungsprobleme\par
    "d": [20, 13]   # R\'fcckfragen\par
\}\par
\par
fig = go.Figure()\par
\par
for i, typ in enumerate(types):\par
    y0 = typ["y"]\par
    x_vals = [1, 2, 2, 3, 4, 5]\par
    y_vals = [\par
        y0,\par
        y0 + vert_offset,\par
        y0 - vert_offset,\par
        y0,\par
        y0,\par
        y0\par
    ]\par
    labels = [\par
        typ["name"],\par
        f"< 31 Tage\\n\{vals['a'][i]\}",\par
        f"> 31 Tage\\n\{vals['b'][i]\}",\par
        f"Tage ab Validierung\\n\{vals['c'][i]\}",\par
        f"Keine Validierungsprobleme\\n\{vals['e'][i]\}",\par
        f"Anzahl R\'fcckfragen\\n\{vals['d'][i]\}"\par
    ]\par
\par
    for x, y, label in zip(x_vals, y_vals, labels):\par
        fig.add_shape(\par
            type="rect",\par
            x0=x - box_width/2,\par
            x1=x + box_width/2,\par
            y0=y - box_height/2,\par
            y1=y + box_height/2,\par
            line=dict(color="black"),\par
            fillcolor=typ["fill"]\par
        )\par
        fig.add_annotation(\par
            x=x, y=y,\par
            text=label.replace("\\n", "<br>"),\par
            showarrow=False,\par
            font=dict(size=font_size),\par
            align="center"\par
        )\par
\par
    # Linien (Pfeile)\par
    fig.add_annotation(x=2, y=y0 + vert_offset, ax=1, ay=y0,\par
                       showarrow=True, arrowhead=2)\par
    fig.add_annotation(x=2, y=y0 - vert_offset, ax=1, ay=y0,\par
                       showarrow=True, arrowhead=2)\par
    fig.add_annotation(x=3, y=y0, ax=2, ay=y0 + vert_offset,\par
                       showarrow=True, arrowhead=2)\par
    fig.add_annotation(x=3, y=y0, ax=2, ay=y0 - vert_offset,\par
                       showarrow=True, arrowhead=2)\par
    fig.add_annotation(x=4, y=y0, ax=3, ay=y0,\par
                       showarrow=True, arrowhead=2)\par
    fig.add_annotation(x=5, y=y0, ax=4, ay=y0,\par
                       showarrow=True, arrowhead=2)\par
\par
# Layout\par
fig.update_layout(\par
    height=600,\par
    margin=dict(t=title_margin+40, b=20, l=20, r=20),\par
    xaxis=dict(visible=False),\par
    yaxis=dict(visible=False),\par
    showlegend=False,\par
    title=dict(\par
        text="Studien-Design",\par
        font=dict(size=24),\par
        x=0.5,\par
        y=1,\par
        xanchor="center",\par
        yanchor="top"\par
    )\par
)\par
\par
st.plotly_chart(fig, use_container_width=True)\par
}
 