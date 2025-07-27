---
marp: true
theme: gaia
paginate: true
backgroundColor: #1e1e1e
backgroundImage: url('https://source.unsplash.com/1600x900/?technology,abstract')
backgroundSize: cover
---

<br><br><br><br>

# 💡 Backend 개발자가 보는 AI  
#### 우리는 어떻게 적응하고 있는가?

<br><br>

<!-- _class: align-right -->

👨‍💻 이상민 &nbsp;&nbsp; 📍 2025.07.27  

---
## 소개

<table style="width: 100%;">
  <tr>
    <td style="width: 60%; vertical-align: top; text-align: left; padding-right: 2em;">
      4년 차 백엔드 개발자이자 DevOps 실무자.<br>
      AI와 협업하는 개발 방식에 깊은 관심을 가지고 있으며,<br>
      실무 경험을 바탕으로 조직 전체의 생산성 향상을 고민하고 있습니다.
    </td>
    <td style="width: 10%; text-align: right;">
      <img src="image.png" alt="alt text" style="max-width: 10%; height: 30%; border-radius: 8px;" />
    </td>
  </tr>
</table>

---

## 🧠 AI가 백엔드 개발에 침투한 기술적 흐름

- GPT-4o, Claude 3 등 LLM의 실시간 코드 생성 능력
- OSS 기반의 자동화 도구: Code Interpreter, AutoGPT, Continue
- RAG 기반의 사내 문서 질의 시스템 도입

💡 백엔드는 구조화된 패턴과 표준이 많기에, AI가 빠르게 학습하고 대체 가능

---

## ⚙️ 주요 백엔드 영역별 AI 활용 사례

### 🔧 1. API 설계 및 문서화
- OpenAPI 명세 → 코드 자동 생성
- API 문서 → ChatGPT로 실시간 요약 및 샘플 생성

### 🧪 2. 테스트 자동화
- Testcase 설명 → JUnit 코드 생성
- Contract Test 스텁 자동 작성

### 📊 3. 로그/지표 분석
- AI 기반 로그 anomaly 탐지
- Prometheus 쿼리 설명 → 자연어로 해석

---

## 🔐 인프라/보안 영역의 변화

- Terraform 코드 리뷰 및 추천 by GPT
- IAM Policy 자동 생성 및 점검
- DevSecOps에서의 정적 분석 + LLM 기반 위험 식별

🧱 AI는 단순 코드 생성보다 '문맥 기반 조율자'로 진화 중

---

## 🧭 AI에 맞춘 개발 환경 재편

- ChatGPT 기반 Swagger 문서 브라우저 도입
- 팀 단위 RAG(Retrieval Augmented Generation) 도입 → 레거시 시스템 문서 질의 가능
- Prompt 관리 플랫폼 도입 (ex. PromptOps)

⚠️ Prompt 관리와 보안, 감사 로깅도 새로운 백엔드 이슈로 부상

---

## 👥 조직과 팀 단위의 적응 변화

- 코드 리뷰 → "AI + 인간 공동 리뷰"로 변화
- PR description을 GPT가 자동 보조
- AI에게 설명 가능한 코드 작성이 새로운 기본

👨‍🏫 주석, 설명, 변수명 → AI도 이해할 수 있도록 작성해야 함

---

## 📚 팀의 학습 방식 변화

- 신규 입사자 온보딩 → 사내 GPT Q&A 봇으로 자동화
- 사내 위키 문서 + LLM → 자동 요약 및 질의
- 기술 블로그/회고 작성 → AI 초안 → 수정 방식으로 변화

📖 “개발자가 쓰는 글”이 아닌 “AI가 읽을 글”을 쓰는 시대

---

## 🧠 조직의 전략적 대응

| 영역 | 전략 |
|------|------|
| 기술 스택 | LLM 친화적 구조로 정비 (ex. 모듈화, 명세 중심 설계) |
| 인재 전략 | Prompt 엔지니어링 + AI 활용 교육 내재화 |
| 업무 방식 | AI 코드 생성 → 리뷰 및 조율 중심 업무로 전환 |

🔄 "개발자"는 설계자이자 조정자로 진화 중

---

## ✅ 결론

> AI는 백엔드 개발을 위협하는 존재가 아니라, **가속화하는 존재**

- 반복적인 구현 → 자동화
- 문서/지식 → 자연어 인터페이스
- 협업 → AI와 함께하는 팀워크

🧭 "도구를 통제하는 사람"이 곧 미래의 개발자