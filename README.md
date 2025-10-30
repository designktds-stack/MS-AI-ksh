# 국가재난안전통신망 안전점검 관리 시스템
### MVP 제작 요약

 1. 모델 : 국가재난안전통신망의 정기점검 시 발생한 이슈와 결과를 데이터베이스 저장파일(엑셀)을 통하여 확인하고 GPT엔진을 이용하여 대응방안을 제시받을 수 있고 차기 분기 점검일정도 추천받을 수 있는 시스템 구축이 목적입니다.

 2. 검색데이터 타입 : 엑셀 (4개 파일 업로드 인덱싱) 
 
 3. 인덱스: rag-ksh-mvp-3
 
 4. 모델: pro-ksh-gpt-4.1-mini
 
 5. 검색 방식: Semantic Hybrid Search
 
 6. 엑셀 구분값 : 시트(분기), 시스템, KT담당자, 업체명, 업체당당자, 점검일, 이슈내용, 이슈처리사항
     - 시스템 목록 : "OS기술지원", "검색엔진", "통계", "SSO", "UMC", "PORTAL", "VMWare", "DB", "내부연계", "ITSM", "IAM", "HPE SERVER", "앱스토어", "외부연계", "BSS", "CHATBOT", "OFCS"
 <br><br>


### 분기 이슈 관리
 ㅇ 분기별 발생한 이슈를 검색하고 대응방안을 GPT를 이용하여 검색할 수 있도록 합니다.
<br><br> 


### 점검일/시간 생성 (자동생성)
 ㅇ 차기 분기 시스템별 점검 일정을 추천받아 업체 점검일정관리 효율성을 높일 수 있도록 합니다.
<br><br>
 

![image](./MVP-KSH.jpg)
<br><br>

### 링크1
[URL] : [MVP-KSH-LINK](https://prowebapp-mvp-ksh-f7fxg0c9bhcgeven.canadacentral-01.azurewebsites.net/)

