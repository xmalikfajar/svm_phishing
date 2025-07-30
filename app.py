import streamlit as st
import pandas as pd
import joblib

# Load model dan scaler
model = joblib.load("svm_model.pkl")
scaler = joblib.load("scaler.pkl")

# Daftar nama fitur dari notebook (pastikan urutan sama!)
feature_names = [
    "NumDots", "SubdomainLevel", "PathLevel", "UrlLength", "NumDash",
    "NumDashInHostname", "AtSymbol", "TildeSymbol", "NumUnderscore", "NumPercent",
    "NumQueryComponents", "NumAmpersand", "NumHash", "NumNumericChars", "NoHttps",
    "RandomString", "IpAddress", "DomainInSubdomains", "DomainInPaths", "HostnameLength",
    "PathLength", "QueryLength", "DoubleSlashInPath", "NumSensitiveWords",
    "EmbeddedBrandName", "PctExtHyperlinks", "PctExtResourceUrls", "ExtFavicon",
    "InsecureForms", "RelativeFormAction", "ExtFormAction", "AbnormalFormAction",
    "PctNullSelfRedirectHyperlinks", "FrequentDomainNameMismatch", "FakeLinkInStatusBar",
    "RightClickDisabled", "PopUpWindow", "SubmitInfoToEmail", "IframeOrFrame",
    "MissingTitle", "ImagesOnlyInForm", "SubdomainLevelRT", "UrlLengthRT",
    "PctExtResourceUrlsRT", "AbnormalExtFormActionR", "ExtMetaScriptLinkRT",
    "PctExtNullSelfRedirectHyperlinksRT"
]

# Streamlit UI
st.set_page_config(page_title="Prediksi Phishing URL", layout="wide")
st.title("🔍 Deteksi URL Phishing")

st.markdown("Isi fitur URL secara manual untuk memprediksi apakah URL mengandung phishing.")

with st.form("input_form"):
    col1, col2 = st.columns(2)
    user_input = {}

    for i, feature in enumerate(feature_names):
        with (col1 if i % 2 == 0 else col2):
            user_input[feature] = st.number_input(feature, step=1)

    submitted = st.form_submit_button("🔍 Prediksi")

    if submitted:
        df_input = pd.DataFrame([user_input])
        df_scaled = scaler.transform(df_input)
        prediction = model.predict(df_scaled)[0]

        st.subheader("📊 Hasil Prediksi")
        if prediction == 1:
            st.error("⚠️ Tautan ini TERINDIKASI PHISHING.")
        else:
            st.success("✅ Tautan ini AMAN.")

        st.markdown("### 🔧 Data yang Anda Masukkan:")
        st.dataframe(df_input)
