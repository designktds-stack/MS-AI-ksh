import openai
from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
import calendar
from datetime import datetime, timedelta

# 환경변수 로드
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_version = os.getenv("OPENAI_API_VERSION")

# Streamlit UI
st.title("📅 TEST 제목")
st.write("년도, 월, 점검 시간을 입력하면 AI가 주간 일정표를 생성합니다.")

year = st.text_input("년도를 입력하세요 (예: 2025):")
month = st.text_input("월을 입력하세요 (예: 10):")
time1 = st.text_input("점검 시간 (예: 09:00, 14:00):")

button_clicked = st.button("---------TEST 제목--------")

if button_clicked:
    try:
        year = int(year)
        month = int(month)
    except ValueError:
        st.error("⚠️ 연도와 월은 숫자로 입력해주세요.")
        st.stop()

    # LLM 프롬프트 메시지
    messages = [
        {"role": "system", "content": "You are an AI scheduler that returns clean HTML tables."},
        {"role": "user", "content": f"""
        {year}년 {month}월의 실제 달력을 기준으로, 
        공휴일을 제외하고 월~일(7일 단위)로 구분된 주간 일정표를 작성해줘.
        각 날짜는 (요일)을 함께 표시하고, 
        점검 시간은 [{time1}]로 모든 날에 동일하게 적용해줘.
        표는 HTML <table> 형태로 출력하되, 
        테두리를 실선(border=1)으로 표시해줘.
        각 주는 별도의 표로 구분해줘.
        """}
    ]

    with st.spinner("AI가 일정표를 작성 중입니다..."):
        response = openai.chat.completions.create(
            model="dev-gpt-4.1-mini",
            messages=messages,
            temperature=0.7
        )

    ai_html = response.choices[0].message.content
    st.success("✅ 일정표 생성 완료!")

    # 결과 표시
    st.markdown("### 🗓️ 생성된 주간 일정표")

    # HTML 표 렌더링
    st.markdown(
        f"""
        <style>
        table {{
            border-collapse: collapse;
            width: 100%;
            text-align: center;
            font-family: '맑은 고딕', sans-serif;
        }}
        th, td {{
            border: 1px solid black; /* 실선 테두리 */
            padding: 8px;
        }}
        th {{
            background-color: #e6f0ff;
        }}
        </style>
        {ai_html}
        """,
        unsafe_allow_html=True
    )

    # AI가 HTML 형식이 아닌 텍스트를 반환했을 경우 대비 
    if "<table" not in ai_html:
        cal = calendar.Calendar(firstweekday=0)
        all_days = [d for d in cal.itermonthdates(year, month) if d.month == month]
        weeks = []
        week = []

        for day in all_days:
            week.append({
                "날짜": f"{day.day} ({calendar.day_name[day.weekday()][:3]})",
                "점검시간": time1
            })
            if len(week) == 7:
                weeks.append(week)
                week = []
        if week:
            weeks.append(week)

        for i, week in enumerate(weeks, 1):
            st.markdown(f"**{i}주차 일정표**")
            df = pd.DataFrame(week)
            st.markdown(
                df.to_html(index=False, border=1, justify="center"),
                unsafe_allow_html=True
            )
