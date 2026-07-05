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
Dashboard ini menyajikan hasil **Social Network Analysis (SNA)**
terhadap komentar YouTube **MPL Indonesia Season 17**.

Analisis dilakukan untuk mengetahui pola hubungan antar pengguna
(User) dengan komunitas atau tim Mobile Legends Professional League
(MPL Indonesia) berdasarkan komentar yang diberikan pada setiap video.

Node pada jaringan terdiri atas:

- 👤 Pengguna YouTube
- 🏆 Tim MPL Indonesia

Sedangkan edge menunjukkan adanya hubungan berupa penyebutan
nama tim pada komentar yang ditulis oleh pengguna.
""")

st.divider()

# ==========================================================
# KPI
# ==========================================================

jumlah_node = len(df)

degree_max = df["Degree Centrality"].max()
close_max = df["Closeness Centrality"].max()
between_max = df["Betweenness Centrality"].max()
eigen_max = df["Eigenvector Centrality"].max()

c1,c2,c3,c4,c5 = st.columns(5)

with c1:
    st.metric(
        "👥 Total Node",
        jumlah_node
    )

with c2:
    st.metric(
        "📈 Degree",
        f"{degree_max:.4f}"
    )

with c3:
    st.metric(
        "📊 Closeness",
        f"{close_max:.4f}"
    )

with c4:
    st.metric(
        "🔀 Betweenness",
        f"{between_max:.4f}"
    )

with c5:
    st.metric(
        "⭐ Eigenvector",
        f"{eigen_max:.4f}"
    )

st.divider()

# ==========================================================
# PENJELASAN SNA
# ==========================================================

st.subheader("📖 Apa itu Social Network Analysis?")

st.info("""

**Social Network Analysis (SNA)** merupakan metode analisis jaringan
yang digunakan untuk mengetahui hubungan antar aktor (node) di dalam
suatu jaringan.

Pada penelitian ini digunakan **graf bipartit (Bipartite Graph)**,
karena terdapat dua jenis node yang berbeda yaitu:

• Pengguna YouTube

• Tim MPL Indonesia

Hubungan (edge) terbentuk ketika seorang pengguna menyebut nama
suatu tim pada komentar YouTube.

Semakin banyak hubungan yang dimiliki suatu node,
maka semakin penting posisi node tersebut di dalam jaringan.

""")

st.divider()

# ==========================================================
# VISUALISASI NETWORK
# ==========================================================

st.subheader("🌐 Visualisasi Jaringan Komentar")

network = IMAGE_PATH / "network_graph.png"

if network.exists():

    st.image(
        str(network),
        use_container_width=True,
        caption="Graf Bipartit Hubungan Pengguna dengan Tim MPL Indonesia"
    )

else:

    st.warning(
        "File network_graph.png belum tersedia."
    )

st.success("""

Interpretasi visualisasi:

🔵 Node Biru
: Merepresentasikan pengguna YouTube.

🔴 Node Merah
: Merepresentasikan tim MPL Indonesia.

➖ Garis (Edge)
: Menunjukkan pengguna menyebutkan nama tim
pada komentar YouTube.

Semakin besar ukuran node,
semakin banyak hubungan yang dimiliki node tersebut.

""")

st.divider()

# ==========================================================
# PENJELASAN TIM MPL
# ==========================================================

st.subheader("🏆 Tim MPL Indonesia yang Dianalisis")

team = pd.DataFrame({

"Nama Tim":[

"RRQ Hoshi",
"ONIC Esports",
"EVOS",
"Team Liquid ID",
"Bigetron Esports",
"Alter Ego",
"Dewa United Esports",
"Geek Fam ID",
"NAVI"

],

"Penjelasan":[

"Tim yang sering disebut pada komentar mengenai performa pertandingan maupun roster.",
"Juara bertahan yang banyak memperoleh perhatian dari penonton.",
"Salah satu tim dengan basis penggemar terbesar sehingga sangat sering muncul pada komentar.",
"Tim yang sebelumnya dikenal sebagai Aura Fire dan menjadi bahan diskusi penonton.",
"Tim yang cukup aktif dibahas terutama mengenai performa pemain.",
"Sering disebut ketika membahas strategi permainan.",
"Tim yang mulai berkembang sehingga mulai banyak diperbincangkan.",
"Tim yang cukup sering dibahas terutama ketika menghadapi tim besar.",
"Tim baru di MPL Indonesia sehingga menjadi perhatian penonton."

]

})

st.dataframe(
    team,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ==========================================================
# KARAKTERISTIK JARINGAN
# ==========================================================

st.subheader("📌 Karakteristik Jaringan")

left,right = st.columns(2)

with left:

    st.success("""

### Jenis Graf

✅ Graf Bipartit

Node dibagi menjadi dua kelompok:

- User YouTube
- Tim MPL Indonesia

Tidak terdapat hubungan langsung
antar sesama user ataupun sesama tim.

""")

with right:

    st.success("""

### Algoritma

Library :
NetworkX

Layout :

