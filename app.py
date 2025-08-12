import streamlit as st
import numpy as np
import joblib

# Load model dan scaler
model = joblib.load("svm_model.pkl")
scaler = joblib.load("scaler.pkl")

# Daftar fitur dan pertanyaan sesuai urutan
fields = [
    ("PctExtNullSelfRedirectHyperlinksRT", "47. Rasio relatif dari hyperlink kosong atau redirect ke diri sendiri (-1, 0, 1)", "pilihan"),
    ("FrequentDomainNameMismatch", "34. Apakah terjadi ketidaksesuaian nama domain? (ya/tidak)", "biner"),
    ("NumDash", "5. Berapa jumlah tanda hubung (-) dalam URL?", "numerik"),
    ("SubmitInfoToEmail", "38. Apakah form mengirim data ke email? (ya/tidak)", "biner"),
    ("PctNullSelfRedirectHyperlinks", "33. Persentase hyperlink yang redirect ke halaman kosong atau diri sendiri (%)", "persen"),
    ("InsecureForms", "29. Apakah form dikirim melalui HTTP? (ya/tidak)", "biner"),
    ("NumDots", "1. Berapa jumlah titik dalam URL?", "numerik"),
    ("PctExtHyperlinks", "26. Berapa persentase hyperlink eksternal di halaman (%)", "persen"),
    ("NumSensitiveWords", "24. Berapa jumlah kata sensitif di URL (seperti id, login, password)?", "numerik"),
    ("IframeOrFrame", "39. Apakah terdapat iframe/frame di halaman? (ya/tidak)", "biner"),
    ("PathLevel", "3. Berapa jumlah level path dalam URL?", "numerik"),
    ("AbnormalExtFormActionR", "45. Bentuk abnormal pada action form eksternal (-1, 0, 1)", "pilihan"),
    ("UrlLengthRT", "43. Panjang URL relatif terhadap rata-rata (-1, 0, 1)", "pilihan"),
    ("HostnameLength", "20. Berapa panjang hostname (karakter)?", "numerik"),
    ("NumDashInHostname", "6. Berapa jumlah tanda hubung (-) dalam hostname?", "numerik"),
    ("NumQueryComponents", "11. Berapa jumlah komponen parameter dalam query URL?", "numerik"),
    ("AbnormalFormAction", "32. Apakah form action tidak sesuai struktur normal? (ya/tidak)", "biner"),
    ("EmbeddedBrandName", "25. Apakah terdapat nama brand dalam subdomain/path? (ya/tidak)", "biner"),
    ("IpAddress", "17. Apakah URL menggunakan alamat IP? (ya/tidak)", "biner"),
    ("DomainInPaths", "19. Apakah domain utama muncul di path URL? (ya/tidak)", "biner"),
    ("MissingTitle", "40. Apakah halaman tidak memiliki tag title? (ya/tidak)", "biner"),
    ("ExtMetaScriptLinkRT", "46. Rasio tag meta/script/link eksternal (-1, 0, 1)", "pilihan"),
    ("ExtFormAction", "31. Apakah form mengarah ke domain eksternal? (ya/tidak)", "biner"),
    ("DomainInSubdomains", "18. Apakah domain utama muncul di subdomain? (ya/tidak)", "biner"),
]

st.set_page_config(layout="wide")
st.title("Prediksi Phishing Website")

with st.form("phishing_form"):
    st.subheader("Isi data sesuai fitur berikut:")
    cols = st.columns(3)
    inputs = []

    for i, (key, question, tipe) in enumerate(fields):
        with cols[i % 3]:
            if tipe == "biner":
                val = st.radio(question, ["Tidak", "Ya"], index=0, key=key)
                inputs.append(1 if val == "Ya" else 0)
            elif tipe == "pilihan":
                val = st.selectbox(question, [-1, 0, 1], index=1, key=key)
                inputs.append(val)
            elif tipe == "persen":
                val = st.number_input(question, min_value=0.0, max_value=100.0, step=1.0, key=key)
                inputs.append(val)
            else:  # numerik
                val = st.number_input(question, step=1, key=key)
                inputs.append(val)

    submitted = st.form_submit_button("Prediksi")

    if submitted:
        try:
            input_array = scaler.transform([inputs])
            prediction = model.predict(input_array)[0]
            label = "🟢 Legitimate" if prediction == 0 else "🔴 Phishing"
            st.success(f"Hasil Prediksi: **{label}**")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat memproses input: {e}")
