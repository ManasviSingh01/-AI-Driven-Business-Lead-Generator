# trade.py

import streamlit as st
import pandas as pd
import os
import plotly.express as px
from openai import OpenAI, AuthenticationError, RateLimitError

# === API KEY ===
API_KEY = "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"
client = OpenAI(api_key=API_KEY)

# === STREAMLIT SETUP ===
st.set_page_config(page_title="AI Lead Generator", page_icon="🤖")
st.title("🤖 AI-Driven Business Lead Generator")
st.markdown("Generate personalized outreach messages for trade leads using OpenAI.")

# === FILE UPLOAD ===
uploaded_file = st.file_uploader("Upload your trade leads CSV", type=["csv"])

# === SAMPLE DATA ===
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.info("Using sample data. Upload a CSV to override.")
    sample_data = {
        "Company Name": ["GlobalTradeX", "AgroWorld", "Meditech"],
        "Product": ["Solar Panels", "Organic Spices", "Medical Devices"],
        "Region": ["Europe", "South Asia", "Middle East"],
        "Email": ["contact@gtx.com", "info@agroworld.com", "hello@meditech.com"]
    }
    df = pd.DataFrame(sample_data)

# === CLEAN COLUMN NAMES ===
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# === FUNCTION TO GENERATE MESSAGE ===
def generate_message(company, product, region):
    prompt = (
        f"Write a short, professional outreach email for a trade lead.\n\n"
        f"Company: {company}\nProduct: {product}\nRegion: {region}\n\n"
        f"The message should express interest in partnership and be warm but formal."
    )
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except AuthenticationError:
        return "⚠️ Invalid API key. Please check your key and try again."
    except RateLimitError:
        return "⚠️ Rate limit exceeded. Please wait or upgrade your plan."
    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)}"

# === VALIDATE COLUMNS ===
required_cols = {"company_name", "product", "region"}
if not required_cols.issubset(df.columns):
    st.error(f"Missing required columns: {required_cols - set(df.columns)}")
    st.stop()

# === GENERATE MESSAGES ===
if st.button("✉️ Generate Outreach Messages"):
    with st.spinner("Generating messages..."):
        messages = []
        error_flag = False
        for _, row in df.iterrows():
            msg = generate_message(row["company_name"], row["product"], row["region"])
            messages.append(msg)
            if "rate limit" in msg.lower():
                error_flag = True
                break
        
        if error_flag:
            st.warning("⚠️ Generation stopped due to rate limit. Some rows may be incomplete.")
            df = df.iloc[:len(messages)]  # trim to match
        
        df["outreach_message"] = messages
        st.success("✅ Messages generated!")

# === SHOW RESULTS ===
if "outreach_message" in df.columns:
    st.subheader("📄 Leads and Generated Messages")
    st.dataframe(df)

    # === DOWNLOAD CSV ===
    csv = df.to_csv(index=False)
    st.download_button("⬇️ Download CSV", data=csv, file_name="outreach_messages.csv", mime="text/csv")

    # === VISUALIZATION ===
    st.subheader("📊 Message Distribution by Region")
    chart_data = df.groupby("region").size().reset_index(name="message_count")
    fig = px.bar(chart_data, x="region", y="message_count", color="region",
                 title="Outreach Messages per Region", labels={"message_count": "Messages"})
    st.plotly_chart(fig, use_container_width=True)













