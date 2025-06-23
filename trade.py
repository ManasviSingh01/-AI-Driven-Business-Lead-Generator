# trade.py

import streamlit as st
import pandas as pd
import plotly.express as px
import openai
from openai import OpenAIError, AuthenticationError, RateLimitError

# === HARD-CODED API KEY (Use your own key if needed) ===
openai.api_key = "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"

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
        "Company Name": ["GlobalTradeX", "AgroWorld", "Meditech", "EcoSolutions"],
        "Product": ["Solar Panels", "Organic Spices", "Medical Devices", "Eco-Friendly Packaging"],
        "Region": ["Europe", "South Asia", "Middle East", "North America"],
        "Email": ["contact@gtx.com", "info@agroworld.com", "hello@meditech.com", "eco@solutions.com"]
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
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            temperature=0.7
        )
        return response["choices"][0]["text"].strip()
    except AuthenticationError:
        return "⚠️ Invalid API key. Please check your key and try again."
    except RateLimitError:
        return "⚠️ Rate limit exceeded. Please wait or upgrade your plan."
    except OpenAIError as e:
        return f"⚠️ OpenAI error: {str(e)}"
    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)}"

# === VALIDATE COLUMNS ===
required_cols = {"company_name", "product", "region"}
if not required_cols.issubset(df.columns):
    st.error(f"Missing required columns: {required_cols - set(df.columns)}")
    st.write("Available columns:", df.columns.tolist())
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
            df = df.iloc[:len(messages)]

        df["outreach_message"] = messages
        st.success("✅ Messages generated!")

# === SHOW RESULTS ===
if "outreach_message" in df.columns:
    st.subheader("📄 Leads and Generated Messages")

    # Filter by region
    regions = df["region"].unique().tolist()
    selected_region = st.selectbox("Filter by Region", ["All"] + regions)
    filtered_df = df if selected_region == "All" else df[df["region"] == selected_region]
    st.dataframe(filtered_df)

    # === DOWNLOAD CSV ===
    csv = df.to_csv(index=False)
    st.download_button("⬇️ Download CSV", data=csv, file_name="outreach_messages.csv", mime="text/csv")

    # === STATS ===
    st.markdown(f"**Total Messages Generated:** {len(df)}")

    # === BAR CHART ===
    st.subheader("📊 Message Distribution by Region")
    chart_data = df.groupby("region").size().reset_index(name="message_count")
    fig = px.bar(chart_data, x="region", y="message_count", color="region",
                 title="Outreach Messages per Region", labels={"message_count": "Messages"})
    st.plotly_chart(fig, use_container_width=True)

    # === PIE CHART ===
    st.subheader("🧭 Region Share in Leads")
    pie_fig = px.pie(chart_data, names="region", values="message_count", title="Lead Distribution by Region")
    st.plotly_chart(pie_fig, use_container_width=True)















