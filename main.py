import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import requests
import json
import hashlib
import os
from PIL import Image
import base64
import time

# ==================== تكوين الصفحة ====================
st.set_page_config(
    page_title="نظام إدارة المدرسة الذكي",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== إعدادات DeepSeek API ====================
DEEPSEEK_API_KEY = st.secrets.get("DEEPSEEK_API_KEY", "YOUR_API_KEY_HERE")  # ضع مفتاح API هنا
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# ==================== أنماط CSS للوضع الليلي ====================
def load_css():
    st.markdown("""
    <style>
    /* الوضع الليلي الأساسي */
    .stApp {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    /* تنسيق الأزرار */
.stButton > button {
        background: linear-gradient(45deg, #007bff, #00d2ff);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);
    }
    
    /* تنسيق البطاقات */
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
        font-weight: bold !important;
    }
    
    /* تنسيق الأيقونات */
    .icon-text {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 10px;
    }
    
    /* تنسيق شريط الأخبار */
.news-ticker {
        background: #007bff;
        color: white;
        padding: 12px;
        border-radius: 12px;
        text-align: center;
        font-weight: bold;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.8; }
        100% { opacity: 1; }
    }
    
    /* تنسيق لوحة الأخبار */
.news-board {
        background: white;
        border-radius: 10px;
        padding: 15px;
        border-right: 5px solid #007bff;
        color: #444;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* تنسيق ركن الأذكار */
.dhikr-card {
        background: #E3F2FD;
        border-radius: 15px;
        padding: 25px;
        border: 2px solid #90CAF9;
        text-align: center;
        color: #0D47A1;
    }
    
    /* تنسيق صندوق الضرورة */
    .emergency-box {
        background: #2d2d2d;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #ff6b6b;
    }
    
/* التبويبات (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #E0E0E0;
        border-radius: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #007bff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== دوال مساعدة ====================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(hashed_password, user_password):
   # نموذج تسجيل الدخول
        with st.form("login_form"):
            username = st.text_input("اسم المستخدم (S للطالب / T للمدرس)")
            password = st.text_input("كلمة المرور", type="password")
            submitted = st.form_submit_button("دخول")
            
            if submitted:
                if username and password:
                    # التحقق من نوع المستخدم (مدرس)
                    if username.startswith('T'):
                        teachers = {"T001": hash_password("teacher123"), "T002": hash_password("teacher456")}
                        if username in teachers and check_password(teachers[username], password):
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.session_state.user_type = "teacher"
                            st.success("✅ أهلاً بك يا أستاذ!")
                            st.rerun()
                        else:
                            st.error("❌ بيانات المدرس غير صحيحة")
                    
                    # التحقق من نوع المستخدم (طالب)
                    elif username.startswith('S'):
                        students = {"S001": hash_password("student123"), "S002": hash_password("student456")}
                        if username in students and check_password(students[username], password):
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.session_state.user_type = "student"
                            st.success("✅ بالتوفيق يا بطل!")
                            st.rerun()
                        else:
                            st.error("❌ بيانات الطالب غير صحيحة")
                    else:
                        st.error("❌ ابدأ بـ T للمدرس أو S للطالب")
        border: 1px solid #CCC !important
    }
    
    /* تنسيق المعلومات الجانبية */
    .info-box {
        background-color: #2d2d2d;
        border-left: 4px solid #667eea;
        padding: 10px;
        margin: 10px 0;
    }
    
    /* تنسيق الأقسام */
    .section-header {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== دوال مساعدة ====================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(hashed_password, user_password):
    return hashed_password == hash_password(user_password)

def generate_deepseek_response(prompt, system_message="أنت مساعد تربوي متخصص في مجال التعليم"):
    """توليد رد باستخدام DeepSeek API"""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return "عذراً، حدث خطأ في الاتصال بـ DeepSeek API"
    except Exception as e:
        return f"خطأ في الاتصال: {str(e)}"

# ==================== تهيئة حالة الجلسة ====================
def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'user_type' not in st.session_state:
        st.session_state.user_type = ""
    if 'news' not in st.session_state:
        st.session_state.news = [
            "📢 بدء التسجيل للفصل الدراسي الثاني",
            "🏆 مسابقة التفوق العلمي الأسبوع القادم",
            "📚 اجتماع أولياء الأمور يوم الخميس"
        ]
    if 'dhikr' not in st.session_state:
        st.session_state.dhikr = generate_dhikr()

def generate_dhikr():
    """توليد ذكر يومي"""
    dhikr_list = [
        "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ، سُبْحَانَ اللَّهِ الْعَظِيمِ",
        "اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّدٍ",
        "لا إِلَهَ إِلا أَنْتَ سُبْحَانَكَ إِنِّي كُنْتُ مِنَ الظَّالِمِينَ",
        "حَسْبِيَ اللَّهُ لا إِلَهَ إِلا هُوَ عَلَيْهِ تَوَكَّلْتُ وَهُوَ رَبُّ الْعَرْشِ الْعَظِيمِ",
        "اللَّهُمَّ أَنْتَ رَبِّي لا إِلَهَ إِلا أَنْتَ، عَلَيْكَ تَوَكَّلْتُ، وَأَنْتَ رَبُّ الْعَرْشِ الْعَظِيمِ"
    ]
    return np.random.choice(dhikr_list)

# ==================== نظام تسجيل الدخول ====================
def login_system():
    st.markdown("<h1 style='text-align: center;'>🏫 نظام إدارة المدرسة الذكي</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.container():
            st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
            
            st.markdown("### 🔐 تسجيل الدخول")
            
            # نموذج تسجيل الدخول
            with st.form("login_form"):
                username = st.text_input("👤 اسم المستخدم", placeholder="أدخل اسم المستخدم...")
                password = st.text_input("🔑 كلمة المرور", type="password", placeholder="أدخل كلمة المرور...")
                
                col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
                with col_btn2:
                    submitted = st.form_submit_button("🚀 دخول", use_container_width=True)
                
                if submitted:
                    if username and password:
                        # التحقق من نوع المستخدم
                        if username.startswith('T'):
                            # بيانات المدرسين (في نظام حقيقي ستكون في قاعدة بيانات)
                            teachers = {
                                "T001": hash_password("teacher123"),
                                "T002": hash_password("teacher456")
                            }
                            if username in teachers and check_password(teachers[username], password):
                                st.session_state.logged_in = True
                                st.session_state.username = username
                                st.session_state.user_type = "teacher"
                                st.success("✅ تم تسجيل الدخول بنجاح!")
                                st.rerun()
                            else:
                                st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")
                        
                        elif username.startswith('S'):
                            # بيانات الطلاب
                            students = {
                                "S001": hash_password("student123"),
                                "S002": hash_password("student456")
                            }
                            if username in students and check_password(students[username], password):
                                st.session_state.logged_in = True
                                st.session_state.username = username
                                st.session_state.user_type = "student"
                                st.success("✅ تم تسجيل الدخول بنجاح!")
                                st.rerun()
                            else:
                                st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")
                        
                        else:
                            st.error("❌ اسم المستخدم يجب أن يبدأ بـ T للمدرس أو S للطالب")
            
            st.markdown("</div>", unsafe_allow_html=True)

# ==================== واجهة المدرس ====================
def teacher_dashboard():
    st.markdown(f"<h1>👨‍🏫 مرحباً أيها المدرس {st.session_state.username}</h1>", unsafe_allow_html=True)
    
    # القائمة الجانبية
    with st.sidebar:
        st.markdown("## 🧭 القائمة الرئيسية")
        
        if st.button("🏠 الرئيسية", use_container_width=True):
            st.session_state.page = "main"
        if st.button("📻 الإذاعة المدرسية", use_container_width=True):
            st.session_state.page = "radio"
        if st.button("📿 الأذكار", use_container_width=True):
            st.session_state.page = "dhikr"
        if st.button("👨‍🏫 المساعد التربوي", use_container_width=True):
            st.session_state.page = "assistant"
        if st.button("📊 الدرجات", use_container_width=True):
            st.session_state.page = "grades"
        if st.button("📝 التحضير", use_container_width=True):
            st.session_state.page = "preparation"
        if st.button("🚪 تسجيل الخروج", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.user_type = ""
            st.rerun()
    
    # تحديد الصفحة المعروضة
    if 'page' not in st.session_state:
        st.session_state.page = "main"
    
    # عرض المحتوى حسب الصفحة المختارة
    if st.session_state.page == "main":
        show_teacher_main()
    elif st.session_state.page == "radio":
        show_radio_section()
    elif st.session_state.page == "dhikr":
        show_dhikr_section()
    elif st.session_state.page == "assistant":
        show_assistant_section()
    elif st.session_state.page == "grades":
        show_grades_section()
    elif st.session_state.page == "preparation":
        show_preparation_section()

def show_teacher_main():
    st.markdown("## 📊 لوحة التحكم الرئيسية")
    
    # إحصائيات سريعة
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='custom-card' style='text-align: center;'>
            <h3>👥 25</h3>
            <p>عدد الطلاب</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='custom-card' style='text-align: center;'>
            <h3>📚 6</h3>
            <p>المواد الدراسية</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='custom-card' style='text-align: center;'>
            <h3>⭐ 15</h3>
            <p>طلاب متفوقين</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='custom-card' style='text-align: center;'>
            <h3>📅 85%</h3>
            <p>نسبة الحضور</p>
        </div>
        """, unsafe_allow_html=True)
    
    # آخر الأخبار
    st.markdown("## 📰 آخر الأخبار")
    
    for i, news_item in enumerate(st.session_state.news):
        st.markdown(f"""
        <div class='news-board'>
            📌 {news_item}
        </div>
        <br>
        """, unsafe_allow_html=True)
    
    # إضافة خبر جديد
    with st.expander("➕ إضافة خبر جديد"):
        new_news = st.text_area("نص الخبر", placeholder="أدخل نص الخبر هنا...")
        if st.button("إضافة الخبر", use_container_width=True):
            if new_news:
                st.session_state.news.append(new_news)
                st.success("✅ تم إضافة الخبر بنجاح!")
                st.rerun()

def show_radio_section():
    st.markdown("## 📻 الإذاعة المدرسية الذكية")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class='custom-card'>
            <h3>📝 إنشاء إذاعة جديدة</h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("radio_form"):
            title = st.text_input("عنوان الإذاعة", placeholder="أدخل عنوان الإذاعة...")
            theme = st.selectbox("موضوع الإذاعة", 
                               ["عام", "ديني", "علمي", "ثقافي", "رياضي", "اجتماعي"])
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                submitted = st.form_submit_button("🎙️ توليد الإذاعة", use_container_width=True)
            
            if submitted and title:
                with st.spinner("جاري توليد الإذاعة..."):
                    prompt = f"""
                    اكتب سيناريو كامل للإذاعة المدرسية بعنوان: {title}
                    الموضوع: {theme}
                    
                    يجب أن يحتوي السيناريو على:
                    1. مقدمة مميزة
                    2. فقرة الحديث الشريف
                    3. حكمة اليوم
                    4. فقرة هل تعلم (3 معلومات)
                    
                    اجعل السيناريو مناسباً للإذاعة المدرسية.
                    """
                    
                    response = generate_deepseek_response(prompt, "أنت مقدم إذاعة مدرسية محترف")
                    
                    if response:
                        st.session_state.radio_script = response
                        st.success("✅ تم توليد الإذاعة بنجاح!")
    
    with col2:
        if 'radio_script' in st.session_state:
            st.markdown("""
            <div class='custom-card'>
                <h3>🎯 الإذاعة المولدة</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(st.session_state.radio_script)
            
            # أزرار للتفاعل
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                if st.button("📋 نسخ", use_container_width=True):
                    st.info("تم النسخ!")
            with col_d2:
                if st.button("💾 حفظ", use_container_width=True):
                    st.success("تم الحفظ!")

def show_dhikr_section():
    st.markdown("## 📿 الأذكار اليومية")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class='custom-card'>
            <h3>🤲 ذكر اليوم</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='dhikr-card'>
            <h2>📖</h2>
            <p style='font-size: 24px;'>{st.session_state.dhikr}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 توليد ذكر جديد", use_container_width=True):
            with st.spinner("جاري توليد ذكر جديد..."):
                prompt = "اكتب ذكراً أو دعاءً مميزاً من الأذكار النبوية"
                response = generate_deepseek_response(prompt, "أنت متخصص في الأذكار والأدعية")
                
                if response:
                    st.session_state.dhikr = response
                    st.rerun()
    
    with col2:
        st.markdown("""
        <div class='custom-card'>
            <h3>📚 بنك الأذكار</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # عرض أذكار متنوعة
        adhkar = [
            "اللهم إني أسألك علماً نافعاً، ورزقاً طيباً، وعملاً متقبلاً",
            "ربِّ زدني علماً، وألحقني بالصالحين",
            "اللهم انفعني بما علمتني، وعلمني ما ينفعني"
        ]
        
        for dhikr in adhkar:
            st.markdown(f"""
            <div class='info-box'>
                {dhikr}
            </div>
            """, unsafe_allow_html=True)

def show_assistant_section():
    st.markdown("## 👨‍🏫 المساعد التربوي الذكي")
    
    st.markdown("""
    <div class='section-header'>
        <h3 style='color: white;'>اطرح مشكلة تربوية واحصل على حلول ذكية</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        with st.form("problem_form"):
            student_name = st.text_input("اسم الطالب", placeholder="أدخل اسم الطالب...")
            problem_type = st.selectbox("نوع المشكلة",
                                      ["سلوكية", "دراسية", "اجتماعية", "نفسية", "أخرى"])
            problem_description = st.text_area("وصف المشكلة",
                                              placeholder="صف المشكلة بالتفصيل...",
                                              height=150)
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                submitted = st.form_submit_button("💡 اقتراح حل", use_container_width=True)
            
            if submitted and problem_description:
                with st.spinner("جاري تحليل المشكلة واقتراح الحلول..."):
                    prompt = f"""
                    مشكلة طالب:
                    - الاسم: {student_name}
                    - نوع المشكلة: {problem_type}
                    - الوصف: {problem_description}
                    
                    قدم حلاً تربوياً ذكياً للمشكلة يتضمن:
                    1. تحليل المشكلة
                    2. خطة علاجية مقترحة
                    3. نصائح للتعامل مع الطالب
                    4. طرق متابعة التقدم
                    """
                    
                    response = generate_deepseek_response(prompt, "أنت مستشار تربوي خبير")
                    
                    if response:
                        st.session_state.solution = response
                        st.success("✅ تم اقتراح الحل!")
    
    with col2:
        if 'solution' in st.session_state:
            st.markdown("""
            <div class='custom-card'>
                <h3>💡 الحلول المقترحة</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(st.session_state.solution)
            
            if st.button("📥 حفظ الحل", use_container_width=True):
                st.success("تم حفظ الحل في قاعدة البيانات!")

def show_grades_section():
    st.markdown("## 📊 نظام الدرجات")
    
    # بيانات تجريبية للدرجات
    grades_data = {
        "الطالب": ["أحمد محمد", "سارة علي", "عمر خالد", "فاطمة أحمد"],
        "الرياضيات": [95, 88, 92, 78],
        "العلوم": [88, 92, 85, 90],
        "اللغة العربية": [90, 85, 88, 92],
        "اللغة الإنجليزية": [85, 90, 87, 88]
    }
    
    df_grades = pd.DataFrame(grades_data)
    
    # عرض الدرجات
    st.markdown("### 📋 جدول الدرجات")
    st.dataframe(df_grades, use_container_width=True)
    
    # إحصائيات
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📈 متوسط الدرجات", "88.5", "+2.5")
    with col2:
        st.metric("🏆 أعلى درجة", "95", "الرياضيات")
    with col3:
        st.metric("📊 عدد الطلاب المتفوقين", "3", "+1")
    
    # إضافة درجة جديدة
    with st.expander("➕ إضافة درجة جديدة"):
        with st.form("add_grade"):
            student = st.selectbox("اختر الطالب", grades_data["الطالب"])
            subject = st.selectbox("المادة", ["الرياضيات", "العلوم", "اللغة العربية", "اللغة الإنجليزية"])
            grade = st.number_input("الدرجة", min_value=0, max_value=100)
            
            if st.form_submit_button("حفظ الدرجة"):
                st.success(f"✅ تم إضافة درجة {grade} للطالب {student} في مادة {subject}")

def show_preparation_section():
    st.markdown("## 📝 التحضير اليومي")
    
    # اختيار المادة
    subject = st.selectbox("اختر المادة", ["الرياضيات", "العلوم", "اللغة العربية", "اللغة الإنجليزية"])
    
    # بيانات التحضير
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='custom-card'>
            <h3>📅 تحضير اليوم</h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("preparation_form"):
            date = st.date_input("التاريخ", datetime.now())
            lesson = st.text_input("عنوان الدرس")
            objectives = st.text_area("الأهداف التعليمية")
            materials = st.text_input("الوسائل التعليمية")
            
            if st.form_submit_button("💾 حفظ التحضير"):
                st.success("✅ تم حفظ التحضير بنجاح!")
    
    with col2:
        st.markdown("""
        <div class='custom-card'>
            <h3>📊 التحضيرات السابقة</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # عرض تحضيرات سابقة (بيانات تجريبية)
        preparations = [
            "📚 درس الجبر - 2024-01-15",
            "🔬 التجارب العلمية - 2024-01-14",
            "📖 قواعد اللغة - 2024-01-13"
        ]
        
        for prep in preparations:
            st.markdown(f"""
            <div class='info-box'>
                {prep}
            </div>
            """, unsafe_allow_html=True)

# ==================== واجهة الطالب ====================
def student_dashboard():
    st.markdown(f"<h1>🧑‍🎓 مرحباً أيها الطالب {st.session_state.username}</h1>", unsafe_allow_html=True)
    
    # القائمة الجانبية للطالب
    with st.sidebar:
        st.markdown("## 🧭 القائمة الرئيسية")
        
        if st.button("🏠 الرئيسية", use_container_width=True):
            st.session_state.student_page = "main"
        if st.button("📿 ركن الأذكار", use_container_width=True):
            st.session_state.student_page = "dhikr"
        if st.button("🚨 صندوق الضرورة", use_container_width=True):
            st.session_state.student_page = "emergency"
        if st.button("📚 جدولي الدراسي", use_container_width=True):
            st.session_state.student_page = "schedule"
        if st.button("🚪 تسجيل الخروج", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.user_type = ""
            st.rerun()
    
    # تحديد الصفحة المعروضة
    if 'student_page' not in st.session_state:
        st.session_state.student_page = "main"
    
    # عرض المحتوى حسب الصفحة المختارة
    if st.session_state.student_page == "main":
        show_student_main()
    elif st.session_state.student_page == "dhikr":
        show_student_dhikr()
    elif st.session_state.student_page == "emergency":
        show_emergency_box()
    elif st.session_state.student_page == "schedule":
        show_student_schedule()

def show_student_main():
    st.markdown("## 📰 لوحة الأخبار")
    
    # شريط الأخبار المتحرك
    st.markdown("""
    <div class='news-ticker'>
        📢 آخر الأخبار والتحديثات المدرسية
    </div>
    """, unsafe_allow_html=True)
    
    # عرض الأخبار
    for i, news_item in enumerate(st.session_state.news):
        st.markdown(f"""
        <div class='news-board'>
            <span style='font-size: 20px;'>📌</span> {news_item}
            <br>
            <small>🕒 {datetime.now().strftime('%Y-%m-%d')}</small>
        </div>
        <br>
        """, unsafe_allow_html=True)
    
    # أنشطة اليوم
    st.markdown("## 📅 أنشطة اليوم")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='custom-card' style='text-align: center;'>
            <h3>📚</h3>
            <p>حصة الرياضيات</p>
            <small>8:00 - 9:00</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='custom-card' style='text-align: center;'>
            <h3>🔬</h3>
            <p>مختبر العلوم</p>
            <small>9:00 - 10:00</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='custom-card' style='text-align: center;'>
            <h3>⚽</h3>
            <p>نشاط رياضي</p>
            <small>10:00 - 11:00</small>
        </div>
        """, unsafe_allow_html=True)

def show_student_dhikr():
    st.markdown("## 📿 ركن الأذكار")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class='dhikr-card'>
            <h2>ذكر اليوم</h2>
            <p style='font-size: 24px; margin: 20px 0;'>{}</p>
            <p style='color: #667eea;'>🔁 تحديث يومي</p>
        </div>
        """.format(st.session_state.dhikr), unsafe_allow_html=True)
        
        # أذكار الصباح والمساء
        st.markdown("### 🌅 أذكار الصباح والمساء")
        
        morning_dhikr = [
            "اللهم بك أصبحنا وبك أمسينا، وبك نحيا وبك نموت وإليك النشور",
            "أصبحنا وأصبح الملك لله رب العالمين",
            "اللهم ما أصبح بي من نعمة فمنك وحدك لا شريك لك"
        ]
        
        for dhikr in morning_dhikr:
            st.markdown(f"""
            <div class='info-box'>
                {dhikr}
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### ⭐ فضل الذكر")
        st.markdown("""
        <div class='custom-card'>
            <p>🔹 سبب لدخول الجنة</p>
            <p>🔹 طمأنينة القلب</p>
            <p>🔹 زيادة الحسنات</p>
            <p>🔹 حفظ من الشرور</p>
            <p>🔹 سبب لذكر الله لنا</p>
        </div>
        """, unsafe_allow_html=True)

def show_emergency_box():
    st.markdown("## 🚨 صندوق الضرورة")
    
    st.markdown("""
    <div class='emergency-box'>
        <h3 style='color: #ff6b6b;'>⚠️ للإبلاغ عن حالات طارئة أو طلب المساعدة</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("emergency_form"):
            emergency_type = st.selectbox("نوع المشكلة",
                                        ["مشكلة دراسية", "مشكلة مع زميل", "استشارة", "طلب مساعدة", "أخرى"])
            emergency_description = st.text_area("وصف المشكلة",
                                                placeholder="اكتب مشكلتك بالتفصيل...",
                                                height=150)
            contact_method = st.radio("طريقة التواصل",
                                     ["البريد الإلكتروني", "اللقاء الشخصي", "الاتصال الهاتفي"])
            
            submitted = st.form_submit_button("📤 إرسال", use_container_width=True)
            
            if submitted and emergency_description:
                st.success("✅ تم إرسال مشكلتك، سيتواصل معك المرشد الطلابي قريباً")
                st.balloons()
    
    with col2:
        st.markdown("### 📞 أرقام الطوارئ")
        st.markdown("""
        <div class='custom-card'>
            <p><strong>🚑 إسعاف:</strong> 123</p>
            <p><strong>👮 شرطة:</strong> 122</p>
            <p><strong>🏥 مستشفى:</strong> 124</p>
            <p><strong>👨‍🏫 مرشد طلابي:</strong> 125</p>
            <p><strong>📱 دعم فني:</strong> 126</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 💬 نصائح مهمة")
        st.markdown("""
        <div class='info-box'>
            • لا تتردد في طلب المساعدة<br>
            • جميع المشكلات سرية<br>
            • سنستمع لك بكل اهتمام<br>
            • فريق الدعم متاح 24/7
        </div>
        """, unsafe_allow_html=True)

def show_student_schedule():
    st.markdown("## 📚 جدول الحصص الأسبوعي")
    
    # بيانات الجدول (مثال)
    schedule_data = {
        "اليوم": ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس"],
        "الحصة الأولى": ["رياضيات", "علوم", "عربي", "إنجليزي", "رياضيات"],
        "الحصة الثانية": ["علوم", "عربي", "إنجليزي", "رياضيات", "علوم"],
        "الحصة الثالثة": ["عربي", "إنجليزي", "رياضيات", "علوم", "عربي"],
        "الحصة الرابعة": ["إنجليزي", "رياضيات", "علوم", "عربي", "إنجليزي"],
        "الحصة الخامسة": ["نشاط", "نشاط", "نشاط", "نشاط", "نشاط"]
    }
    
    df_schedule = pd.DataFrame(schedule_data)
    st.dataframe(df_schedule, use_container_width=True, hide_index=True)
    
    # مهام اليوم
    st.markdown("## ✅ مهام اليوم")
    
    tasks = [
        "📝 حل تمارين الرياضيات ص 25",
        "🔬 تجربة العلوم المنزلية",
        "📖 حفظ قصيدة اللغة العربية",
        "✍️ كتابة موضوع تعبير"
    ]
    
    for task in tasks:
        col1, col2 = st.columns([0.1, 0.9])
        with col1:
            st.checkbox("")
        with col2:
            st.markdown(f"<p style='margin:0;'>{task}</p>", unsafe_allow_html=True)

# ==================== التطبيق الرئيسي ====================
def main():
    # تحميل التنسيقات
    load_css()
    
    # تهيئة حالة الجلسة
    init_session_state()
    
    # التحقق من حالة تسجيل الدخول
    if not st.session_state.logged_in:
        login_system()
    else:
        # عرض الواجهة المناسبة حسب نوع المستخدم
        if st.session_state.user_type == "teacher":
            teacher_dashboard()
        else:  # student
            student_dashboard()

if __name__ == "__main__":
    main()
