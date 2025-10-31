import os # 운영체제 관련 기능을 사용하기 위해 불러오는 모듈
from dotenv import load_dotenv # .env 파일을 읽어서 환경 변수로 로드하는 함수
from openai import AzureOpenAI # Azure OpenAI 서비스와 통신하기 위해 제공되는 Python SDK (GPT질문, RAG연동)
import streamlit as st # 웹 앱을 쉽게 만들 수 있는 프레임워크 Streamlit를 불러옴
import random # 난수 생성, 리스트 섞기 등 무작위 기능 제공
import re # 문자열 패턴을 정의하고, 그 패턴을 사용해서 문자열을 검색, 추출, 치환, 검증
from datetime import datetime, timedelta # 날짜와 시간 계산 관련 기능 제공

# 페이지 설정 - Streamlit 앱의 기본 설정 (제목, 아이콘, 레이아웃)
st.set_page_config(page_title="AI 검색 어시스턴트", page_icon="🔍", layout="wide")

# 스타일링 - 커스텀 CSS로 UI 디자인 정의
st.markdown("""
    <style>
    .main-header {
        font-size: 2.3rem; font-weight: bold; color: #1f77b4;
        text-align: center; margin-bottom: 2rem;
    }
    .answer {
        font-size: 1.6rem; font-weight: 600; padding: 12px 0px 10px; 
        border-bottom: 1px solid; margin: 0 0 20px 0; color: #1f77b4;
    }
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        font-weight: 600;
        padding: 5px 10px;
        border-radius: 0.5rem;
        font-size: 1.1rem;
        border: 1px solid #1f77b4 !important;
        width: 150px !important;
    }
    .stButton > button:hover {
        background-color: #000000;
        box-shadow: 0 2px 2px rgba(0,0,0,0.2);
        border: 1px solid #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 환경변수 로드 - .env 파일에서 API 키 등 민감 정보 불러오기
load_dotenv()

# Azure 서비스 설정 - OpenAI와 AI Search 연결에 필요한 정보
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")  # OpenAI 엔드포인트 URL
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")  # OpenAI API 키
AZURE_AI_SEARCH_ENDPOINT = os.getenv("AZURE_AI_SEARCH_ENDPOINT")  # AI Search 엔드포인트 URL
AZURE_AI_SEARCH_API_KEY = os.getenv("AZURE_AI_SEARCH_API_KEY")  # AI Search API 키
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")  # 사용할 GPT 모델명
DEPLOYMENT_EMBEDDING_NAME = os.getenv("DEPLOYMENT_EMBEDDING_NAME")  # 임베딩 모델명
INDEX_NAME = "rag-ksh-mvp-3"  # AI Search 인덱스 이름

# Azure OpenAI 클라이언트 초기화 - GPT 모델과 통신하기 위한 클라이언트 생성
init_success = True  # 초기화 성공 여부 플래그
try:
    chat_client = AzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_version="2024-12-01-preview",  # API 버전 지정
    )
except Exception as e:
    st.error(f"클라이언트 초기화 실패: {str(e)}")  # 초기화 실패 시 오류 메시지 표시
    init_success = False

# 사이드바 - 좌측에 시스템 정보 및 안내 표시
with st.sidebar:
    st.header("ℹ️ 시스템 정보")
    st.info(f"**인덱스**: {INDEX_NAME}")  # 사용 중인 인덱스명 표시
    st.info(f"**모델**: {DEPLOYMENT_NAME}")  # 사용 중인 GPT 모델명 표시
    st.info(f"**검색 방식**: Semantic Hybrid Search")  # 검색 방식 표시

    if init_success:
        st.success("✅ 시스템 준비 완료")  # 초기화 성공 시
    else:
        st.error("❌ 초기화 실패")  # 초기화 실패 시

    st.markdown("---")
    st.markdown("### 💡 검색 가능한 정보")  # 검색 가능한 정보 카테고리 안내
    st.markdown("""
    - 시스템 정기점검 (분기)
    - 시스템 KT담당자
    - 점검업체 및 일정
    - 이슈 현황
    - 대응 방안
    """)

# 메인 UI - 페이지 제목 표시
st.markdown('<div class="main-header">국가재난안전통신망 안전점검 관리 시스템</div>', unsafe_allow_html=True)

# 사용자 입력 영역 - 질문 입력창과 검색 버튼
input_text = st.text_input("질문을 입력하세요. (예시. 3분기의 각 시스템  KT담당자와 이슈내용 및 완료 여부를 알려줘.)")  # 질문 입력 필드

button_clicked = st.button("🔍 검색", type="primary")  # 검색 버튼

# 시스템 목록 - 점검 대상 시스템들의 리스트
system_list = ["OS기술지원", "검색엔진", "통계", "SSO", "UMC", "PORTAL", "VMWare", "DB", 
               "내부연계", "ITSM", "IAM", "HPE SERVER", "앱스토어", "외부연계", "BSS", "CHATBOT", "OFCS"]

# 추천 시간 유형 - 점검 시간 추천에 사용할 시간대
available_times = ["10:00", "15:30", "15:00"]

# 2025년 공휴일 - 점검 날짜 추천 시 제외할 공휴일 리스트
holidays_2025 = [
    "2025-01-01", "2025-02-28", "2025-03-01", "2025-05-05", "2025-06-06", 
    "2025-08-15", "2025-09-08", "2025-09-09", "2025-09-10", "2025-10-03", "2025-10-09", "2025-12-25"
]
holidays_2025 = [datetime.strptime(h, "%Y-%m-%d").date() for h in holidays_2025]  # 문자열을 날짜 객체로 변환

# 분기별 점검 기간 - 각 분기의 점검 가능 기간 정의
quarter_periods = {
    "1분기": ("2025-02-01", "2025-02-14"),  # 1분기: 2월 1일 ~ 2월 14일
    "2분기": ("2025-05-01", "2025-05-14"),  # 2분기: 5월 1일 ~ 5월 14일
    "3분기": ("2025-09-01", "2025-09-14"),  # 3분기: 9월 1일 ~ 9월 14일
    "4분기": ("2025-11-01", "2025-11-14")   # 4분기: 11월 1일 ~ 11월 14일
}



# 여기부터는 점검일정을 추천받고자 제가 업무적으로 필요한 부분으로 생성하였습니다. -----------------------------------------------

def assign_times_to_systems(systems, times): # def : 함수를 정의 parameter (systems, times)
    """시스템별로 중복되지 않게 시간 배정하는 함수"""
    assigned_times = {}  # 시스템별 배정된 시간을 저장할 딕셔너리
    random.shuffle(times)  # 시간대를 랜덤으로 섞음
    time_index = 0  # 현재 시간대 인덱스

    for system in systems:  # 각 시스템에 대해
        assigned_times[system] = times[time_index]  # 현재 시간대 배정
        time_index += 1  # 다음 시간대로 이동
        if time_index >= len(times):  # 시간대를 모두 사용했으면
            random.shuffle(times)  # 다시 섞고
            time_index = 0  # 인덱스 초기화
    return assigned_times

def get_available_dates(quarter):
    """분기 내 공휴일과 주말을 제외한 점검 추천 날짜 리스트 생성 함수"""
    if quarter not in quarter_periods:  # 유효하지 않은 분기명이면
        return []  # 빈 리스트 반환

    start_str, end_str = quarter_periods[quarter]  # 시작일과 종료일 가져오기
    start_date = datetime.strptime(start_str, "%Y-%m-%d").date()  # 시작일을 날짜 객체로 변환
    end_date = datetime.strptime(end_str, "%Y-%m-%d").date()  # 종료일을 날짜 객체로 변환

    valid_dates = []  # 유효한 날짜를 저장할 리스트
    current_date = start_date  # 현재 날짜를 시작일로 설정
    while current_date <= end_date:  # 종료일까지 반복
        if current_date.weekday() < 5 and current_date not in holidays_2025:  # 주말(토일)과 공휴일 제외
            valid_dates.append(current_date)  # 유효한 날짜 추가
        current_date += timedelta(days=1)  # 다음 날로 이동
    return valid_dates

# 검색 버튼 클릭 시 실행되는 메인 로직 -------------------------------------------------------------------------------------------------
if button_clicked and input_text.strip():  # 버튼이 클릭되고 입력값이 있으면
    try:
        # 일반 점검정보 질문에서 분기 정보 추출
        found_quarter = None  # 찾은 분기를 저장할 변수
        for q in ["1분기", "2분기", "3분기", "4분기"]:  # 각 분기명으로
            if q in input_text:  # 질문에 분기명이 포함되어 있으면
                found_quarter = q  # 해당 분기 저장
                break

        st.write('<div class="answer">AI 답변</div>', unsafe_allow_html=True)  # 답변 섹션 헤더 표시

        # 조건 문의 - 점검 일정 추천 기능
        if found_quarter and (("추천" in input_text and "시간" in input_text) or "점검일정" in input_text):  # 분기와 "추천", "시간" 키워드가 있으면
            st.markdown(f"**{found_quarter} 점검 시 시스템별 추천 점검 시간 및 날짜입니다.**")

            recommended_times = assign_times_to_systems(system_list, available_times)  # 시스템별 시간 배정
            available_dates = get_available_dates(found_quarter)  # 해당 분기의 가능한 날짜 가져오기

            if not available_dates:  # 가능한 날짜가 없으면
                st.warning("추천 가능한 날짜가 없습니다 (공휴일 혹은 기간 오류).")
            else:
                # 시스템 수만큼 랜덤으로 날짜 선택
                random_dates = random.sample(available_dates, min(len(system_list), len(available_dates)))

                for i, sys in enumerate(system_list):  # 각 시스템에 대해
                    t = recommended_times[sys]  # 배정된 시간 가져오기
                    date = random_dates[i % len(random_dates)]  # 날짜 선택 (순환)
                    st.write(f"- **{sys}** → 🗓️ {date.strftime('%Y-%m-%d')} 🕒 {t}")  # 결과 표시

# 여기까지는 점검일정을 추천받고자 제가 업무적으로 필요한 부분으로 생성하였습니다.----------------------------------------------------                   




# 여기부터는 일반 점검정보 검색 prompt, 정의 영역으로 시스템의 점검내역과 이슈내역 등 검색 코드입니다.----------------------------------- 
        else:
            # 시맨틱 검색을 위한 개선된 프롬프트 - GPT에게 역할과 답변 형식 지시
            prompt = [
                {"role" : "system", "content" : """당신은 KT 시스템 정보 전문가입니다.
                
                사용자의 질문을 의미적으로 이해하고 관련된 정보를 제공.
                - 분기가 언급되면 해당 분기의 관련 정보를 포괄적으로 검색
                - 답변시 맨윗 줄에 질문을 요약하여 간결하게 표기.
                - 시스템 단위로 구분하고 시스템은 폰트사이즈 12px, 볼드체로 처리하고, 나머지 정보들은 각각 한줄씩 내려가며 
                  맨앞에 한칸 띄워 ' - ' 를 붙이고 구분값을 먼저 호출하고 한칸 띄우고 ' : ' 를 붙이고 내용을 표기. 
                  단 시스템은 예외로 시스템명만 호출고 각 시스템 정보 호출이 끝나면 두줄 내려 다음 시스템 정보를 호출함.
                - 즉 시스템, 이슈내용 등 관련된 내용이 해당. 
                - 질문의 의도를 파악하여 관련성 높은 답변을 제공하며, 정보가 없는 경우 '내용없음'으로 표기. 
                - 검색된 데이타 정보는 그대로 보여줌.

                1분기, 2분기, 3분기, 4분기 에서 추가 시스템으로 분류된 앱스토어, 외부연계, BSS, CHATBOT, OFCS 도 시스템에 포함.       
                 
                필수사항:
                    - 검색된 이슈중에서 질의에 연관된 이슈는 반드시 모두 포함시켜야 함.
                    - 추가 시스템 이슈와 시스템 이슈를 구분짓지 말것.
                    - 예) 추가 시스템 : 앱스토어, 외부연계, BSS, CHATBOT, OFCS
    """},
                {"role" : "user", "content" : input_text}  # 사용자 질문
            ]

            # Semantic Hybrid Search 파라미터 - Azure AI Search 설정
            rag_params = { # Azure OpenAI 모델에게 “어디서, 어떤 방식으로 데이터를 검색할지” 알려주는 검색 설정
                "data_sources": [
                    {
                        "type": "azure_search",  # Azure AI Search 사용
                        "parameters": {
                            "endpoint": AZURE_AI_SEARCH_ENDPOINT,  # Azure AI Search 서비스 URL
                            "index_name": INDEX_NAME,  # 검색할 인덱스 이름
                            "authentication": {
                                "type": "api_key",  # API 키 인증 방식
                                "key": AZURE_AI_SEARCH_API_KEY,  # API 키
                            },
                            "query_type": "vector_semantic_hybrid",  # 벡터 + 시맨틱 하이브리드 검색
                            "embedding_dependency": {
                                "type": "deployment_name",  # 임베딩 모델 타입
                                "deployment_name": DEPLOYMENT_EMBEDDING_NAME,  # 배포 임베딩 모델명 - text-embedding-3-large
                            },
                            "top_n_documents": 5,  # 검색할 최대 문서 수
                            "strictness": 3,  # 검색된 문서의 관련성 필터링 강도를 조정 (1-5, 3은 중간)
                            "in_scope": True  # 검색 범위 지정된 범위나 인덱스 내에서만 문서를 검색
                        }
                    }
                ],
            }

            # Azure OpenAI API 호출 - GPT 모델로 답변 생성
            response = chat_client.chat.completions.create(
                model=DEPLOYMENT_NAME,  # 사용할 GPT 모델
                messages=prompt,  # 시스템 프롬프트와 사용자 질문
                extra_body=rag_params,  # RAG(검색 증강 생성) 파라미터
                temperature=0.0,  # 창의성 수준 (0=결정적, 1=창의적)
                max_tokens=5000  # 최대 생성 토큰 수 (답변 길이)
            )

            # 답변 처리 - Citation 마커([doc1], [doc2] 등)  # 모델이 실제로 생성한 “답변 문장” 텍스트
            answer = response.choices[0].message.content  # choices : GPT가 생성한 답변들(list) / ex. response.choices[0] : 첫 번째 답변을 선택
            
            # Citation 마커 추출 (정규표현식으로 [doc숫자] 패턴 찾기)
            citations = re.findall(r'\[doc\d+\]', answer) # citations 리스트로 저장하는 역할 / re : 문자열에서 패턴을 찾거나 치환, 분리할 때 사용
            
            # Citation 마커 제거한 깔끔한 답변 (정규표현식으로 치환)
            clean_answer = re.sub(r'\[doc\d+\]', '', answer).strip()
            
            # 답변 표시 - Streamlit에 결과 출력
            st.write(clean_answer)

    except Exception as e:  # 오류 발생 시
        st.error(f"Error occurred: {str(e)}")  # 오류 메시지 표시
        st.info("Please check your Azure AI Search index name and configuration.")  # 확인 안내

elif button_clicked:  # 버튼만 클릭하고 질문을 입력하지 않은 경우
    st.warning("Please enter a question.")  # 경고 메시지 표시

# 페이지 하단에 출처 표시
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:gray;'>Powered by Azure OpenAI + Azure AI Search (Semantic Hybrid)</div>",
    unsafe_allow_html=True
)