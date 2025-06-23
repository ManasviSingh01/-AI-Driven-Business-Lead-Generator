# 🤖 AI-Driven Business Lead Generator

This project is a smart, AI-powered tool built using Python and Streamlit that generates personalized outreach messages for business trade leads. By combining lead data with OpenAI's language models, the tool helps sales and marketing teams automate communication while maintaining a professional, contextual tone.

---

## 🚀 Features

- 📄 Upload CSV files of trade leads (Company Name, Product, Region)
- ✨ Automatically generate customized outreach messages using GPT
- 📊 View region-wise distribution using bar and pie charts
- 💾 Export the final table with messages to CSV
- 🖼️ Visual interface powered by Streamlit — no coding required

---

## 📁 Sample Data Format

Ensure your CSV has the following headers:

```csv
Company Name, Product, Region, Email
AgriBoost, Hybrid Seeds, Africa, info@agriboost.af

🛠️ Tech Stack

Layer- Technology
UI- Streamlit
AI Engine- OpenAI GPT (text-davinci-003)
Data Handling- Pandas
Visuals- Plotly Express
File Support- CSV upload/download

📌 How It Works
Upload your CSV of trade leads (or use built-in sample data).
The app cleans column names (company_name, product, region).
For each row, a prompt is generated and sent to OpenAI’s GPT.
The AI returns a professional, friendly outreach message.
Messages are shown in a table and can be filtered/exported.

📊 Outreach Message Distribution by Region
![image](https://github.com/user-attachments/assets/0e41b850-9942-43f1-871f-9e5b08b03eb9)

🧭 Lead Share by Region
![image](https://github.com/user-attachments/assets/c4aaa9be-2919-44d8-bb7e-930162786d5a)

✅ Requirements

Python 3.8+
streamlit
openai
pandas
plotly

💡 Future Enhancements

🌍 Multilingual message generation
🔗 CRM integrations (HubSpot, Salesforce, Zoho)
✉️ Direct message delivery (Email, WhatsApp)
📈 Campaign analytics dashboard
🧠 Lead scoring with machine learning


If you find this project useful, don’t forget to ⭐ the repo and share it!
Let me know if you want:
- A `requirements.txt` file generated
- Deployment instructions (like for Streamlit Cloud or Hugging Face)
- A customized logo/banner





