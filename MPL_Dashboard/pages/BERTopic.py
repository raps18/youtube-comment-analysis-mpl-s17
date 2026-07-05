import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

from utils.load_data import load_bertopic

# ==========================================================
# CONFIG
# ==========================================================

st.set_page_config(layout="wide")

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_PATH = BASE_DIR / "image"

# ==========================================================
# LOAD DATA
# ==========================================================

df = load_bertopic()

if df.empty:
    st.error("Data BERTopic tidak ditemukan.")
    st.stop()

# ==========================================================
# TITLE
# ==========================================================

st.title("📊 Analisis Topik Menggunakan BERTopic")

st.markdown("""
Halaman ini menampilkan hasil **Topic Modeling**
komentar YouTube MPL Indonesia Season 17 menggunakan
algoritma **BERTopic**.
""")

st.divider()

# ==========================================================
# KPI
# ==========================================================

total_comment = len(df)

total_topic = df["topic"].nunique()

outlier = (df["topic"] == -1).sum()

col1, col2, col3 = st.columns(3)

col1.metric("💬 Total Komentar", total_comment)

col2.metric("📂 Jumlah Topic", total_topic)

col3.metric("⚠️ Outlier", outlier)

st.divider()

# ==========================================================
# DISTRIBUSI TOPIK
# ==========================================================

st.subheader("📈 Distribusi Topic")

topic_count = (
    df["topic"]
    .value_counts()
    .sort_index()
    .reset_index()
)

topic_count.columns = ["Topic","Jumlah"]

fig = px.bar(
    topic_count,
    x="Topic",
    y="Jumlah",
    color="Topic",
    text="Jumlah"
)

fig.update_layout(height=450)

st.plotly_chart(fig,use_container_width=True)

# ==========================================================
# PERSENTASE TOPIK
# ==========================================================

st.subheader("🥧 Persentase Distribusi Topic")

# Hitung persentase
topic_count["Persentase (%)"] = (
    topic_count["Jumlah"] / topic_count["Jumlah"].sum() * 100
).round(2)

col1, col2 = st.columns([2, 1])

# =======================
# DONUT CHART
# =======================

with col1:

    fig = px.pie(
        topic_count,
        names="Topic",
        values="Jumlah",
        hole=0.60,
        color="Topic"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        pull=[0.08 if i == 0 else 0 for i in range(len(topic_count))]
    )

    fig.update_layout(
        title="Distribusi Topic BERTopic",
        height=550,
        legend_title="Topic"
    )

    st.plotly_chart(fig, use_container_width=True)

# =======================
# TABEL PERSENTASE
# =======================

with col2:

    st.markdown("### 📋 Persentase Topic")

    st.dataframe(
        topic_count[["Topic", "Jumlah", "Persentase (%)"]],
        use_container_width=True,
        hide_index=True
    )

# ==========================================================
# FILTER
# ==========================================================

col1,col2=st.columns(2)

with col1:

    topic_list=sorted(df["topic"].unique())

    selected_topic=st.selectbox(
        "Pilih Topic",
        topic_list
    )

with col2:

    label_option=st.selectbox(
        "Filter Label",
        [
            "Semua",
            "Toxic",
            "Non-Toxic"
        ]
    )

topic_df=df[df["topic"]==selected_topic]

if label_option!="Semua":

    topic_df=topic_df[
        topic_df["label"]==label_option
    ]

# ==========================================================
# SEARCH
# ==========================================================

keyword=st.text_input(
    "🔍 Cari Komentar"
)

if keyword:

    topic_df=topic_df[
        topic_df["comment"].str.contains(
            keyword,
            case=False,
            na=False
        )
    ]

st.divider()

# ==========================================================
# STATISTIK TOPIK
# ==========================================================

toxic=(topic_df["label"]=="Toxic").sum()

non_toxic=(topic_df["label"]=="Non-Toxic").sum()

c1,c2,c3=st.columns(3)

c1.metric(
    "Jumlah Komentar",
    len(topic_df)
)

c2.metric(
    "Toxic",
    toxic
)

c3.metric(
    "Non Toxic",
    non_toxic
)

st.divider()

# ==========================================================
# GAMBAR TOPIK
# ==========================================================

st.subheader("🖼 Visualisasi BERTopic")

gambar={

0:"bertopic_topics 0.png",
1:"bertopic_topics 1.png",
2:"bertopic_topics 2.png",
3:"bertopic_topics 3.png"

}

if selected_topic in gambar:

    file=IMAGE_PATH/gambar[selected_topic]

    if file.exists():

        st.image(
            str(file),
            use_container_width=True
        )

    else:

        st.warning("Gambar tidak ditemukan.")

elif selected_topic==-1:

    st.info("""
Topic -1 merupakan **Outlier**.

Komentar pada topic ini tidak memiliki kemiripan
yang cukup sehingga tidak masuk ke cluster tertentu.
""")

else:

    st.info(
        "Visualisasi hanya tersedia untuk Topic 0-3."
    )

st.divider()

# ==========================================================
# TABEL
# ==========================================================

st.subheader("📋 Daftar Komentar")

show=topic_df[[
    "author",
    "comment",
    "label",
    "video_title",
    "published_at"
]]

show.columns=[
    "Nama User",
    "Komentar",
    "Label",
    "Video",
    "Tanggal"
]

st.dataframe(
    show,
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# DOWNLOAD
# ==========================================================

csv=show.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    "📥 Download CSV",
    csv,
    file_name=f"Topic_{selected_topic}.csv",
    mime="text/csv"
)

st.divider()

# ==========================================================
# TOP TOPIK
# ==========================================================

st.subheader("🏆 Ranking Topic")

ranking=topic_count.sort_values(
    "Jumlah",
    ascending=False
)

st.dataframe(
    ranking,
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# WORD PALING SERING
# ==========================================================

st.subheader("📝 Kata yang Sering Muncul")

text=" ".join(topic_df["comment"].astype(str))

kata=pd.Series(text.split())

top_words=kata.value_counts().head(20)

fig=px.bar(

    x=top_words.values,

    y=top_words.index,

    orientation="h",

    labels={

        "x":"Frekuensi",

        "y":"Kata"

    }

)

fig.update_layout(height=500)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# ==========================================================
# PENJELASAN
# ==========================================================

with st.expander("ℹ Penjelasan BERTopic"):

    st.markdown("""

### BERTopic

BERTopic merupakan metode Topic Modeling yang menggabungkan:

- Sentence Transformer
- UMAP
- HDBSCAN
- c-TF-IDF

untuk menemukan kelompok pembahasan yang sering muncul
pada komentar YouTube.

### Interpretasi

**Topic -1**

Komentar tidak berhasil masuk ke cluster tertentu
(outlier).

**Topic 0,1,2,...**

Kelompok komentar dengan pembahasan yang serupa.

Semakin banyak komentar pada suatu topic,
menunjukkan topik tersebut paling sering dibahas
oleh penonton MPL Indonesia Season 17.

""")