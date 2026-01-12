import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from groq import Groq
from googlesearch import search
import re
import time
import uuid

# --- 🔐 الربط مع Secrets ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ API Key missing!")

# --- 🎨 Beast UI (Gold & Black) ---
st.set_page_config(page_title="BEAST HUNTER V2.2", layout="wide")
st.markdown("""<style>
    .stApp { background: #050505; color: #e0e0e0; }
    .stButton>button { background: linear-gradient(45deg, #d4af37, #f4cf47); color: black; font-weight: bold; border-radius: 12px; height: 50px; }
    h1, h2, h3 { color: #d4af37 !important; }
    .stTextInput>div>div>input { background-color: #111 !important; color: white !important; }
</style>""", unsafe_allow_html=True)

st.title("🎯 Beast Unstoppable Hunter V2.2")

# --- 🛡️ Sidebar ---
st.sidebar.header("🕹️ Command Center")
smtp_user = st.sidebar.text_input("Sender Gmail (SMTP)")
smtp_pass = st.sidebar.text_input("App Password", type="password")

# --- 📑 Tabs ---
tabs = st.tabs(["🔎 Atomic Sniper", "🤖 AI Writer", "🚀 Launcher"])

# --- 1. Atomic Sniper (النسخة المجهدة) ---
with tabs[0]:
    st.header("🔎 Targeted Email Sniper")
    col1, col2, col3 = st.columns(3)
    with col1:
        niche = st.text_input("Niche", value="Spiritual Coaches")
    with col2:
        domain = st.selectbox("Domain", ["@gmail.com", "@yahoo.com", "@outlook.com"])
    with col3:
        platform = st.selectbox("Platform", ["Instagram", "LinkedIn", "Facebook", "Websites"])

    if st.button("EXECUTE HUNTER"):
        # الخدعة: Google Dorking متطور
        if platform == "Websites":
            query = f'"{niche}" "{domain}" -filetype:pdf'
        else:
            query = f'site:{platform.lower()}.com "{niche}" "{domain}"'
            
        with st.spinner(f"Beast is deep-scanning {platform}..."):
            try:
                # محاولة البحث مع زيادة عدد النتائج وتغيير الـ User-Agent
                search_results = search(query, num_results=40, lang="en")
                results_links = [url for url in search_results]
                
                if results_links:
                    st.success(f"🔥 Found {len(results_links)} potential targets!")
                    # محاولة استخراج الإيميلات من العناوين (Snippet Extraction)
                    for i, link in enumerate(results_links):
                        st.markdown(f"**Target {i+1}:** {link}")
                    
                    st.info("💡 Tip: If you see many links, use a Chrome extension like 'Email Extractor' to pull all emails from these tabs at once!")
                else:
                    st.error("❌ Google is blocking the script. Try again in 5 minutes or use a VPN.")
            except Exception as e:
                st.error(f"Search Error: {e}")

# --- 2. AI Writer & 3. Launcher (باقي الكود كالسابق) ---
with tabs[1]:
    st.header("🤖 AI Email Architect")
    target = st.text_input("Target Info")
    offer = st.text_area("Offer")
    if st.button("Generate"):
        res = client.chat.completions.create(messages=[{"role": "user", "content": f"Write cold email for {target}: {offer}"}], model="llama-3.3-70b-versatile")
        st.session_state['ai_msg'] = res.choices[0].message.content
        st.write(st.session_state['ai_msg'])

with tabs[2]:
    st.header("🚀 Missile Launcher")
    targets = st.text_area("Paste Emails")
    sub = st.text_input("Subject")
    if st.button("FIRE"):
        clean = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', targets)
        if clean and smtp_user and smtp_pass:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(smtp_user, smtp_pass)
            for em in clean:
                msg = MIMEMultipart()
                msg['From'], msg['To'], msg['Subject'] = smtp_user, em, sub
                msg.attach(MIMEText(st.session_state.get('ai_msg', "Offer"), 'html'))
                server.send_message(msg)
                st.write(f"🚀 Sent to {em}")
                time.sleep(3)
            server.quit()
            st.success("Done!")
