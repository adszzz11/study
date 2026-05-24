---
date: 2026-05-24
tags:
  - tech
  - ai
  - google-cloud
  - agent-garden
  - gemini-enterprise
status: learning
type: tech-tool
---

# Agent Garden (Google Cloud)

> **한 줄 소개**: ADK 기반 에이전트 샘플을 큐레이트해 둔 카탈로그 + Agent Engine 원클릭 배포 콘솔. "Explore → Learn → Deploy → Customize" 워크플로로 에이전트 개발 시작점 제공.

| 항목 | 내용 |
|------|------|
| 공식 사이트 | https://console.cloud.google.com/vertex-ai/agents/agent-garden |
| 산하 플랫폼 | **Gemini Enterprise Agent Platform** (구 Vertex AI Agent Builder, 2026-05-21 개편) |
| 라이선스 | 콘솔은 GCP, 샘플 코드는 각각 오픈소스 (대부분 Apache 2.0) |
| 접근 | 전체 공개 (GCP 고객 아니어도 콘솔 접근 가능) |
| 관련 GitHub | [google/adk-samples](https://github.com/google/adk-samples), [GoogleCloudPlatform/agent-starter-pack](https://github.com/GoogleCloudPlatform/agent-starter-pack) |

---

## 1. 무엇을 해결하는가

### 해결하려는 문제

- 멀티 에이전트 시스템 구축의 진입 장벽 — 어디서부터 시작할지 모름
- 단편적 샘플은 많아도 "프로덕션 배포까지" 보여주는 레퍼런스 부족
- 큐레이션 부재 — adk-samples 레포에 30+개 샘플이 흩어져 있어 비교·발견이 어려움

### 도입 목적

- ADK + Gemini + Agent Engine 풀스택 학습 경로 단축
- 도메인별(BigQuery, Vertex AI Search 등) 통합 사례 빠르게 확인
- 샘플을 한 번 클릭으로 자기 프로젝트에 클론·배포

### 예상 효과

- 신규 에이전트 PoC 시간을 일/주 단위에서 시간 단위로 단축
- 검증된 패턴(HITL, 멀티 에이전트, 평가 루프 등) 재사용
- Agent Engine 운영 (observability, scaling, eval) 무료로 시작

---

## 2. 핵심 기능

### 주요 기능

| 기능 | 설명 | 중요도 |
|------|------|--------|
| **샘플 카탈로그** | adk-samples 30+개를 카테고리·설명·아키텍처 다이어그램과 함께 탐색 | ⭐⭐⭐ |
| **원클릭 배포** | `agent-starter-pack`으로 Agent Engine + playground UI 자동 배포 | ⭐⭐⭐ |
| **Firebase Studio 연동** | 배포된 에이전트를 브라우저 IDE에서 즉시 커스터마이즈 | ⭐⭐ |
| **GitHub 직링크** | 각 샘플의 소스를 GitHub에서 바로 확인 | ⭐⭐ |
| **케이스 스터디** | Renault Group EV 충전 데이터 사이언티스트 에이전트 등 실 사례 노출 | ⭐ |

### 작업 흐름

```
콘솔에서 샘플 검색
       │
       ▼
샘플 카드: 개요 / 아키텍처 / 유스케이스 / GitHub 링크
       │
       ▼
[Deploy] 버튼
       │
       ▼
agent-starter-pack가 자동 실행
  - 프로젝트 스캐폴드 생성
  - Agent Engine에 배포
  - playground UI 노출
  - CI/CD 파이프라인 생성
       │
       ▼
Firebase Studio에서 커스터마이즈 → 다시 배포
```

### 주변 생태계

```
Gemini Enterprise Agent Platform (2026-05~)
├── Agent Garden            ← 샘플 카탈로그 (이 문서)
├── MCP Server Registry     ← MCP 서버 디스커버리
├── Memory Bank             ← 장기 컨텍스트
├── Sessions                ← 상태 있는 인터랙션
├── Agent Registry          ← 배포된 에이전트 카탈로그
└── Agent Engine            ← 매니지드 실행 환경 (구 Vertex AI Agent Engine)
```

---

## 3. 비교 분석

### vs 대안 카탈로그

| 비교 항목 | Agent Garden | LangChain Hub | OpenAI GPTs Store | Anthropic Skills (CC) |
|-----------|--------------|---------------|------------------|----------------------|
| **대상** | 풀스택 에이전트 샘플 | 프롬프트 + 체인 | GPT 단위 봇 | Claude Code 확장 |
| **배포** | Agent Engine 1-click | 자체 배포 | OpenAI 호스팅 | 로컬 + 공유 |
| **커스터마이즈 깊이** | 코드 풀스택 | 프롬프트 위주 | 거의 불가 | 코드 + 마크다운 |
| **벤더 락인** | GCP/Gemini | 없음 | OpenAI | Anthropic |

### 장단점

**장점**
- 코드 풀스택까지 공개 + 자동 배포 → 가장 학습 곡선 낮음
- Google Cloud 인프라(observability, eval, 스케일링) 자동 통합
- Gemini Enterprise Agent Platform 산하로 통합되어 MCP·Memory Bank 등과 자연스럽게 연결

**단점**
- GCP/Gemini 락인 — 다른 클라우드/모델로 옮기려면 작업 필요
- 한국어 자료/케이스 부족
- 샘플별 품질·최신성 편차 존재 (커뮤니티 PR 베이스)

---

## 4. Quick Start

### 사전 준비

- GCP 프로젝트 + 결제 활성화
- `gcloud` CLI 로그인
- Python 3.10+, `uv` 패키지 매니저

### 명령어

```bash
# 1. agent-starter-pack 설치
pip install agent-starter-pack

# 2. Agent Garden에서 샘플 선택 후 받아쓴 명령 실행
agents-cli create my-deep-search-agent -a adk@deep-search

# 3. 배포 (CI/CD 파이프라인 자동 구성)
cd my-deep-search-agent
make deploy
```

### 추천 첫 샘플

| 샘플 | 추천 이유 |
|------|----------|
| `deep-search` | HITL + 멀티 에이전트 + 풀스택 — ADK 패턴의 종합판 |
| `RAG` | 가장 기본적인 패턴, Vertex AI Search 통합 |
| `gemini-fullstack` | React 프론트 + Gemini 백엔드 최소 골격 |
| `customer-service` | 멀티턴 + Tool 호출 + 라우팅 |

---

## 5. 실무 적용 가이드

### 도입 검토 체크리스트

- [ ] GCP 계정 / 결제 셋업
- [ ] Vertex AI / Agent Engine API 활성화
- [ ] 샘플 1개 deploy → playground UI에서 동작 확인
- [ ] Firebase Studio에서 커스터마이즈 시도
- [ ] CI/CD 파이프라인 코드 리뷰
- [ ] 비용 알람 설정 (Gemini 호출 + Agent Engine 인스턴스)

### 주의사항

| 문제 | 원인 | 해결 |
|------|------|------|
| Agent Engine 비용 누적 | 자동 스케일링이 0으로 안 내려감 | Cloud Scheduler로 비활성 시 인스턴스 0 강제 |
| 샘플 코드 최신성 | adk-samples PR 누적 | 배포 전 GitHub 마지막 커밋 날짜 확인 |
| Gemini quota 초과 | 평가 루프가 토큰 폭증 | ResearchConfiguration에서 max iterations 제한 |

---

## 6. 트렌드 메모

- 2026-05-21 Google Cloud Console에서 Vertex AI 메뉴 자체가 사라지고 **Gemini Enterprise Agent Platform**으로 이름 변경됨
- "에이전트 우선" 정보 구조 — 모델 학습/AutoML/Registry/Endpoints가 에이전트 플랫폼의 하위 기능으로 재배치
- Agent Garden은 같은 흐름에서 학습·디스커버리 진입점 역할

---

## 7. References

- [Agent Garden 콘솔](https://console.cloud.google.com/vertex-ai/agents/agent-garden)
- [공식 출시 블로그 (Google Developers Blog)](https://developers.googleblog.com/agent-garden-samples-for-learning-discovering-and-building/)
- [agent-starter-pack GitHub](https://github.com/GoogleCloudPlatform/agent-starter-pack)
- [adk-samples GitHub](https://github.com/google/adk-samples)
- [ADK 공식 문서](https://adk.dev)
- 관련 노트: [[google-adk-deep-search]] · [[ai-ecosystem/01-overview]]
