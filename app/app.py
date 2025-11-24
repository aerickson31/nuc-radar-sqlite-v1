import streamlit as st

st.set_page_config(
    page_title="NucRadar v1",
    layout="wide",
)

st.title("NucRadar v1 — Advanced Fission Startup Radar")

st.markdown(
    """        This is a local prototype of a "Bloomberg for nuclear" dashboard.

    Use the sidebar to:
    - View the overview dashboard
    - Drill into a specific company
    - Browse the raw events log
    - Manually add events for testing

    Data is stored in a local SQLite file (`nuc_radar.sqlite`) in this folder.
    """
)
