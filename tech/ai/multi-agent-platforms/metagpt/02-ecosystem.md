# Part 2. MetaGPT 생태계

## 🆚 vs ChatDev (가장 비슷한 카테고리)

| 항목 | MetaGPT | ChatDev |
|------|---------|---------|
| 메타포 | SW 회사 SOP | SW 회사 채팅 |
| 협업 모델 | publish/subscribe | 페어 대화 (Designer-Coder 등) |
| 산출물 | PRD/Design/Code/Test | Code+Doc |
| 활성도 | ⭐ 매우 활발 | 활발 |
| Data Interpreter | ⭐ 강력 | 없음 |
| ★ | 68k | 28k |

## 🆚 vs AutoGen

- AutoGen: 일반 대화형 — 어떤 작업이든 (디베이트, 분석 등)
- MetaGPT: 소프트웨어 회사에 특화 — 코드 생성 자동화에 최적

## 🆚 vs CrewAI / LangGraph

- CrewAI/LangGraph: **워크플로우 작성 도구** — 사용자가 흐름 정의
- MetaGPT: **이미 정의된 흐름** — 사용자는 요구사항만 입력

MetaGPT 흐름을 CrewAI/LangGraph로 직접 재현해도 OK. 다만 MetaGPT는 SOP가 패키지에 박혀있음.

## 🌐 함께 쓰는 스택

| 역할 | 추천 |
|------|------|
| LLM | OpenAI GPT-4o, Anthropic Claude, DeepSeek |
| 실행 환경 | Docker (코드 실행 격리) |
| 결과 저장 | Git (자동 commit) |
| 데이터 분석 | Jupyter / Streamlit (DI 결과) |
| 운영 레이어 | Paperclip 직원으로 등록 가능 |

## 🔥 동향

- **Data Interpreter 강화** — DS 작업 정확도가 GPT-4 단독 대비 ↑
- **GPT-Pilot, OpenHands** 같은 후속 도구가 비슷한 컨셉으로 등장
- **SOPs as code** 트렌드 — 다른 프레임워크도 도입 검토 중
- Chinese AI 커뮤니티에서 인기 (중국어 자료 풍부)

## 🔗 다음 → [03-references.md](03-references.md)
