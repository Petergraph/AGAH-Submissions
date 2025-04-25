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
dnodes = []
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
    rect = Rectangle(
        (node["xmin"], node["ymin"]),
        box_width, height,
        facecolor=node["fill"],
        edgecolor="black",
        linewidth=0.8
    )
    ax.add_patch(rect)
    ax.text(
        node["x"], node["y"], node["label"],
        ha="center", va="center", fontsize=11, wrap=True
    )

# Titel und Achsen
tplt = fig.suptitle("FIH vs PK-Studien", fontsize=20)
plt.setp(tplt, y=1 - title_margin/fig.get_figheight()/fig.dpi)
ax.set_xlim(0.5, 5.5)
ymin = min(n['ymin'] for n in nodes) - 0.5
ymax = max(n['ymax'] for n in nodes) + 0.5
ax.set_ylim(ymin, ymax)
ax.axis('off')
plt.tight_layout()

# Anzeige in Streamlit
st.pyplot(fig)
```python
import streamlit as st
import requests
import datetime
import pandas as pd
from collections import defaultdict

st.set_page_config(layout="wide")
st.title("Neu registrierte Studien von ClinicalTrials.gov")

# --- Sidebar für Parameter ---
st.sidebar.header("Filter")
days = st.sidebar.slider(
    "Zeitraum (Tage zurück)",
    min_value=1,
    max_value=14,
    value=1
)
if st.sidebar.button("Aktualisieren"):
    st.experimental_rerun()

# --- Funktion zum Abrufen der Studien über API V1 ---
@st.cache_data(ttl=3600)
def fetch_new_studies(days: int):
    """
    Ruft alle Studien ab, deren "First Posted"-Datum in den letzten `days` Tagen liegt
    über die Version 1 API (study_fields endpoint).
    """
    today = datetime.date.today()
    start = today - datetime.timedelta(days=days)
    # Baue Suche mit RANGE und US-Datum
    search_range = f"AREA[FirstPosted]RANGE[{start.strftime('%m/%d/%Y')} TO {today.strftime('%m/%d/%Y')}]"  # Verwende 'TO' statt Komma für die V1 API
    params = {
        "expr": search_range,  # V1 API uses 'expr'
        "fields": "NCTId,Condition,FirstPosted,BriefTitle",
        "min_rnk": 1,
        "max_rnk": 10000,
        "fmt": "json"
    }
    try:
        r = requests.get(
            "https://clinicaltrials.gov/api/query/study_fields",
            params=params
        )
        r.raise_for_status()
        data = r.json()
        return data.get("StudyFieldsResponse", {}).get("StudyFields", [])
    except requests.HTTPError as e:
        st.error(f"Fehler beim Abrufen der Daten: {e}")
        return []

# --- Daten holen und gruppieren ---
with st.spinner("Hole Daten …"):
    studies = fetch_new_studies(days)

# Gruppierung nach Condition für V1 API Response
grouped = defaultdict(list)
for s in studies:
    nct = s.get("NCTId", [None])[0]
    date_fp = s.get("FirstPosted", [None])[0]
    title = s.get("BriefTitle", [""])[0]
    conditions = s.get("Condition", [])
    for cond in conditions:
        grouped[cond].append({
            "NCTId": nct,
            "Title": title,
            "FirstPosted": date_fp
        })

# --- Anzeige sortiert nach Anzahl Studien pro Condition ---
for cond, items in sorted(grouped.items(), key=lambda x: -len(x[1])):
    st.subheader(f"{cond} ({len(items)})")
    df = pd.DataFrame(items)
    st.dataframe(df, height=200)

