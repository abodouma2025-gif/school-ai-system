import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import requests
import json
import hashlib
import os

# ==================== تكوين الصفحة ====================
st.set_page_config(
    page_title="نظام إدارة المدرسة الذكي",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== إعدادات DeepSeek API ====================
DEEPSEEK_API_KEY = st.secrets.get("DEEPSEEK_API_KEY", "YOUR_API_KEY_HERE")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# ==================== أنماط CSS الموحدة (الألوان الفاتحة) ====================
def load_css():
    st.markdown("""
    <style>
    /* الخلفية البيضاء الأساسية */
    .stApp {
        background-color: #F8F9FA;
        color: #212529;
    }
    
    /* تنسيق الأزرار باللون الأزرق المبهج */
    .stButton > button {
        background: linear-gradient(45deg, #007bff, #00d2ff) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 10px 24px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);
    }
    
    /* تنسيق الحقول Inputs */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: white !important;
        color: black !important;
        border: 1px solid #DEE2E6 !important;
        border-radius: 8px !important;
    }

    /* تنسيق البطاقات Cards */
    .custom-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        border: 1px solid #E0E0E0;
        color: #333;
    }
    
    /* تنسيق العناوين */
    h1, h2, h3 {
        color: #0056b3 !important;
    }

    /* شريط الأخبار */
    .news-ticker {
        background: #007bff;
        color: white;
        padding: 12px;
        border-radius: 12px;
        text-align: center;
        font-weight: bold;
    }

    /* ركن الأذكار */
    .dhikr-card {
        background: #E3F2FD;
        border-radius: 15px;
        padding: 25px;
        border: 2px solid #90CAF9;
        text-align: center;
        color: #0D47A1;
    }

    /* صندوق الطوارئ */
    .emergency-box {
        background: #FFF5F5;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #FFC9C9;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== دوال مساعدة ====================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(hashed_password, user_password):
    return hashed_password == hash_password(user_password)

def generate_deepseek_response(prompt, system_message="أنت مساعد تربوي متخصص"):
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        return "💡 وضع التجربة: الخدمة غير متوفرة حالياً."
    except:
        return "💡 خطأ في الاتصال بالخادم."

# ==================== تهيئة حالة الجلسة ====================
def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'user_type' not in st.session_state:
        st.session_state.user_type = ""
    if 'news' not in st.session_state:
        st.session_state.news = ["📢 بدء التسجيل للفصل الدراسي الثاني", "🏆 مسابقة التفوق العلمي"]
    if 'dhikr' not in st.session_state:
        st.session_state.dhikr = "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ"

# ==================== نظام تسجيل الدخول ====================
def login_system():
    st.markdown("<h1 style='text-align: center;'>🏫 نظام إدارة المدرسة الذكي</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("### 🔐 تسجيل الدخول")
        with st.form("login_form"):
            username = st.text_input("👤 اسم المستخدم (S للطالب / T للمدرس)")
            password = st.text_input("🔑 كلمة المرور", type="password")
            submitted = st.form_submit_button("🚀 دخول", use_container_width=True)
            
            if submitted:
                if username.startswith('T'):
                    teachers = {"T001": hash_password("teacher123")}
                    if username in teachers and check_password(teachers[username], password):
                        st.session_state.logged_in, st.session_state.username, st.session_state.user_type = True, username, "teacher"
                        st.rerun()
                    else: st.error("❌ خطأ في بيانات المدرس")
                elif username.startswith('S'):
                    students = {"S001": hash_password("student123")}
                    if username in students and check_password(students[username], password):
                        st.session_state.logged_in, st.session_state.username, st.session_state.user_type = True, username, "student"
                        st.rerun()
                    else: st.error("❌ خطأ في بيانات الطالب")
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== واجهة المدرس ====================
def teacher_dashboard():
    st.sidebar.title(f"👨‍🏫 مرحباً {st.session_state.username}")
    page = st.sidebar.radio("القائمة", ["الرئيسية", "المساعد التربوي", "الدرجات", "خروج"])
    
    if page == "الرئيسية":
        st.markdown("## 📊 لوحة التحكم")
        st.info(st.session_state.news[0])
    elif page == "المساعد التربوي":
        prob = st.text_area("وصف المشكلة")
        if st.button("اقتراح حل"):
            st.write(generate_deepseek_response(prob))
    elif page == "خروج":
        st.session_state.logged_in = False
        st.rerun()

# ==================== واجهة الطالب ====================
def student_dashboard():
    st.sidebar.title(f"🧑‍🎓 مرحباً {st.session_state.username}")
    page = st.sidebar.radio("القائمة", ["الرئيسية", "ركن الأذكار", "صندوق الضرورة", "خروج"])
    
    if page == "الرئيسية":
        st.markdown("<div class='news-ticker'>📢 أهلاً بك في مدرستك الذكية</div>", unsafe_allow_html=True)
    elif page == "ركن الأذكار":
        st.markdown(f"<div class='dhikr-card'>{st.session_state.dhikr}</div>", unsafe_allow_html=True)
    elif page == "صندوق الضرورة":
        with st.form("emergency"):
            msg = st.text_area("كيف نساعدك؟")
            if st.form_submit_button("إرسال"):
                st.success("تم الإرسال للمرشد الطلابي")
    elif page == "خروج":
        st.session_state.logged_in = False
        st.rerun()

# ==================== التشغيل الرئيسي ====================
def main():
    load_css()
    init_session_state()
    if not st.session_state.logged_in:
        login_system()
    else:
        if st.session_state.user_type == "teacher":
            teacher_dashboard()
        else:
            student_dashboard()

if __name__ == "__main__":
    main()
