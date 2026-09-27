import streamlit as st
import pandas as pd
import joblib

# 1. تحميل الموديل وقائمة الأعمدة
model = joblib.load('student_model.pkl')
model_columns = joblib.load('model_columns.pkl')

# 2. عنوان الصفحة
st.title("🎓 نظام التنبؤ بأداء الطالب")
st.write("أدخل البيانات الأساسية للطالب لمعرفة احتمالية النجاح:")

# 3. واجهة المدخلات المبسطة (3 مدخلات فقط)
attendance = st.slider("نسبة الحضور (Attendance %):", min_value=0, max_value=100, value=80)
hours_studied = st.number_input("ساعات المذاكرة الأسبوعية (Hours Studied):", min_value=0, max_value=100, value=15)
previous_scores = st.number_input("درجات الامتحانات السابقة (Previous Scores):", min_value=0, max_value=100, value=75)

# 4. زر التنبؤ
if st.button("توقع النتيجة 🚀"):
    # تجهيز قاموس يحتوي على قيم افتراضية (0) لكل الأعمدة
    input_data = {col: 0 for col in model_columns}
    
    # تحديث القيم التي أدخلها المستخدم فقط
    if 'Attendance' in input_data:
        input_data['Attendance'] = attendance
    if 'Hours_Studied' in input_data:
        input_data['Hours_Studied'] = hours_studied
    if 'Previous_Scores' in input_data:
        input_data['Previous_Scores'] = previous_scores

    # تحويل البيانات إلى DataFrame بنفس ترتيب الأعمدة الأصلية
    input_df = pd.DataFrame([input_data])[model_columns]

    # 5. إجراء التنبؤ واحتمالية النجاح
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1] * 100

    # 6. عرض النتائج
    st.markdown("---")
    if prediction == 1:
        st.success(f"🎉 **النتيجة المتوقعة: ناجح (Passed)**")
    else:
        st.error(f"⚠️ **النتيجة المتوقعة: معرض للرسوب (Failed)**")

    st.info(f"📊 **احتمالية النجاح:** {probability:.2f}%")