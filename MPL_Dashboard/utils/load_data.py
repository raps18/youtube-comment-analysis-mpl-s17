import pandas as pd
import streamlit as st
from pathlib import Path

# Folder project
BASE_DIR = Path(__file__).resolve().parent.parent

# Folder data
DATA_PATH = BASE_DIR / "data"


@st.cache_data
def load_comments():

    file = DATA_PATH / "mpl_s17_toxic_labeledd.csv"

    st.write("Lokasi file:", file)

    if not file.exists():
        st.error(f"File tidak ditemukan:\n{file}")
        return pd.DataFrame()

    return pd.read_csv(file)


@st.cache_data
def load_bertopic():

    file = DATA_PATH / "hasil_klasterisasi_bertopic.csv"

    if not file.exists():
        st.error(f"File tidak ditemukan:\n{file}")
        return pd.DataFrame()

    return pd.read_csv(file)


@st.cache_data
def load_centrality():

    file = DATA_PATH / "hasil_centrality.csv"

    if not file.exists():
        st.error(f"File tidak ditemukan:\n{file}")
        return pd.DataFrame()

    return pd.read_csv(file)