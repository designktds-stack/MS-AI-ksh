# 국가재난안전통신망 안전점검 관리 시스템
### MVP 제작 준비

 - 검색 데이터 타입 : 엑셀 (4개 파일 업로드 인덱싱)
 - Resource group : pro-resource-ksh-1027
 - Azure OpenAI : pro-openai-ksh-1027
 - Search service : pro-search-ksh-1027
 - Storage account : prostorageaccountmvpksh
 - Web App : prowebapp-mvp-ksh
 - 인덱스 : rag-ksh-mvp-3
 - 언어모델 : pro-ksh-gpt-4.1-mini
 - 임베딩 모델 : pro-ksh-text-embedding-3-large
 - 검색 방식 : Semantic Hybrid Search
 - 엑셀 구분값 : 시트(분기), 시스템, KT담당자, 업체명, 업체당당자, 점검일, 이슈내용, 이슈처리사항
 - 시스템 항목 : "검색엔진", "통계", "SSO", "UMC", "PORTAL", "VMWare", "DB", "내부연계", "ITSM", "IAM", "HPE SERVER", "앱스토어", "외부연계", "BSS", "CHATBOT", "OFCS"
 <br><br>

### 구축 목적
 ㅇ 국가재난안전통신망의 정기점검 시 발생한 이슈와 결과를 데이터베이스 저장파일(엑셀)을 통하여 확인<br>
 ㅇ GPT엔진을 이용하여 대응방안을 제시받을 수 있고 차기 분기 점검일정도 추천받을 수 있는 시스템 구축<br>
 ㅇ 분기 점검 진행시 업체별 점검일정 사전 조율
<br><br> 

### 제작 배경
 ㅇ 분기별 점검이 매년 진행이 되고 있으나 점검 내역관리가 되어 있지 않아 정보의 유실이 발생<br>
 ㅇ kt측의 분기별 점검 정보 요청 및 이슈 대응관리 및 향후 유사 이슈 발생에 대한 과거 대응 정보 필요성
<br><br> 


### 분기 점검 결과 및 이슈 관리
 ㅇ 점검이 진행된 분기별 발생한 이슈를 검색하고 대응방안을 GPT를 이용하여 검색 가능하도록 함.<br>
 ㅇ 점검 완료 및 미처리, 결과 확인 관리<br>
 ㅇ 시스템 오류, 이슈 발생으로 미처리된 건에 대한 조치 계획 수립<br>
 ㅇ kt측의 분기별 점검 정보 요청 및 이슈 대응관리 및 향후 유사 이슈 발생에 대한 과거 대응 정보 필요성
<br><br> 


### 점검일/시간 생성 (자동생성)
 ㅇ 차기 분기 시스템별 점검 일정을 추천받아 업체 점검일정생성에 있어 효율성 기대<br>
 ㅇ 향후 조건 (kt담당자 근무시간)을 추가하여 점검시간의 적확도를 높일 수 있도록 함
<br><br>
 

![image](./MVP-KSH.jpg)
<br><br>

### MVP
[URL] : [MVP-KSH-LINK](https://prowebapp-mvp-ksh-f7fxg0c9bhcgeven.canadacentral-01.azurewebsites.net/)


<br>

[질문 예시]
1. 3분기의 각 시스템  KT담당자와 이슈내용 및 완료 여부를 알려줘
2. 3분기의 각 시스템 점검내역을 알려줘
3. 3분기의  검색엔진  업체명을 알려줘
4. 3분기의  검색엔진  KT담당자를 알려줘
5. 3분기의 검색엔진의 KT담당자와 점검내역을 알려줘
6. 3분기의 각 시스템  KT담당자와 업체명 이슈내용 및 완료 여부를 알려줘
7. 3분기의 시스템 이슈에 대한 대응방안을 추천해줘
8. 4분기 점검일정을 추천해줘
