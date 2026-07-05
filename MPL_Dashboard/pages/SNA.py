import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

from utils.load_data import load_centrality

# ==========================================================
# CONFIG
# ==========================================================

st.set_page_config(
    page_title="Social Network Analysis",
    page_icon="🌐",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_PATH = BASE_DIR / "image"

# ==========================================================
# LOAD DATA
# ==========================================================

df = load_centrality()

if df.empty:
    st.error("Data Centrality tidak ditemukan.")
    st.stop()

# ==========================================================
# HEADER
# ==========================================================

st.title("🌐 Social Network Analysis (SNA)")

st.markdown("""
Halaman ini menampilkan hasil analisis jaringan sosial (Social Network Analysis)
berdasarkan interaksi komentar YouTube **MPL Indonesia Season 17**.

Analisis dilakukan menggunakan beberapa ukuran centrality untuk mengetahui
node atau pengguna yang paling berpengaruh dalam jaringan.
""")

st.divider()

# ==========================================================
# KPI
# ==========================================================

jumlah_node = len(df)

top_degree = df["Degree Centrality"].max()

top_closeness = df["Closeness Centrality"].max()

top_betweenness = df["Betweenness Centrality"].max()

top_eigen = df["Eigenvector Centrality"].max()

c1,c2,c3,c4,c5 = st.columns(5)

c1.metric(
    "👤 Total Node",
    jumlah_node
)

c2.metric(
    "📈 Degree",
    f"{top_degree:.4f}"
)

c3.metric(
    "📊 Closeness",
    f"{top_closeness:.4f}"
)

c4.metric(
    "🔀 Betweenness",
    f"{top_betweenness:.4f}"
)

c5.metric(
    "⭐ Eigenvector",
    f"{top_eigen:.4f}"
)

st.divider()

# ==========================================================
# NETWORK GRAPH
# ==========================================================

st.subheader("🌐 Visualisasi Jaringan")

network = IMAGE_PATH / "network_graph.png"

if network.exists():

    st.image(
        str(network),
        use_container_width=True
    )

else:

    st.warning(
        "network_graph.png tidak ditemukan pada folder image."
    )

st.divider()

# ==========================================================
# SEARCH NODE
# ==========================================================

st.subheader("🔍 Pencarian Node")

keyword = st.text_input(
    "Masukkan nama node"
)

if keyword:

    hasil = df[
        df["Node"].astype(str).str.contains(
            keyword,
            case=False,
            na=False
        )
    ]

    st.dataframe(
        hasil,
        use_container_width=True,
        hide_index=True
    )

st.divider()

# ==========================================================
# TOP 10 DEGREE CENTRALITY
# ==========================================================

st.subheader("📊 Top 10 Degree Centrality")

degree = (
    df.sort_values(
        by="Degree Centrality",
        ascending=False
    )
    .head(10)
)

fig = px.bar(
    degree,
    x="Degree Centrality",
    y="Node",
    orientation="h",
    text="Degree Centrality",
    color="Degree Centrality",
    color_continuous_scale="Blues"
)

fig.update_layout(
    height=500,
    yaxis=dict(categoryorder="total ascending"),
    xaxis_title="Degree Centrality",
    yaxis_title="Node"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

with st.expander("ℹ Penjelasan Degree Centrality"):

    st.write("""
Degree Centrality menunjukkan jumlah koneksi langsung yang dimiliki
oleh suatu node.

Semakin tinggi nilai Degree Centrality maka semakin aktif node tersebut
berinteraksi dengan node lain dalam jaringan.
""")

st.divider()

# ==========================================================
# TOP 10 CLOSENESS CENTRALITY
# ==========================================================

st.subheader("📊 Top 10 Closeness Centrality")

closeness = (
    df.sort_values(
        by="Closeness Centrality",
        ascending=False
    )
    .head(10)
)

fig = px.bar(
    closeness,
    x="Closeness Centrality",
    y="Node",
    orientation="h",
    text="Closeness Centrality",
    color="Closeness Centrality",
    color_continuous_scale="Greens"
)

fig.update_layout(
    height=500,
    yaxis=dict(categoryorder="total ascending"),
    xaxis_title="Closeness Centrality",
    yaxis_title="Node"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

with st.expander("ℹ Penjelasan Closeness Centrality"):

    st.write("""
Closeness Centrality mengukur seberapa dekat suatu node terhadap
seluruh node lainnya dalam jaringan.

Semakin besar nilainya maka node tersebut semakin cepat menjangkau
node lain.
""")

st.divider()

# ==========================================================
# RANKING NODE
# ==========================================================

st.subheader("🏆 Ranking Berdasarkan Degree Centrality")

ranking_degree = degree[
    ["Node", "Degree Centrality"]
].reset_index(drop=True)

ranking_degree.index += 1

st.dataframe(
    ranking_degree,
    use_container_width=True
)

# ==========================================================
# TOP 10 BETWEENNESS CENTRALITY
# ==========================================================

st.subheader("🔀 Top 10 Betweenness Centrality")

betweenness = (
    df.sort_values(
        by="Betweenness Centrality",
        ascending=False
    )
    .head(10)
)

fig = px.bar(
    betweenness,
    x="Betweenness Centrality",
    y="Node",
    orientation="h",
    text="Betweenness Centrality",
    color="Betweenness Centrality",
    color_continuous_scale="Oranges"
)

fig.update_layout(
    height=500,
    yaxis=dict(categoryorder="total ascending"),
    xaxis_title="Betweenness Centrality",
    yaxis_title="Node"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

with st.expander("ℹ Penjelasan Betweenness Centrality"):

    st.write("""
Betweenness Centrality menunjukkan seberapa sering suatu node
menjadi penghubung (bridge) antara node lainnya.

Semakin tinggi nilainya maka node tersebut berperan penting
dalam penyebaran informasi di dalam jaringan.
""")

st.divider()

# ==========================================================
# TOP 10 EIGENVECTOR CENTRALITY
# ==========================================================

st.subheader("⭐ Top 10 Eigenvector Centrality")

eigen = (
    df.sort_values(
        by="Eigenvector Centrality",
        ascending=False
    )
    .head(10)
)

fig = px.bar(
    eigen,
    x="Eigenvector Centrality",
    y="Node",
    orientation="h",
    text="Eigenvector Centrality",
    color="Eigenvector Centrality",
    color_continuous_scale="Purples"
)

fig.update_layout(
    height=500,
    yaxis=dict(categoryorder="total ascending"),
    xaxis_title="Eigenvector Centrality",
    yaxis_title="Node"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

with st.expander("ℹ Penjelasan Eigenvector Centrality"):

    st.write("""
Eigenvector Centrality mengukur tingkat pengaruh suatu node
berdasarkan hubungan dengan node-node penting lainnya.

Semakin tinggi nilainya maka semakin berpengaruh node tersebut
di dalam jaringan.
""")

st.divider()

# ==========================================================
# PERBANDINGAN CENTRALITY
# ==========================================================

st.subheader("📈 Perbandingan Nilai Centrality (Top 10 Node)")

compare = df.sort_values(
    by="Degree Centrality",
    ascending=False
).head(10)

compare = compare.set_index("Node")

fig = px.line(
    compare.reset_index(),
    x="Node",
    y=[
        "Degree Centrality",
        "Closeness Centrality",
        "Betweenness Centrality",
        "Eigenvector Centrality"
    ],
    markers=True
)

fig.update_layout(
    height=550,
    xaxis_title="Node",
    yaxis_title="Nilai Centrality",
    legend_title="Metrik"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ==========================================================
# TOP NODE SETIAP METRIK
# ==========================================================

st.subheader("🥇 Node Terbaik Berdasarkan Setiap Metrik")

col1, col2 = st.columns(2)

with col1:

    st.success(
        f"""
🏆 Degree Centrality

Node : **{degree.iloc[0]['Node']}**

Nilai : **{degree.iloc[0]['Degree Centrality']:.6f}**
"""
    )

    st.success(
        f"""
🏆 Closeness Centrality

Node : **{closeness.iloc[0]['Node']}**

Nilai : **{closeness.iloc[0]['Closeness Centrality']:.6f}**
"""
    )

with col2:

    st.success(
        f"""
🏆 Betweenness Centrality

Node : **{betweenness.iloc[0]['Node']}**

Nilai : **{betweenness.iloc[0]['Betweenness Centrality']:.6f}**
"""
    )

    st.success(
        f"""
🏆 Eigenvector Centrality

Node : **{eigen.iloc[0]['Node']}**

Nilai : **{eigen.iloc[0]['Eigenvector Centrality']:.6f}**
"""
    )

st.divider()

# ==========================================================
# DATA CENTRALITY
# ==========================================================

st.subheader("📋 Data Centrality")

search = st.text_input(
    "Cari Node",
    placeholder="Masukkan nama node..."
)

if search:

    table = df[
        df["Node"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

else:

    table = df

st.dataframe(
    table,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ==========================================================
# STATISTIK DATA
# ==========================================================

st.subheader("📊 Statistik Centrality")

st.dataframe(
    df.describe(),
    use_container_width=True
)

st.divider()

# ==========================================================
# DOWNLOAD CSV
# ==========================================================

csv = df.to_csv(
    index=False
).encode("utf-8-sig")

st.download_button(
    label="📥 Download Hasil Centrality",
    data=csv,
    file_name="hasil_centrality.csv",
    mime="text/csv"
)

st.divider()

# ==========================================================
# INSIGHT
# ==========================================================

st.subheader("💡 Insight Hasil Social Network Analysis")

degree_node = degree.iloc[0]["Node"]
degree_value = degree.iloc[0]["Degree Centrality"]

close_node = closeness.iloc[0]["Node"]
close_value = closeness.iloc[0]["Closeness Centrality"]

between_node = betweenness.iloc[0]["Node"]
between_value = betweenness.iloc[0]["Betweenness Centrality"]

eigen_node = eigen.iloc[0]["Node"]
eigen_value = eigen.iloc[0]["Eigenvector Centrality"]

st.success(f"""
### Hasil Analisis

🔹 **Degree Centrality**

Node **{degree_node}**
memiliki Degree Centrality tertinggi sebesar
**{degree_value:.6f}**.

Artinya node tersebut memiliki koneksi langsung
paling banyak dengan node lainnya.

---

🔹 **Closeness Centrality**

Node **{close_node}**
memiliki nilai Closeness tertinggi sebesar
**{close_value:.6f}**.

Artinya node tersebut mampu menjangkau
node lain dengan lebih cepat.

---

🔹 **Betweenness Centrality**

Node **{between_node}**
memiliki nilai Betweenness tertinggi sebesar
**{between_value:.6f}**.

Node ini berperan sebagai penghubung utama
dalam jaringan.

---

🔹 **Eigenvector Centrality**

Node **{eigen_node}**
memiliki nilai Eigenvector tertinggi sebesar
**{eigen_value:.6f}**.

Node tersebut merupakan node yang paling
berpengaruh karena terhubung dengan node-node penting.
""")

st.divider()

# ==========================================================
# PENJELASAN
# ==========================================================

with st.expander("ℹ Penjelasan Social Network Analysis"):

    st.markdown("""

## Apa itu Social Network Analysis (SNA)?

Social Network Analysis (SNA) merupakan metode analisis
yang digunakan untuk mempelajari hubungan antar aktor
(node) dalam suatu jaringan.

Pada penelitian ini node merupakan pengguna YouTube
yang berinteraksi melalui komentar.

---

### Degree Centrality

Mengukur jumlah hubungan langsung yang dimiliki
suatu node.

Semakin besar nilainya maka semakin aktif node
tersebut dalam jaringan.

---

### Closeness Centrality

Mengukur kedekatan suatu node terhadap seluruh
node lain.

Semakin tinggi nilainya maka semakin cepat
node tersebut menyebarkan informasi.

---

### Betweenness Centrality

Mengukur seberapa sering suatu node menjadi
jalur penghubung antar node.

Node dengan nilai tinggi memiliki peran
penting sebagai bridge.

---

### Eigenvector Centrality

Mengukur tingkat pengaruh suatu node berdasarkan
hubungannya dengan node-node penting lainnya.

Semakin tinggi nilainya maka semakin berpengaruh
node tersebut dalam jaringan.

""")

st.divider()

# ==========================================================
# FOOTER
# ==========================================================

st.caption(
    "Dashboard Analisis Komentar YouTube MPL Indonesia Season 17 | Social Network Analysis"
)