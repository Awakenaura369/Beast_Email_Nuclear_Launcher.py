import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from groq import Groq
from googlesearch import search
import re
import time
import uuid

# --- 🔐 إعدادات الأمان والربط مع الوحش ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ GROQ_API_KEY is missing in Streamlit Secrets!")

# --- 🎨 تصميم واجهة الوحش (Beast UI) ---
st.set_page_config(page_title="BEAST EMAIL SNIPER V2", layout="wide")

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
    .stTextInput>div>div>input { background-color: #111 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 Beast Email Sniper & AI Launcher V2")

# --- 🛡️ Command Center (Sidebar) ---
st.sidebar.header("🕹️ Control Panel")
smtp_user = st.sidebar.text_input("Sender Gmail (SMTP)", placeholder="example@gmail.com")
smtp_pass = st.sidebar.text_input("App Password", type="password", help="Get this from Google Account > Security > App Passwords")
st.sidebar.markdown("---")
st.sidebar.warning("🛡️ Safety Tip: Send max 50-100 emails/day to keep your account safe.")

# --- 📑 الأقسام الرئيسية (Tabs) ---
tabs = st.tabs(["🔎 Lead Sniper", "🤖 AI Content Architect", "🚀 Launch Missile", "📊 Tracking Intelligence"])

# --- 1. القسم الأول: صيد الإيميلات (Sniper) ---
with tabs[0]:
    st.header("🔎 Web Target Hunting")
    col1, col2 = st.columns(2)
    with col1:
        niche = st.text_input("Industry / Niche", placeholder="e.g. Roofers, Agency Owners")
    with col2:
        target_domain = st.selectbox("Email Provider", ["@gmail.com", "@yahoo.com", "@outlook.com", "@hotmail.com"])
    
    if st.button("Start Hunting for Emails"):
        # منطق الـ Google Dorking المتقدم
        query = f'site:facebook.com OR site:instagram.com OR site:linkedin.com "{niche}" "{target_domain}"'
        with st.spinner("Scouring social platforms for public emails..."):
            results = []
            for url in search(query, num=15, stop=15, pause=2):
                results.append(url)
            
            st.success(f"Found {len(results)} high-potential source links!")
            for link in results:
                st.markdown(f"🔗 [Potential Lead Source]({link})")
            st.info("💡 Copy the emails from these pages and paste them in the Launcher tab.")

# --- 2. القسم الثاني: هندسة المحتوى بـ AI ---
with tabs[1]:
    st.header("🤖 AI Email Copywriter")
    target_description = st.text_input("Describe your target audience precisely")
    value_prop = st.text_area("What is your unique offer / value proposition?")
    
    if st.button("Generate Atomic Email Copy"):
        with st.spinner("Groq AI is analyzing psychology..."):
            prompt = f"""
            You are a world-class cold email specialist. 
            Write a high-converting, short, and punchy cold email for: {target_description}.
            Our Offer: {value_prop}.
            Style: Bold, Professional, Curious. No spammy words.
            """
            res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
            st.session_state['ai_email_body'] = res.choices[0].message.content
            st.success("Email Content Ready!")
            st.markdown("---")
            st.write(st.session_state['ai_email_body'])

# --- 3. القسم الثالث: الإطلاق (Launcher) ---
with tabs[2]:
    st.header("🚀 Nuclear Launch System")
    target_emails = st.text_area("Paste Target Emails (one per line)")
    email_subject = st.text_input("Email Subject Line")
    
    track_option = st.checkbox("Embed Tracking Pixel (Identify Opens)", value=True)
    
    if st.button("FIRE ALL MISSILES"):
        # تنظيف القائمة باستخدام Regex
        clean_list = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', target_emails)
        
        if not clean_list:
            st.error("No valid emails found in the list!")
        elif not smtp_user or not smtp_pass:
            st.error("Please setup SMTP in the sidebar first!")
        else:
            try:
                # الاتصال بسيرفر جوجل
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(smtp_user, smtp_pass)
                
                progress_bar = st.progress(0)
                for i, target_email in enumerate(clean_list):
                    msg = MIMEMultipart()
                    msg['From'] = smtp_user
                    msg['To'] = target_email
                    msg['Subject'] = email_subject
                    
                    # صياغة الرسالة مع بيكسل التتبع
                    content = st.session_state.get('ai_email_body', "Hello, checking in...")
                    if track_option:
                        track_id = str(uuid.uuid4())
                        # رابط وهمي للتتبع (يحتاج سيرفر للاشتغال الحقيقي)
                        tracking_pixel = f'<img src="https://your-server.com/track/{track_id}.png" width="1" height="1" style="display:none;" />'
                        content += tracking_pixel
                    
                    msg.attach(MIMEText(content, 'html'))
                    server.send_message(msg)
                    
                    st.write(f"🚀 Sent to: {target_email}")
                    progress_bar.progress((i + 1) / len(clean_list))
                    time.sleep(3) # فجوة أمان لعدم حظر الحساب
                
                server.quit()
                st.success(f"Mission Accomplished! {len(clean_list)} emails sent.")
            except Exception as e:
                st.error(f"Launch Failed: {e}")

# --- 4. القسم الرابع: التتبع والاستخبارات ---
with tabs[3]:
    st.header("📊 Intelligence & Tracking")
    render_beast_card = """
    <div style="background: #111; padding: 20px; border-radius: 15px; border: 1px solid #d4af37; text-align: center;">
        <h3 style="margin:0;">Email Open Rate</h3>
        <h1 style="color: #d4af37; font-size: 3em;">-- %</h1>
        <p>Real-time tracking requires a hosted backend (Flask/FastAPI).</p>
    </div>
    """
    st.components.v1.html(render_beast_card, height=200)
    st.info("The tracking pixel is working. To see live data, you must link this app to a logging database.")

st.sidebar.markdown("---")
st.sidebar.info("Beast Sniper V2.0 - Developed for Marketing Legends")
