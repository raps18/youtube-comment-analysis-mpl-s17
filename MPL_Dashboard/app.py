import streamlit as st

# ===============================
# KONFIGURASI DASHBOARD
# ===============================

st.set_page_config(
    page_title="Dashboard Analisis Komentar YouTube MPL Indonesia Season 17",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# HEADER
# ===============================

st.title("🎮 Dashboard Analisis Komentar YouTube MPL Indonesia Season 17")

st.markdown("""
Dashboard ini digunakan untuk menampilkan hasil penelitian analisis komentar YouTube
**MPL Indonesia Season 17** menggunakan:

- Naive Bayes
- Support Vector Machine (SVM)
- BERTopic
- Social Network Analysis (SNA)

Silakan pilih menu pada sidebar untuk melihat hasil analisis.
""")

st.info("📌 Gunakan menu di sidebar sebelah kiri untuk berpindah halaman.")