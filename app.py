import streamlit as st
import pandas as pd
import joblib

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Student Success Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS للخلفية والتصميم الملون الاحترافي
st.markdown("""
    <style>
    /* خلفية متدرجة ومتناسقة للصفحة الرئيسية */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* تصميم Sidebar بخلفية متميزة */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
        color: white;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* كروت النتائج بتصميم زجاجي عصري (Glassmorphism) */
    .custom-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 20px;
    }

    /* كروت حالة النتيجة الملونة */
    .status-pass {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        color: white;
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(56, 239, 125, 0.4);
    }

    .status-fail {
        background: linear-gradient(135deg, #eb3349, #f45c43);
        color: white;
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(235, 51, 73, 0.4);
    }
    
    /* تحسين شكل زر التحليل */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        color: white;
        border: none;
        padding: 12px 28px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.25);
    }
    </style>
""", unsafe_allow_html=True)

# 3. تحميل الموديل والأعمدة
@st.cache_resource
def load_assets():
    model = joblib.load('student_model.pkl')
    columns = joblib.load('model_columns.pkl')
    return model, columns

try:
    model, model_columns = load_assets()
except Exception as e:
    st.error("⚠️ خطأ في تحميل ملفات الموديل. تأكد من وجود ملفات .pkl في نفس المجلد.")
    st.stop()

# 4. القائمة الجانبية (Sidebar)
st.sidebar.markdown("<h2 style='text-align: center;'>🎓 نظام التقييم</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown(
    "### 📌 عن Dashboard\n"
    "يقوم هذا النظام المطور بتوظيف موديل **Logistic Regression** الموزون لتحليل مؤشرات الأداء الأكاديمي والتنبؤ المبكر بحالات الرسوب بدقة مرتفعة."
)
st.sidebar.markdown("---")
st.sidebar.markdown("⚙️ **إصدار الموديل:** v1.0 (Balanced Class Weight)")

# 5. الهيدر الرئيسي داخل كارت شيك
st.markdown("""
    <div class="custom-card">
        <h1 style='color: #1e3c72; margin-bottom: 0;'>🎓 Early Student Success & Risk Assessment</h1>
        <p style='color: #555; font-size: 16px;'>قم بإدخال بيانات الطالب للحصول على التنبؤ الإحصائي الفوري ومستوى الخطورة الأكاديمية.</p>
    </div>
""", unsafe_allow_html=True)

# 6. قسم المدخلات مع تنسيق جذاب
st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #2a5298;'>📥 المدخلات الأساسية للطالب</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    attendance = st.slider("📋 نسبة الحضور (Attendance %)", min_value=0, max_value=100, value=75, step=1)

with col2:
    hours_studied = st.number_input("📚 ساعات المذاكرة أسبوعياً", min_value=0, max_value=60, value=15, step=1)

with col3:
    previous_scores = st.slider("📊 الدرجات السابقة (Previous Scores)", min_value=0, max_value=100, value=65, step=1)

st.markdown("</div>", unsafe_allow_html=True)

# 7. زر التنبؤ
if st.button("🚀 تحليل وحساب النتيجة الأكاديمية", use_container_width=True):
    # إعداد البيانات
    input_data = pd.DataFrame(0, index=[0], columns=model_columns)
    
    if 'Attendance' in input_data.columns:
        input_data['Attendance'] = attendance
    if 'Hours_Studied' in input_data.columns:
        input_data['Hours_Studied'] = hours_studied
    if 'Previous_Scores' in input_data.columns:
        input_data['Previous_Scores'] = previous_scores

    # الحسابات
    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]
    pass_prob = probabilities[1] * 100 if len(probabilities) > 1 else 0

    # عرض النتائج في كارت زجاجي مخصص
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #1e3c72;'>📊 التقرير النهائي للتحليل</h3>", unsafe_allow_html=True)
    
    res_col1, res_col2 = st.columns([1, 1])

    with res_col1:
        if prediction == 1 or pass_prob >= 50:
            st.markdown(
                f'<div class="status-pass">✅ النتيجة المتوقعة: ناجح (Passed)</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="status-fail">⚠️ النتيجة المتوقعة: معرض للرسوب (At-Risk)</div>',
                unsafe_allow_html=True
            )

    with res_col2:
        st.metric(label="احتمالية النجاح المقدرة", value=f"{pass_prob:.1f}%")
        st.progress(int(pass_prob))

    # التوصية الأكاديمية
    st.markdown("<br>", unsafe_allow_html=True)
    if pass_prob < 50:
        st.error("⚠️ **توصية المرشد الأكاديمي:** الطالب في دائرة الخطر الأكاديمي. يُوصى بتكثيف الحضور وساعات المذاكرة فوراً.")
    else:
        st.success("🎉 **توصية المرشد الأكاديمي:** أداء الطالب ممتاز واستقراري. يُنصح بالمحافظة على نفس المعدل الحالي.")

    st.markdown("</div>", unsafe_allow_html=True)
