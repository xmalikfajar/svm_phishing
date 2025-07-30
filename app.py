import streamlit as st
import pickle
import numpy as np


import joblib

# Load model dan scaler
model = joblib.load("svm_model.pkl")
scaler = joblib.load("scaler.pkl")

st.title("Deteksi URL Phishing")
st.write("Masukkan data URL untuk memprediksi apakah termasuk phishing atau legitimate.")

# Buat layout kolom 3
cols = st.columns(3)

# Pertanyaan numerik
numerik_inputs = {
    "NumDots" : ["Berapa jumlah titik dalam url", 0],
    "SubdomainLevel" : ["Berapa jumlah level subdomain", 0],
    "PathLevel" : ["Berapa jumlah path level", 0],
    "UrlLength" : ["Berapa panjang karakter url", 12],
    "NumDash" : ["Berapa jumlah tanda hubung (-) dalam url", 0],
    "NumDashInHostname" : ["Berapa jumlah tanda hubung (-) dalam hostname", 0],
    "NumUnderscore" : ["Berapa jumlah garis bawah / underscore dalam url", 0],
    "NumPercent" : ["Berapa jumlah simbol persen dalam url", 0],
    "NumQueryComponents" : ["Berapa jumlah komponen parameter dalam query url", 0],
    "NumAmpersand" : ["Berapa jumlah simbol & dalam url", 0],
    "NumHash" : ["Berapa jumlah simbol # dalam url", 0],
    "NumNumericChars" : ["Berapa jumlah karakter angka dalam url", 0],
    "HostnameLength" : ["Berapa panjang hostname", 3],
    "PathLength" : ["Berapa panjang path dalam url", 0],
    "QueryLength" : ["Berapa panjang query dalam url", 0],
    "NumSensitiveWords" : ["berpa jumlah kata sensitif di url(seperti id, login,password)", 0],
    "PctExtHyperlinks" : ["Berapa persentase hyperlink external di halaman", 0.0],
    "PctExtResourceUrls" : ["Berapa persentase resource (img,js,dll) external di halaman", 0.0],
    "PctNullSelfRedirectHyperlinks" : ["persentase hyperlink yang redirect ke halaman kosong atau diri sendiri", 0.0]
}

# Pertanyaan Yes/No bernilai 0/1
yesno_inputs = {
    "AtSymbol" : "apakah ada simbol @ dalam url",
    "TildeSymbol" : "apakah ada simbol ~ dalam url",
    "NoHttps" : "apakah url tidak menggunakan https",
    "RandomString" : "apakah url mengandung string acak",
    "IpAddress" : "apakah url menggunakan alamat ip",
    "DomainInSubdomains" : "apakah domain utama muncul di subdomain",
    "DomainInPaths" : "apakah domain utama muncul di path url",
    "DoubleSlashInPath" : "apakah terdapat dua garis miring (//) dalam path",
    "EmbeddedBrandName" : "Apakah terdapat nama brand dalam subdomain/path",
    "ExtFavicon" : "apakah favicon dimuat dari domain external",
    "InsecureForms" : "apakah form dikitim melalui http",
    "RelativeFormAction" : "apakah form menggunakan action relative",
    "ExtFormAction" : "apakah form menhgarah ke domain external",
    "AbnormalFormAction" : "apakah form action tidak sesuai struktur normal",
    "FrequentDomainNameMismatch" : "Apakah terjadi ketidak sesuaian nama domain",
    "FakeLinkInStatusBar" : "apakah status bar memalsukan link",
    "RightClickDisabled" : "apakah klik kanan dinonaktifkan",
    "PopUpWindow" : "apakah membuka jendela popup",
    "SubmitInfoToEmail" : "apakah formmengirim data ke email",
    "IframeOrFrame" : "apakah terdapat iframe/frame di halaman",
    "MissingTitle" : "apakah halaman tidak memiliki tag title",
    "ImagesOnlyInForm" : "apakah hanya gamnar yang digunakan dalam form"
}

