import streamlit as st
import plotly.express as px

from utils.load_data import load_comments, load_bertopic

# =====================================================
# LOAD DATA
# =====================================================

df = load_comments()
df_topic = load_bertopic()

# =====================================================
# CEK DATA
# =====================================================

if df.empty:
    st.error("Data komentar tidak ditemukan.")
    st.stop()

if df_topic.empty:
    st.error("Data BERTopic tidak ditemukan.")
    st.stop()

# =====================================================
# TITLE
# =====================================================

st.title("🏠 Dashboard Overview")
st.markdown("""
Dashboard ini menyajikan ringkasan hasil penelitian **Analisis Komentar YouTube MPL Indonesia Season 17**
menggunakan metode:

- Naive Bayes
- Support Vector Machine (SVM)
- BERTopic
- Social Network Analysis (SNA)
""")

st.divider()

# =====================================================
# KPI
# =====================================================

total_comment = len(df)
total_user = df["author"].nunique()
total_video = df["video_title"].nunique()

# Total Topic
if "topic" in df_topic.columns:
    total_topic = df_topic["topic"].nunique()
else:
    total_topic = 4

# Label
label_count = (
    df["label"]
    .astype(str)
    .str.strip()
    .value_counts()
)

total_toxic = label_count.get("Toxic", 0)
total_non_toxic = label_count.get("Non-Toxic", 0)

# =====================================================
# KPI CARD
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💬 Total Komentar", f"{total_comment:,}")

with col2:
    st.metric("👤 Total User", f"{total_user:,}")

with col3:
    st.metric("🎥 Total Video", f"{total_video:,}")

col4, col5, col6 = st.columns(3)

with col4:
    st.metric("📊 Total Topik", total_topic)

with col5:
    st.metric("🟢 Non-Toxic", f"{total_non_toxic:,}")

with col6:
    st.metric("🔴 Toxic", f"{total_toxic:,}")

st.divider()

# =====================================================
# PIE CHART
# =====================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("🥧 Distribusi Label")

    fig = px.pie(
        names=label_count.index,
        values=label_count.values,
        hole=0.45
    )

    fig.update_layout(height=420)

    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# WEEK DISTRIBUTION
# =====================================================

with col2:

    st.subheader("📈 Distribusi Komentar per Week")

    week_count = (
        df["keyword"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    week_count.columns = ["Week", "Jumlah"]

    fig = px.bar(
        week_count,
        x="Week",
        y="Jumlah",
        text_auto=True
    )

    fig.update_layout(height=420)

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# =====================================================
# TOPIC DISTRIBUTION
# =====================================================

st.subheader("📊 Distribusi Topik BERTopic")

if "topic" in df_topic.columns:

    topic_count = (
        df_topic["topic"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    topic_count.columns = ["Topic", "Jumlah"]

    fig = px.bar(
        topic_count,
        x="Topic",
        y="Jumlah",
        color="Topic",
        text_auto=True
    )

    fig.update_layout(height=500)

    st.plotly_chart(fig, use_container_width=True)

else:

    st.warning("Kolom topic tidak ditemukan.")

st.divider()

# =====================================================
# DATA TERBARU
# =====================================================

st.subheader("📋 10 Komentar Terbaru")

show_df = df[
    [
        "author",
        "comment",
        "label",
        "video_title",
        "published_at"
    ]
].copy()

show_df.columns = [
    "Author",
    "Komentar",
    "Label",
    "Video",
    "Tanggal"
]

st.dataframe(
    show_df.head(10),
    use_container_width=True,
    hide_index=True
)

st.divider()

# =====================================================
# INFORMASI DATASET
# =====================================================

with st.expander("ℹ️ Informasi Dataset"):

    st.write("Jumlah Baris :", len(df))
    st.write("Jumlah Kolom :", len(df.columns))
    st.write("Kolom Dataset :")

    st.write(df.columns.tolist())