import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from pathlib import Path

# ===========================================
# PATH
# ===========================================

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_PATH = BASE_DIR / "image"

# ===========================================
# PAGE
# ===========================================

st.title("😀 Hasil Klasifikasi")

st.markdown("""
Halaman ini menampilkan hasil evaluasi algoritma klasifikasi
yang digunakan untuk mendeteksi komentar **Toxic** dan **Non-Toxic**
pada komentar YouTube MPL Indonesia Season 17.
""")

st.divider()

# ===========================================
# METRIK
# ===========================================

nb = {
    "Accuracy":0.938,
    "Precision":0.94,
    "Recall":0.94,
    "F1 Score":0.91
}

svm = {
    "Accuracy":0.973,
    "Precision":0.97,
    "Recall":0.97,
    "F1 Score":0.97
}

# ===========================================
# CARD
# ===========================================

st.subheader("📊 Perbandingan Performa")

col1,col2 = st.columns(2)

with col1:

    st.success("Naive Bayes")

    c1,c2 = st.columns(2)

    c1.metric("Accuracy",f"{nb['Accuracy']*100:.2f}%")
    c2.metric("Precision",f"{nb['Precision']*100:.2f}%")

    c3,c4 = st.columns(2)

    c3.metric("Recall",f"{nb['Recall']*100:.2f}%")
    c4.metric("F1 Score",f"{nb['F1 Score']*100:.2f}%")

with col2:

    st.success("Support Vector Machine")

    c1,c2 = st.columns(2)

    c1.metric("Accuracy",f"{svm['Accuracy']*100:.2f}%")
    c2.metric("Precision",f"{svm['Precision']*100:.2f}%")

    c3,c4 = st.columns(2)

    c3.metric("Recall",f"{svm['Recall']*100:.2f}%")
    c4.metric("F1 Score",f"{svm['F1 Score']*100:.2f}%")

st.divider()

# ===========================================
# CONFUSION MATRIX
# ===========================================

st.subheader("🧩 Confusion Matrix")

col1,col2 = st.columns(2)

with col1:

    st.write("### Naive Bayes")

    img = Image.open(IMAGE_PATH/"nb_confusion_matrix.png")

    st.image(img,use_container_width=True)

with col2:

    st.write("### Support Vector Machine")

    img = Image.open(IMAGE_PATH/"svm_confusion_matrix.png")

    st.image(img,use_container_width=True)

st.divider()

# ===========================================
# BAR CHART
# ===========================================

st.subheader("📈 Perbandingan Algoritma")

compare = pd.DataFrame({

    "Metric":[
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score"
    ],

    "Naive Bayes":[
        93.8,
        94,
        94,
        91
    ],

    "SVM":[
        97.3,
        97,
        97,
        97
    ]

})

fig = px.bar(

    compare,

    x="Metric",

    y=["Naive Bayes","SVM"],

    barmode="group",

    text_auto=True

)

fig.update_layout(height=500)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# ===========================================
# KESIMPULAN
# ===========================================

st.subheader("📌 Kesimpulan")

st.info("""
Berdasarkan hasil evaluasi model:

• Support Vector Machine memiliki performa terbaik.

• Accuracy mencapai 97,3%.

• Precision, Recall dan F1 Score lebih tinggi dibanding Naive Bayes.

• Naive Bayes memiliki Recall Toxic yang rendah sehingga
masih banyak komentar Toxic yang gagal dikenali.

• Oleh karena itu SVM dipilih sebagai model terbaik
untuk klasifikasi komentar Toxic dan Non-Toxic.
""")