# Pertanyaan -1/0/1
kategori_inputs = {
    "SubdomainLevelRT" : ["level subdomain relatif", [-1, 0, 1]],
    "UrlLengthRT" : ["Panjang URL relatif terhadap rata-rata", [-1, 0, 1]],
    "PctExtResourceUrlsRT" : ["ersentase resource eksternal relatif terhadap standar", [-1, 0, 1]],
    "AbnormalExtFormActionR" : ["Bentuk abnormal pada action form eksternal", [-1, 0, 1]],
    "ExtMetaScriptLinkRT" : ["Rasio tag meta/script/link eksternal", [-1, 0, 1]],
    "PctExtNullSelfRedirectHyperlinksRT" : ["Rasio relatif dari hyperlink kosong atau redirect ke diri sendiri", [-1, 0, 1]]
}

user_input = {}
p = []

# Input numerik
for i, (label, question) in enumerate(numerik_inputs.items()):
    with cols[i % 3]:
        val = st.number_input(question[0], value=question[1], key=label)
        user_input[label] = val
        p.append(val)

# Input yes/no (0/1)
for i, (label, question) in enumerate(yesno_inputs.items()):
    with cols[(i + len(numerik_inputs)) % 3]:
        val = st.radio(question, options=[0, 1], format_func=lambda x: "Ya" if x == 1 else "Tidak", key=label)
        user_input[label] = val

# Input kategori -1/0/1
for i, (label, question) in enumerate(kategori_inputs.items()):
    with cols[(i + len(numerik_inputs) + len(yesno_inputs)) % 3]:
        val = st.radio(question[0], options=question[1], format_func=lambda x: {1: "Positif", 0: "Netral", -1: "Negatif"}[x], key=label)
        user_input[label] = val

# Prediksi
if st.button("Prediksi"):
    seq_feature = [
        user_input["NumDots"],
        user_input["SubdomainLevel"],
        user_input["PathLevel"],
        user_input["UrlLength"],
        user_input["NumDash"],
        user_input["NumDashInHostname"],
        user_input["AtSymbol"],
        user_input["TildeSymbol"],
        user_input["NumUnderscore"],
        user_input["NumPercent"],
        user_input["NumQueryComponents"],
        user_input["NumAmpersand"],
        user_input["NumHash"],
        user_input["NumNumericChars"],
        user_input["NoHttps"],
        user_input["RandomString"],
        user_input["IpAddress"],
        user_input["DomainInSubdomains"],
        user_input["DomainInPaths"],
        user_input["HostnameLength"],
        user_input["PathLength"],
        user_input["QueryLength"],
        user_input["DoubleSlashInPath"],
        user_input["NumSensitiveWords"],
        user_input["EmbeddedBrandName"],
        user_input["PctExtHyperlinks"],
        user_input["PctExtResourceUrls"],
        user_input["ExtFavicon"],
        user_input["InsecureForms"],
        user_input["RelativeFormAction"],
        user_input["ExtFormAction"],
        user_input["AbnormalFormAction"],
        user_input["PctNullSelfRedirectHyperlinks"],
        user_input["FrequentDomainNameMismatch"],
        user_input["FakeLinkInStatusBar"],
        user_input["RightClickDisabled"],
        user_input["PopUpWindow"],
        user_input["SubmitInfoToEmail"],
        user_input["IframeOrFrame"],
        user_input["MissingTitle"],
        user_input["ImagesOnlyInForm"],
        user_input["SubdomainLevelRT"],
        user_input["UrlLengthRT"],
        user_input["PctExtResourceUrlsRT"],
        user_input["AbnormalExtFormActionR"],
        user_input["ExtMetaScriptLinkRT"],
        user_input["PctExtNullSelfRedirectHyperlinksRT"]
    ]

    data = scaler.transform(np.array(seq_feature).reshape(1, -1))
    pred = model.predict(data)[0]
    label = "🔒 Legitimate" if pred == 0 else "🚨 Phishing"

    st.success(f"Hasil Prediksi: {label}")
   
#     st.write(pred)
#     st.write(data)
#     st.write(np.array(seq_feature).reshape(1, -1))

# st.table(user_input)