Spring Layout (Force Directed)

Metode Analisis :

• Degree Centrality

• Closeness Centrality

• Betweenness Centrality

• Eigenvector Centrality

""")

st.divider()

st.header("📈 Degree Centrality")

st.markdown("""
Degree Centrality menunjukkan **jumlah hubungan langsung** yang dimiliki
oleh setiap node di dalam jaringan.

Semakin tinggi nilai Degree Centrality, maka semakin banyak pengguna
yang terhubung dengan node tersebut.
""")

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
    yaxis=dict(categoryorder="total ascending")
)

st.plotly_chart(fig, use_container_width=True)

top_degree = degree.iloc[0]

st.success(f"""
### 🏆 Node dengan Degree Centrality Tertinggi

**{top_degree['Node']}**

Nilai Degree Centrality :

**{top_degree['Degree Centrality']:.6f}**

Interpretasi:

Node ini mempunyai hubungan langsung paling banyak
dibandingkan node lainnya.

Apabila node tersebut merupakan **EVOS**, maka hal ini
menunjukkan bahwa EVOS menjadi tim yang paling sering
disebut oleh pengguna YouTube sehingga memiliki
jumlah koneksi terbesar di dalam jaringan komentar.
""")

st.dataframe(
    degree,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.header("📊 Closeness Centrality")

st.markdown("""
Closeness Centrality mengukur **kedekatan suatu node**
terhadap seluruh node lain di dalam jaringan.

Semakin tinggi nilainya maka semakin cepat node tersebut
dapat menjangkau node lainnya.
""")

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

    yaxis=dict(categoryorder="total ascending")

)

st.plotly_chart(fig,use_container_width=True)

top_close = closeness.iloc[0]

st.success(f"""

### 🏆 Node dengan Closeness Centrality Tertinggi

**{top_close['Node']}**

Nilai :

**{top_close['Closeness Centrality']:.6f}**

Interpretasi:

Node ini memiliki jarak rata-rata paling dekat
dengan node lainnya.

Apabila node tersebut adalah **EVOS**,
maka EVOS merupakan tim yang paling cepat
terhubung dengan seluruh pengguna
di dalam jaringan komentar.

""")

st.dataframe(

    closeness,

    use_container_width=True,

    hide_index=True

)

st.divider()

st.header("🔀 Betweenness Centrality")

st.markdown("""
Betweenness Centrality menunjukkan seberapa besar
peran suatu node sebagai **penghubung (bridge)**
antara node-node lain.
""")

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

    yaxis=dict(categoryorder="total ascending")

)

st.plotly_chart(fig,use_container_width=True)

top_between = betweenness.iloc[0]

if top_between["Betweenness Centrality"] == 0:

    st.warning("""

Seluruh node memiliki nilai Betweenness Centrality = 0.

Hal ini disebabkan karena jaringan yang digunakan
berbentuk **Graf Bipartit**.

Hubungan yang terbentuk hanya antara pengguna
dan tim MPL sehingga hampir tidak terdapat
jalur alternatif yang membuat suatu node
menjadi penghubung antar node lain.

""")

else:

    st.success(f"""

### 🏆 Node dengan Betweenness Tertinggi

**{top_between['Node']}**

Nilai :

**{top_between['Betweenness Centrality']:.6f}**

Node ini paling sering menjadi jalur penghubung
antar node di dalam jaringan.

""")

st.dataframe(

    betweenness,

    use_container_width=True,

    hide_index=True

)

st.divider()

st.header("⭐ Eigenvector Centrality")

st.markdown("""
Eigenvector Centrality mengukur **tingkat pengaruh**
suatu node berdasarkan hubungan dengan
node-node penting lainnya.
""")

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

    yaxis=dict(categoryorder="total ascending")

)

st.plotly_chart(fig,use_container_width=True)

top_eigen = eigen.iloc[0]

st.success(f"""

### 🏆 Node dengan Eigenvector Centrality Tertinggi

**{top_eigen['Node']}**

Nilai :

**{top_eigen['Eigenvector Centrality']:.6f}**

Interpretasi:

Node ini merupakan node yang paling berpengaruh
di dalam jaringan karena tidak hanya memiliki
banyak hubungan, tetapi juga terhubung
dengan node-node penting lainnya.

Apabila node tersebut adalah **EVOS**,
maka EVOS merupakan pusat perhatian pengguna
dan menjadi salah satu topik utama
dalam komentar YouTube MPL Indonesia Season 17.

""")

st.dataframe(

    eigen,

    use_container_width=True,

    hide_index=True

)

st.divider()

st.header("📈 Perbandingan Nilai Centrality")

compare = df.sort_values(
    by="Degree Centrality",
    ascending=False
).head(10)

fig = px.line(
    compare,
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
    height=600,
    legend_title="Jenis Centrality",
    xaxis_title="Node",
    yaxis_title="Nilai"
)

st.plotly_chart(fig, use_container_width=True)

st.info("""
Grafik ini menunjukkan perbandingan empat ukuran centrality pada
10 node dengan Degree Centrality tertinggi.

