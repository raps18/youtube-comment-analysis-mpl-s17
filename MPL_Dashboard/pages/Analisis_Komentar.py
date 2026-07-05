import streamlit as st
import pandas as pd

from utils.load_data import load_comments

# =====================================================
# LOAD DATA
# =====================================================

df = load_comments()

st.title("🔍 Analisis Komentar")

st.markdown("Melakukan pencarian dan analisis komentar YouTube MPL Indonesia Season 17")

st.divider()

# =====================================================
# SIDEBAR FILTER
# =====================================================

st.sidebar.header("Filter Data")

# Search komentar
search_comment = st.sidebar.text_input(
    "🔎 Cari Komentar"
)

# Search Author
search_author = st.sidebar.text_input(
    "👤 Cari Nama User"
)

# Label
label_option = st.sidebar.selectbox(

    "Label",

    ["Semua"] + sorted(df["label"].unique().tolist())

)

# Video

video_option = st.sidebar.selectbox(

    "Video",

    ["Semua"] + sorted(df["video_title"].unique().tolist())

)

# Week

week_option = st.sidebar.selectbox(

    "Week",

    ["Semua"] + sorted(df["keyword"].unique().tolist())

)

# =====================================================
# FILTER DATA
# =====================================================

filtered = df.copy()

if search_comment:

    filtered = filtered[
        filtered["comment"].str.contains(
            search_comment,
            case=False,
            na=False
        )
    ]

if search_author:

    filtered = filtered[
        filtered["author"].str.contains(
            search_author,
            case=False,
            na=False
        )
    ]

if label_option != "Semua":

    filtered = filtered[
        filtered["label"] == label_option
    ]

if video_option != "Semua":

    filtered = filtered[
        filtered["video_title"] == video_option
    ]

if week_option != "Semua":

    filtered = filtered[
        filtered["keyword"] == week_option
    ]

# =====================================================
# HASIL FILTER
# =====================================================

st.subheader("📊 Ringkasan")

col1,col2,col3 = st.columns(3)

col1.metric(
    "Jumlah Komentar",
    len(filtered)
)

col2.metric(
    "Jumlah User",
    filtered["author"].nunique()
)

col3.metric(
    "Jumlah Video",
    filtered["video_title"].nunique()
)

st.divider()

# =====================================================
# LABEL RESULT
# =====================================================

label_count = filtered["label"].value_counts()

col1,col2 = st.columns(2)

with col1:

    st.metric(
        "🟢 Non-Toxic",
        label_count.get("Non-Toxic",0)
    )

with col2:

    st.metric(
        "🔴 Toxic",
        label_count.get("Toxic",0)
    )

st.divider()

# =====================================================
# DATA TABLE
# =====================================================

st.subheader("📋 Hasil Pencarian")

show = filtered[

    [

        "author",

        "comment",

        "label",

        "video_title",

        "published_at",

        "like_count"

    ]

].copy()

show.columns = [

    "Nama User",

    "Komentar",

    "Label",

    "Video",

    "Tanggal",

    "Like"

]

st.dataframe(

    show,

    use_container_width=True,

    hide_index=True

)

st.write(f"Menampilkan {len(show)} komentar")

# =====================================================
# DOWNLOAD CSV
# =====================================================

csv = show.to_csv(index=False).encode("utf-8-sig")

st.download_button(

    "📥 Download Hasil Filter",

    csv,

    "hasil_filter.csv",

    "text/csv"

)