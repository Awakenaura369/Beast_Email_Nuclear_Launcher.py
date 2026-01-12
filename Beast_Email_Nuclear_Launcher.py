import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from groq import Groq
from googlesearch import search
import re
import time
import uuid

# --- 🔐 إعدادات الربط (Secrets) ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ GROQ_API_KEY missing in Streamlit Secrets!")

# --- 🎨 واجهة الوحش (Beast UI Customization) ---
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
    h1, h2, h3 { color: #d4af37 !important; font-family: 'Inter', sans-serif; }
    .stTextInput>div>div>input { background-color: #111 !important; color: white !important; border: 1px solid #333; }
    .stTextArea>div>div>textarea { background-color: #111 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 Beast Email Sniper & AI Launcher V2.1")

# --- 🛡️ Control Panel (Sidebar) ---
st.sidebar.header("🕹️ Command Center")
smtp_user = st.sidebar.text_input("Sender Gmail (SMTP)", placeholder="yourname@gmail.com")
smtp_pass = st.sidebar.text_input("App Password", type="password", help="Use 'App Password' from Google Security settings.")
st.sidebar.markdown("---")
st.sidebar.write("System Status: **Ready to Hunt** ☢️")

# --- 📑 الأقسام (Tabs) ---
tabs = st.tabs(["🔎 Lead Sniper", "🤖 AI Content Architect", "🚀 Launch Missile", "📊 Intelligence"])

# --- 1. Lead Sniper (المعدل والمصلح) ---
with tabs[0]:
    st.header("🔎 Web Target Hunting")
    col1, col2 = st.columns(2)
    with col1:
        niche = st.text_input("Industry / Niche", value="Spiritual Coaches")
    with col2:
        target_domain = st.selectbox("Email Domain", ["@gmail.com", "@yahoo.com", "@outlook.com", "@hotmail.com"])
    
    if st.button("Start Hunting for Emails"):
        # صيغة Dorking احترافية
        query = f'site:instagram.com OR site:facebook.com "{niche}" "{target_domain}"'
        with st.spinner("Scouring social platforms for public leads..."):
            try:
                # الإصلاح: استخدام num_results بدلاً من num/stop لتفادي TypeError
                search_results = search(query, num_results=15)
                
                results_links = []
                for url in search_results:
                    results_links.append(url)
                
                if results_links:
                    st.success(f"Found {len(results_links)} high-potential source links!")
                    for link in results_links:
                        st.markdown(f"🔗 [Lead Source]({link})")
                    st.info("💡 Open links and copy public emails into the 'Launch' tab.")
                else:
                    st.warning("No public results found. Try changing the niche or domain.")
            except Exception as e:
                st.error(f"Search Module Error: {e}")

# --- 2. AI Content Architect ---
with tabs[1]:
    st.header("🤖 AI Email Copywriter")
    target_info = st.text_input("Who are you messaging? (e.g., Coaches wanting more clients)")
    offer_detail = st.text_area("Your Offer (e.g., Free Strategy Session, AI Ads Service)")
    
    if st.button("Generate Atomic Email Copy"):
        with st.spinner("AI is crafting the message..."):
            prompt = f"Write a world-class cold email for {target_info}. Our offer: {offer_detail}. Keep it bold, short, and high-converting."
            res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
            st.session_state['ai_email_body'] = res.choices[0].message.content
            st.success("Email Content Ready!")
            st.markdown("---")
            st.write(st.session_state['ai_email_body'])

# --- 3. Launch Missile ---
with tabs[2]:
    st.header("🚀 Nuclear Launch System")
    target_emails = st.text_area("Paste Target Emails (one per line)")
    email_subject = st.text_input("Email Subject Line")
    
    track_option = st.checkbox("Embed Tracking Pixel", value=True)
    
    if st.button("FIRE ALL MISSILES"):
        # تصفية الإيميلات
        clean_list = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', target_emails)
        
        if not clean_list:
            st.error("No valid emails detected!")
        elif not smtp_user or not smtp_pass:
            st.error("Set up SMTP in the sidebar first!")
        else:
            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(smtp_user, smtp_pass)
                
                progress = st.progress(0)
                for i, email in enumerate(clean_list):
                    msg = MIMEMultipart()
                    msg['From'] = smtp_user
                    msg['To'] = email
                    msg['Subject'] = email_subject
                    
                    body = st.session_state.get('ai_email_body', "Hello, I have something for you.")
                    if track_option:
                        body += f'<br><img src="https://your-tracking.com/pixel.png?id={uuid.uuid4()}" width="1" height="1" style="display:none;"/>'
                    
                    msg.attach(MIMEText(body, 'html'))
                    server.send_message(msg)
                    st.write(f"🚀 Missile sent to: {email}")
                    progress.progress((i + 1) / len(clean_list))
                    time.sleep(3) # أمان لتفادي السبام
                
                server.quit()
                st.success("Campaign Finished Successfully!")
            except Exception as e:
                st.error(f"Launch Error: {e}")

# --- 4. Intelligence ---
with tabs[3]:
    st.header("📊 Intelligence Report")
    st.write("Real-time open tracking would appear here if linked to a live backend server.")
    st.info("The system is currently tagging each email with a unique tracking ID.")

st.sidebar.markdown("---")
st.sidebar.write("🦁 **Beast Mode: Active**")
