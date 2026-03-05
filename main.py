سأقدم لك كوداً متكاملاً واحترافياً لنظام إدارة المدرسة الذكي مع واجهة عصرية وتصميم داكن متطور:

```python
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
import hashlib
import requests
import json
import time
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import base64

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="مدرسة الفتح الذكية",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== إعدادات DeepSeek API ====================
DEEPSEEK_API_KEY = st.secrets.get("DEEPSEEK_API_KEY", "YOUR_API_KEY_HERE")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# ==================== التصميم المتقدم (Advanced Theming) ====================
def apply_custom_theme():
    st.markdown("""
    <style>
        /* الأساسيات - أزرق غامق جداً */
        .stApp {
            background: linear-gradient(135deg, #0A1929 0%, #0F2744 100%);
            color: #FFFFFF !important;
        }
        
        /* العناوين الرئيسية */
        h1, h2, h3 {
            color: #FFFFFF !important;
            font-weight: 700 !important;
            letter-spacing: -0.5px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        
        /* الهيدر المخصص */
        .custom-header {
            background: linear-gradient(90deg, #1E3A8A, #2563EB);
            padding: 1.5rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(37, 99, 235, 0.2);
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .header-logo {
            font-size: 3rem;
            background: rgba(255,255,255,0.1);
            padding: 0.5rem 1rem;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        
        .header-title {
            color: white;
            font-size: 2rem;
            font-weight: 700;
            margin: 0;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
        
        .header-subtitle {
            color: rgba(255,255,255,0.9);
            font-size: 1rem;
            margin: 0;
        }
        
        /* البطاقات المحسنة */
        .modern-card {
            background: linear-gradient(145deg, #1A2F4F, #13263E);
            border-radius: 20px;
            padding: 1.5rem;
            box-shadow: 0 20px 40px rgba(0,0,0,0.4);
            border: 1px solid rgba(37, 99, 235, 0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .modern-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 25px 50px rgba(37, 99, 235, 0.3);
            border-color: rgba(37, 99, 235, 0.4);
        }
        
        /* حقول الإدخال */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select,
        .stNumberInput > div > div > input {
            background: #1E2F45 !important;
            border: 2px solid #2D4A6F !important;
            color: white !important;
            border-radius: 12px !important;
            padding: 12px !important;
            font-size: 1rem !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #3B82F6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
        }
        
        /* الأزرار المتطورة */
        .stButton > button {
            background: linear-gradient(135deg, #2563EB, #1E40AF) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3) !important;
        }
        
        .stButton > button:hover {
            transform: scale(1.05) !important;
            box-shadow: 0 8px 25px rgba(37, 99, 235, 0.5) !important;
            background: linear-gradient(135deg, #3B82F6, #2563EB) !important;
        }
        
        /* الجداول */
        .stDataFrame {
            background: #1A2F4F !important;
            border-radius: 15px !important;
            padding: 1rem !important;
        }
        
        .stDataFrame td, .stDataFrame th {
            color: white !important;
            border-bottom: 1px solid #2D4A6F !important;
        }
        
        /* القائمة الجانبية */
        .css-1d391kg, .css-1wrcr25 {
            background: #0A1A2F !important;
        }
        
        /* التبويبات */
        .stTabs [data-baseweb="tab-list"] {
            background: #1A2F4F !important;
            border-radius: 15px !important;
            padding: 5px !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            color: white !important;
            border-radius: 10px !important;
            padding: 10px 20px !important;
        }
        
        .stTabs [aria-selected="true"] {
            background: #2563EB !important;
        }
        
        /* مؤشرات التقدم */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #2563EB, #3B82F6) !important;
        }
        
        /* الرسائل التحذيرية */
        .stAlert {
            background: #1E2F45 !important;
            border: 1px solid #2563EB !important;
            color: white !important;
        }
        
        /* الأقسام المخصصة */
        .section-title {
            color: #90CAF9;
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 1rem;
            padding-right: 1rem;
            border-right: 4px solid #2563EB;
        }
        
        /* بطاقات الإحصائيات */
        .stat-card {
            background: linear-gradient(135deg, #1E3A8A, #1E40AF);
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: 700;
            color: white;
            margin: 0;
        }
        
        .stat-label {
            color: #90CAF9;
            font-size: 1rem;
            margin: 0;
        }
        
        /* تأثيرات حركية */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .fade-in {
            animation: fadeIn 0.5s ease;
        }
        
        /* شاشة تسجيل الدخول */
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 40px;
            background: linear-gradient(145deg, #13263E, #0A1A2F);
            border-radius: 30px;
            box-shadow: 0 30px 60px rgba(0,0,0,0.5);
            border: 1px solid #2563EB;
        }
        
        .login-logo {
            text-align: center;
            font-size: 5rem;
            margin-bottom: 20px;
        }
        
        .login-title {
            text-align: center;
            color: white;
            font-size: 2rem;
            margin-bottom: 10px;
        }
        
        .login-subtitle {
            text-align: center;
            color: #90CAF9;
            margin-bottom: 30px;
        }
    </style>
    """, unsafe_allow_html=True)

# ==================== شاشة تسجيل الدخول ====================
def show_login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.container():
            st.markdown("""
            <div class='login-container'>
                <div class='login-logo'>🏫</div>
                <div class='login-title'>مدرسة الفتح الذكية</div>
                <div class='login-subtitle'>نظام إدارة التعليم المتكامل</div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("login_form"):
                username = st.text_input(
                    "👤 اسم المستخدم",
                    placeholder="أدخل اسم المستخدم...",
                    help="للمدرس: T001-T005، للطالب: S001-S010"
                )
                
                password = st.text_input(
                    "🔑 كلمة المرور",
                    type="password",
                    placeholder="أدخل كلمة المرور..."
                )
                
                col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
                with col_btn2:
                    submitted = st.form_submit_button(
                        "🚀 تسجيل الدخول",
                        use_container_width=True
                    )
                
                if submitted:
                    if authenticate_user(username, password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.user_type = 'teacher' if username.startswith('T') else 'student'
                        st.rerun()
                    else:
                        st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")
            
            # روابط مساعدة
            st.markdown("""
            <div style='text-align: center; margin-top: 20px;'>
                <p style='color: #90CAF9; font-size: 0.9rem;'>
                    للدخول التجريبي:<br>
                    مدرس: T001 / password123<br>
                    طالب: S001 / password123
                </p>
            </div>
            """, unsafe_allow_html=True)

# ==================== قاعدة البيانات المحاكاة ====================
@st.cache_data
def load_mock_database():
    """تحميل قاعدة البيانات المحاكاة"""
    
    # بيانات المدرسين
    teachers = {
        'T001': {
            'name': 'أحمد محمد',
            'password': hash_password('password123'),
            'subject': 'الرياضيات',
            'class': '3/1',
            'email': 'ahmed@school.com',
            'phone': '0555123456'
        },
        'T002': {
            'name': 'سارة علي',
            'password': hash_password('password123'),
            'subject': 'العلوم',
            'class': '3/2',
            'email': 'sara@school.com',
            'phone': '0555234567'
        },
        'T003': {
            'name': 'محمد خالد',
            'password': hash_password('password123'),
            'subject': 'اللغة العربية',
            'class': '2/1',
            'email': 'mohamed@school.com',
            'phone': '0555345678'
        },
        'T004': {
            'name': 'فاطمة أحمد',
            'password': hash_password('password123'),
            'subject': 'اللغة الإنجليزية',
            'class': '2/2',
            'email': 'fatma@school.com',
            'phone': '0555456789'
        },
        'T005': {
            'name': 'عمر حسن',
            'password': hash_password('password123'),
            'subject': 'التربية الإسلامية',
            'class': '1/1',
            'email': 'omar@school.com',
            'phone': '0555567890'
        }
    }
    
    # بيانات الطلاب
    students = {}
    classes = ['1/1', '1/2', '2/1', '2/2', '3/1', '3/2']
    names = [
        'يوسف عبدالله', 'لينا محمد', 'عمر خالد', 'سارة أحمد', 'علي حسن',
        'مريم عمر', 'خالد سعد', 'نورا علي', 'فيصل محمد', 'لمى خالد',
        'عبدالله فهد', 'رهف أحمد', 'أسامة طارق', 'جود سامي', 'بدر ناصر',
        'لمار عبدالعزيز', 'تركي فيصل', 'ريناد محمد', 'معاذ سليمان', 'لجين عمر',
        'سعود عبدالرحمن', 'أثير خالد', 'نايف سعود', 'جنى فهد', 'هاشم نايف'
    ]
    
    for i, name in enumerate(names[:10], 1):
        student_id = f"S{str(i).zfill(3)}"
        class_name = np.random.choice(classes)
        students[student_id] = {
            'name': name,
            'password': hash_password('password123'),
            'class': class_name,
            'parent_phone': f'0555{np.random.randint(100000, 999999)}',
            'address': f'الرياض - حي النرجس',
            'gpa': round(np.random.uniform(75, 100), 2)
        }
    
    return {'teachers': teachers, 'students': students}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    """التحقق من صحة بيانات الدخول"""
    db = load_mock_database()
    
    hashed_input = hash_password(password)
    
    if username.startswith('T') and username in db['teachers']:
        return db['teachers'][username]['password'] == hashed_input
    elif username.startswith('S') and username in db['students']:
        return db['students'][username]['password'] == hashed_input
    
    return False

# ==================== دوال مساعدة ====================
def generate_ai_response(prompt, system_prompt="أنت مساعد تربوي متخصص"):
    """توليد رد باستخدام DeepSeek API"""
    if DEEPSEEK_API_KEY == "YOUR_API_KEY_HERE":
        return "⚠️ يرجى إضافة مفتاح DeepSeek API للاستفادة من هذه الخدمة"
    
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"❌ خطأ في الاتصال: {response.status_code}"
    except Exception as e:
        return f"❌ خطأ: {str(e)}"

# ==================== واجهة المدرس ====================
def teacher_dashboard():
    db = load_mock_database()
    teacher_info = db['teachers'][st.session_state.username]
    
    # الهيدر المخصص
    st.markdown(f"""
    <div class='custom-header'>
        <div class='header-logo'>🏫</div>
        <div>
            <h1 class='header-title'>مدرسة الفتح الذكية</h1>
            <p class='header-subtitle'>مرحباً بك، {teacher_info['name']} | {teacher_info['subject']} | {teacher_info['class']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # القائمة الجانبية
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/school.png", width=100)
        st.markdown(f"### 👨‍🏫 {teacher_info['name']}")
        st.markdown(f"📧 {teacher_info['email']}")
        st.markdown("---")
        
        selected = option_menu(
            menu_title="القائمة الرئيسية",
            options=["الرئيسية", "الدرجات", "التحضير", "المساعد التربوي", "الإذاعة", "الأذكار"],
            icons=["house", "graph-up", "calendar-check", "robot", "mic", "star"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#0A1A2F"},
                "icon": {"color": "#2563EB", "font-size": "20px"},
                "nav-link": {"color": "white", "font-size": "16px", "text-align": "right", "margin": "5px"},
                "nav-link-selected": {"background-color": "#2563EB"},
            }
        )
        
        st.markdown("---")
        if st.button("🚪 تسجيل الخروج", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.user_type = ""
            st.rerun()
    
    # عرض المحتوى حسب الاختيار
    if selected == "الرئيسية":
        show_teacher_home(teacher_info)
    elif selected == "الدرجات":
        show_grades_system(teacher_info)
    elif selected == "التحضير":
        show_lesson_planner(teacher_info)
    elif selected == "المساعد التربوي":
        show_ai_assistant()
    elif selected == "الإذاعة":
        show_radio_section()
    elif selected == "الأذكار":
        show_dhikr_section()

def show_teacher_home(teacher_info):
    st.markdown("## 📊 لوحة المعلومات")
    
    # إحصائيات سريعة
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-number'>25</div>
            <div class='stat-label'>عدد الطلاب</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-number'>88%</div>
            <div class='stat-label'>نسبة الحضور</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-number'>85.5</div>
            <div class='stat-label'>متوسط الدرجات</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-number'>6</div>
            <div class='stat-label'>طلاب متفوقين</div>
        </div>
        """, unsafe_allow_html=True)
    
    # جدول الطلاب
    st.markdown("## 📋 قائمة الطلاب")
    
    db = load_mock_database()
    students_data = []
    for student_id, student_info in db['students'].items():
        if student_info['class'] == teacher_info['class']:
            students_data.append({
                'رقم الجلوس': student_id,
                'الاسم': student_info['name'],
                'الفصل': student_info['class'],
                'المعدل': student_info['gpa']
            })
    
    if students_data:
        df = pd.DataFrame(students_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("لا يوجد طلاب في هذا الفصل")

def show_grades_system(teacher_info):
    st.markdown("## 📊 نظام رصد الدرجات")
    
    tab1, tab2, tab3 = st.tabs(["➕ إضافة درجة", "📋 عرض الدرجات", "📈 إحصائيات"])
    
    with tab1:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("<div class='section-title'>بيانات الدرجة</div>", unsafe_allow_html=True)
            
            with st.form("grade_form"):
                # قائمة الطلاب
                db = load_mock_database()
                students_in_class = []
                student_ids = []
                
                for student_id, student_info in db['students'].items():
                    if student_info['class'] == teacher_info['class']:
                        students_in_class.append(student_info['name'])
                        student_ids.append(student_id)
                
                student = st.selectbox("👤 اختر الطالب", students_in_class)
                
                # المواد
                subjects = ["الرياضيات", "العلوم", "اللغة العربية", "اللغة الإنجليزية", "التربية الإسلامية"]
                subject = st.selectbox("📚 المادة", subjects)
                
                # نوع التقييم
                assessment_type = st.selectbox(
                    "📝 نوع التقييم",
                    ["اختبار شهري", "اختبار نهائي", "واجب", "مشاركة", "مشروع"]
                )
                
                # الدرجة
                grade = st.number_input("🎯 الدرجة", min_value=0, max_value=100, value=70)
                
                # التاريخ
                grade_date = st.date_input("📅 التاريخ", datetime.now())
                
                # ملاحظات
                notes = st.text_area("📌 ملاحظات", placeholder="أي ملاحظات إضافية...")
                
                submitted = st.form_submit_button("💾 حفظ الدرجة", use_container_width=True)
                
                if submitted:
                    st.success(f"✅ تم إضافة درجة {grade} للطالب {student} في مادة {subject}")
                    st.balloons()
        
        with col2:
            st.markdown("<div class='section-title'>آخر الدرجات المضافة</div>", unsafe_allow_html=True)
            
            # عرض آخر الدرجات (بيانات تجريبية)
            recent_grades = pd.DataFrame({
                'الطالب': ['أحمد محمد', 'سارة علي', 'عمر خالد'],
                'المادة': ['الرياضيات', 'العلوم', 'اللغة العربية'],
                'الدرجة': [95, 88, 92],
                'التاريخ': ['2024-01-15', '2024-01-15', '2024-01-14']
            })
            st.dataframe(recent_grades, use_container_width=True, hide_index=True)
    
    with tab2:
        st.markdown("<div class='section-title'>جميع الدرجات</div>", unsafe_allow_html=True)
        
        # عرض جميع الدرجات (بيانات تجريبية)
        all_grades = pd.DataFrame({
            'الطالب': np.random.choice(['أحمد', 'سارة', 'عمر', 'فاطمة', 'خالد'], 10),
            'المادة': np.random.choice(['الرياضيات', 'العلوم', 'العربية', 'الإنجليزية'], 10),
            'الدرجة': np.random.randint(65, 100, 10),
            'نوع التقييم': np.random.choice(['اختبار', 'واجب', 'مشاركة'], 10),
            'التاريخ': pd.date_range(start='2024-01-01', periods=10, freq='D')
        })
        
        st.dataframe(all_grades, use_container_width=True, hide_index=True)
        
        # تصدير البيانات
        col_exp1, col_exp2, col_exp3 = st.columns(3)
        with col_exp2:
            if st.button("📥 تصدير إلى Excel", use_container_width=True):
                st.success("تم تصدير البيانات بنجاح!")
    
    with tab3:
        st.markdown("<div class='section-title'>التحليلات والإحصائيات</div>", unsafe_allow_html=True)
        
        # رسوم بيانية
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            # توزيع الدرجات
            grades_data = np.random.normal(75, 10, 100)
            fig = px.histogram(
                grades_data, 
                nbins=20,
                title="توزيع الدرجات",
                labels={'value': 'الدرجة', 'count': 'عدد الطلاب'}
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col_chart2:
            # متوسط الدرجات حسب المادة
            subjects = ['الرياضيات', 'العلوم', 'العربية', 'الإنجليزية']
            averages = np.random.uniform(70, 90, 4)
            
            fig = go.Figure(data=[
                go.Bar(x=subjects, y=averages, marker_color='#2563EB')
            ])
            fig.update_layout(
                title="متوسط الدرجات حسب المادة",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)

def show_lesson_planner(teacher_info):
    st.markdown("## 📝 نظام التحضير الإلكتروني")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<div class='section-title'>تحضير درس جديد</div>", unsafe_allow_html=True)
        
        with st.form("lesson_form"):
            date = st.date_input("📅 التاريخ", datetime.now())
            subject = st.selectbox(
                "📚 المادة",
                ["الرياضيات", "العلوم", "اللغة العربية", "اللغة الإنجليزية", "التربية الإسلامية"]
            )
            lesson_title = st.text_input("🏷️ عنوان الدرس", placeholder="أدخل عنوان الدرس...")
            
            # الأهداف
            objectives = st.text_area(
                "🎯 الأهداف التعليمية",
                placeholder="اكتب الأهداف التعليمية للدرس...",
                height=100
            )
            
            # الوسائل
            materials = st.text_area(
                "🛠️ الوسائل التعليمية",
                placeholder="الوسائل والأدوات المستخدمة...",
                height=100
            )
            
            # الأنشطة
            activities = st.text_area(
                "⚽ الأنشطة التعليمية",
                placeholder="الأنشطة التي سيقوم بها الطلاب...",
                height=100
            )
            
            # التقييم
            evaluation = st.text_area(
                "📊 أساليب التقييم",
                placeholder="كيف ستقيم فهم الطلاب؟...",
                height=100
            )
            
            submitted = st.form_submit_button("💾 حفظ التحضير", use_container_width=True)
            
            if submitted and lesson_title:
                st.success("✅ تم حفظ التحضير بنجاح!")
    
    with col2:
        st.markdown("<div class='section-title'>التحضيرات السابقة</div>", unsafe_allow_html=True)
        
        # عرض التحضيرات السابقة (بيانات تجريبية)
        previous_lessons = [
            {
                "date": "2024-01-15",
                "subject": "الرياضيات",
                "title": "المعادلات الخطية",
                "status": "✅ منجز"
            },
            {
                "date": "2024-01-14",
                "subject": "العلوم",
                "title": "التفاعلات الكيميائية",
                "status": "✅ منجز"
            },
            {
                "date": "2024-01-13",
                "subject": "اللغة العربية",
                "title": "قواعد النحو",
                "status": "✅ منجز"
            }
        ]
        
        for lesson in previous_lessons:
            st.markdown(f"""
            <div class='modern-card' style='margin-bottom: 10px;'>
                <div style='display: flex; justify-content: space-between;'>
                    <span style='color: #90CAF9;'>{lesson['date']}</span>
                    <span style='color: #2563EB;'>{lesson['status']}</span>
                </div>
                <h4 style='margin: 10px 0;'>{lesson['title']}</h4>
                <p style='color: #90CAF9;'>{lesson['subject']}</p>
            </div>
            """, unsafe_allow_html=True)

def show_ai_assistant():
    st.markdown("## 🤖 المساعد التربوي الذكي")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<div class='section-title'>اكتب مشكلتك التربوية</div>", unsafe_allow_html=True)
        
        with st.form("ai_assistant_form"):
            problem_type = st.selectbox(
                "نوع المشكلة",
                ["سلوكية", "دراسية", "اجتماعية", "نفسية", "تحصيلية", "أخرى"]
            )
            
            student_info = st.text_input(
                "معلومات الطالب (اختياري)",
                placeholder="مثال: عمر - الصف الثالث - 10 سنوات"
            )
            
            problem_description = st.text_area(
                "وصف المشكلة",
                placeholder="صف المشكلة بالتفصيل...",
                height=150
            )
            
            submitted = st.form_submit_button("🔍 تحليل واقتراح حلول", use_container_width=True)
            
            if submitted and problem_description:
                with st.spinner("جاري تحليل المشكلة واقتراح الحلول..."):
                    prompt = f"""
                    المشكلة: {problem_type}
                    معلومات الطالب: {student_info}
                    الوصف: {problem_description}
                    
                    قدم خطة علاجية متكاملة تتضمن:
                    1. تحليل المشكلة
                    2. الأسباب المحتملة
                    3. خطة علاجية مرحلية
                    4. أنشطة مقترحة
                    5. طرق المتابعة والتقييم
                    """
                    
                    response = generate_ai_response(prompt, "أنت مستشار تربوي خبير")
                    st.session_state.ai_response = response
    
    with col2:
        if 'ai_response' in st.session_state:
            st.markdown("<div class='section-title'>💡 الخطة العلاجية المقترحة</div>", unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class='modern-card'>
                {st.session_state.ai_response}
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("💾 حفظ الخطة", use_container_width=True):
                st.success("تم حفظ الخطة في قاعدة البيانات")

def show_radio_section():
    st.markdown("## 📻 الإذاعة المدرسية الذكية")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<div class='section-title'>توليد إذاعة جديدة</div>", unsafe_allow_html=True)
        
        with st.form("radio_form"):
            radio_title = st.text_input("عنوان الإذاعة", placeholder="أدخل عنوان الإذاعة...")
            radio_theme = st.selectbox(
                "الموضوع",
                ["عام", "ديني", "وطني", "علمي", "ثقافي", "اجتماعي"]
            )
            radio_duration = st.slider("المدة (بالدقائق)", 5, 20, 10)
            
            submitted = st.form_submit_button("🎙️ توليد الإذاعة", use_container_width=True)
            
            if submitted and radio_title:
                with st.spinner("جاري توليد نص الإذاعة..."):
                    prompt = f"""
                    عنوان الإذاعة: {radio_title}
                    الموضوع: {radio_theme}
                    المدة: {radio_duration} دقائق
                    
                    اكتب سيناريو متكاملاً للإذاعة المدرسية يتضمن:
                    1. مقدمة مشوقة
                    2. فقرة القرآن الكريم
                    3. فقرة الحديث الشريف
                    4. كلمة الصباح
                    5. فقرة هل تعلم (3-5 معلومات)
                    6. حكمة اليوم
                    7. خاتمة
                    
                    اجعل النص متناسقاً ومناسباً للإذاعة المدرسية.
                    """
                    
                    response = generate_ai_response(prompt, "أنت مقدم إذاعة مدرسية محترف")
                    st.session_state.radio_script = response
    
    with col2:
        if 'radio_script' in st.session_state:
            st.markdown("<div class='section-title'>نص الإذاعة المولدة</div>", unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class='modern-card' style='max-height: 500px; overflow-y: auto;'>
                {st.session_state.radio_script}
            </div>
            """, unsafe_allow_html=True)
            
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("📋 نسخ النص", use_container_width=True):
                    st.info("تم النسخ!")
            with col_b2:
                if st.button("💾 حفظ", use_container_width=True):
                    st.success("تم الحفظ!")

def show_dhikr_section():
    st.markdown("## 📿 بنك الأذكار اليومية")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<div class='section-title'>ذكر اليوم</div>", unsafe_allow_html=True)
        
        # ذكر اليوم (يمكن تغييره يومياً)
        daily_dhikr = "اللهم إني أسألك علماً نافعاً، ورزقاً طيباً، وعملاً متقبلاً"
        
        st.markdown(f"""
        <div class='modern-card' style='text-align: center;'>
            <h1 style='font-size: 3rem; margin: 0;'>🤲</h1>
            <p style='font-size: 1.5rem; line-height: 2rem;'>{daily_dhikr}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 توليد ذكر جديد", use_container_width=True):
            with st.spinner("جاري توليد ذكر جديد..."):
                prompt = "اكتب ذكراً أو دعاءً مميزاً من الأذكار النبوية مع ذكر فضله"
                response = generate_ai_response(prompt, "أنت متخصص في الأذكار والأدعية")
                st.session_state.generated_dhikr = response