Melalui grafik ini dapat diketahui node mana yang paling dominan
berdasarkan setiap ukuran centrality.
""")

st.divider()

st.header("🏆 Ringkasan Node Terbaik")

c1,c2=st.columns(2)

with c1:

    st.success(f"""
### 📈 Degree Centrality

Node :

**{top_degree['Node']}**

Nilai :

**{top_degree['Degree Centrality']:.6f}**
""")

    st.success(f"""
### 📊 Closeness Centrality

Node :

**{top_close['Node']}**

Nilai :

**{top_close['Closeness Centrality']:.6f}**
""")

with c2:

    st.success(f"""
### 🔀 Betweenness Centrality

Node :

**{top_between['Node']}**

Nilai :

**{top_between['Betweenness Centrality']:.6f}**
""")

    st.success(f"""
### ⭐ Eigenvector Centrality

Node :

**{top_eigen['Node']}**

Nilai :

**{top_eigen['Eigenvector Centrality']:.6f}**
""")

st.divider()

st.header("🔍 Pencarian Node")

search = st.text_input(
    "Cari nama node..."
)

if search:

    hasil = df[
        df["Node"].astype(str).str.contains(
            search,
            case=False,
            na=False
        )
    ]

    st.dataframe(
        hasil,
        use_container_width=True,
        hide_index=True
    )

else:

    st.dataframe(
        df.head(20),
        use_container_width=True,
        hide_index=True
    )

st.divider()

st.header("📊 Statistik Centrality")

st.dataframe(
    df.describe(),
    use_container_width=True
)

st.divider()

st.header("💡 Insight Hasil Analisis")

st.success(f"""

### Hasil Analisis Social Network Analysis

Berdasarkan hasil pengukuran centrality diperoleh bahwa:

• **{top_degree['Node']}**
memiliki Degree Centrality tertinggi sebesar
**{top_degree['Degree Centrality']:.6f}**.

Hal ini menunjukkan bahwa node tersebut
memiliki hubungan langsung paling banyak
dengan node lain.

---

• **{top_close['Node']}**
memiliki Closeness Centrality tertinggi sebesar
**{top_close['Closeness Centrality']:.6f}**.

Artinya node tersebut mempunyai jarak
paling dekat terhadap seluruh node
dalam jaringan.

---

• **{top_between['Node']}**
memiliki Betweenness Centrality tertinggi sebesar
**{top_between['Betweenness Centrality']:.6f}**.

Node tersebut berperan sebagai penghubung
antar kelompok node.

---

• **{top_eigen['Node']}**
memiliki Eigenvector Centrality tertinggi sebesar
**{top_eigen['Eigenvector Centrality']:.6f}**.

Hal ini menunjukkan bahwa node tersebut
memiliki pengaruh paling besar
karena terhubung dengan node-node penting.

""")

st.divider()

st.header("📌 Kesimpulan")

st.info(f"""

Berdasarkan hasil **Social Network Analysis (SNA)**
terhadap komentar YouTube MPL Indonesia Season 17
diperoleh bahwa node **{top_degree['Node']}**
merupakan node yang paling dominan di dalam jaringan.

Hal tersebut ditunjukkan melalui nilai Degree,
Closeness, Betweenness, maupun Eigenvector
yang relatif lebih tinggi dibandingkan node lainnya.

Artinya node tersebut menjadi pusat interaksi
serta memiliki pengaruh besar terhadap
percakapan pengguna YouTube.

Dengan demikian dapat disimpulkan bahwa
node tersebut merupakan pusat perhatian
masyarakat selama berlangsungnya
MPL Indonesia Season 17.

""")

st.divider()

with st.expander("📖 Penjelasan Metrik Social Network Analysis"):

    st.markdown("""

### Degree Centrality

Mengukur banyaknya hubungan langsung yang dimiliki suatu node.

---

### Closeness Centrality

Mengukur kedekatan suatu node terhadap seluruh node lainnya.

---

### Betweenness Centrality

Mengukur seberapa sering suatu node menjadi penghubung
antar node lainnya.

---

### Eigenvector Centrality

Mengukur tingkat pengaruh suatu node berdasarkan hubungan
dengan node-node penting lainnya.

---

### Mengapa menggunakan Social Network Analysis?

Social Network Analysis digunakan untuk mengetahui
hubungan antar pengguna YouTube dengan tim MPL Indonesia.

Melalui metode ini dapat diketahui:

- Tim yang paling banyak dibicarakan.
- Tim yang menjadi pusat perhatian.
- Tim yang mempunyai pengaruh paling besar.
- Struktur hubungan antar pengguna dan tim.

Pada penelitian ini jaringan dibangun menggunakan
graf bipartit sehingga hubungan hanya terbentuk
antara pengguna YouTube dan tim MPL Indonesia.

""")
    
st.caption(
    "Dashboard Analisis Komentar YouTube MPL Indonesia Season 17 | Social Network Analysis"
)
