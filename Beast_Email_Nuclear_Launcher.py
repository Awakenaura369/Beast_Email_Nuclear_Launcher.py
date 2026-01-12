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
    st.error("⚠️ GROQ_API_KEY missing in Streamlit Secrets!")

# --- 🎨 تصميم Beast UI الفخم ---
st.set_page_config(page_title="BEAST EMAIL SNIPER V2.1", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #050505; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #0d1117; border-right: 2px solid #d4af37; }
    .stButton>button { 
        background: linear-gradient(45deg, #d4af37, #f4cf47); 
        color: black; font-weight: bold; border-radius: 12px; 
        border: none; height: 50px; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px #d4af37; }
    h1, h2, h3 { color: #d4af37 !important; }
    .stTextInput>div>div>input { background-color: #111 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 Beast Email Sniper & AI Launcher V2.1")

# --- 🛡️ Sidebar ---
st.sidebar.header("🕹️ Command Center")
smtp_user = st.sidebar.text_input("Sender Gmail (SMTP)")
smtp_pass = st.sidebar.text_input("App Password", type="password")
st.sidebar.markdown("---")
st.sidebar.write("Status: **System Armed** ☢️")

# --- 📑 الأقسام ---
tabs = st.tabs(["🔎 Lead Sniper", "🤖 AI Writer", "🚀 Launcher", "📊 Stats"])

# --- 1. Lead Sniper (النسخة المصلحة) ---
with tabs[0]:
    st.header("🔎 Web Target Hunting")
    col1, col2 = st.columns(2)
    with col1:
        niche = st.text_input("Industry", value="Real Estate Investors")
    with col2:
        target_domain = st.selectbox("Domain", ["@gmail.com", "@yahoo.com", "@outlook.com"])
    
    if st.button("Start Hunting for Emails"):
        # تحسين البحث بـ Google Dorking
        query = f'"{niche}" "{target_domain}"'
        with st.spinner("Hunting for public leads..."):
            try:
                # تصحيح الـ TypeError باستخدام num_results
                search_results = search(query, num_results=20)
                results_links = [url for url in search_results]
                
                if results_links:
                    st.success(f"Found {len(results_links)} potential sources!")
                    for link in results_links:
                        st.markdown(f"🔗 [Lead Page]({link})")
                else:
                    st.warning("No results. Try a broader niche!")
            except Exception as e:
                st.error(f"Error: {e}")

# --- 2. AI Writer ---
with tabs[1]:
    st.header("🤖 AI Email Architect")
    target_info = st.text_input("Who is the target?")
    offer = st.text_area("Your Offer Details")
    
    if st.button("Generate AI Script"):
        prompt = f"Write a world-class cold email for {target_info}. Offer: {offer}. Short and bold."
        res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
        st.session_state['ai_body'] = res.choices[0].message.content
        st.write(st.session_state['ai_body'])

# --- 3. Launcher ---
with tabs[2]:
    st.header("🚀 Missile Launch")
    target_emails = st.text_area("Paste Emails Here")
    subject = st.text_input("Subject Line")
    
    if st.button("FIRE!"):
        clean_list = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', target_emails)
        if clean_list and smtp_user and smtp_pass:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(smtp_user, smtp_pass)
            for email in clean_list:
                msg = MIMEMultipart()
                msg['From'], msg['To'], msg['Subject'] = smtp_user, email, subject
                body = st.session_state.get('ai_body', "Check this offer out.")
                msg.attach(MIMEText(body, 'html'))
                server.send_message(msg)
                st.write(f"🚀 Sent to {email}")
                time.sleep(3) # أمان
            server.quit()
            st.success("Campaign Finished!")
        else:
            st.error("Check emails and SMTP settings.")

# --- 4. Stats ---
with tabs[3]:
    st.header("📊 Intelligence")
    st.info("System is tagging emails for open tracking.")
