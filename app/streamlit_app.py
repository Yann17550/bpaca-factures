import pandas as pd
import streamlit as st

from services.supabase_service import get_operations


st.set_page_config(
    page_title="BPACA Factures",
    layout="wide"
)

st.title("📊 BPACA Factures")

operations = get_operations()

df = pd.DataFrame(operations)

st.metric(
    "Nombre d'opérations",
    len(df)
)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)