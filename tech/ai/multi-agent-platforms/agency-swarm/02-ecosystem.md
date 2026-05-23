# Part 2. Agency Swarm 생태계

## 🆚 vs 경쟁자

| 항목 | Agency Swarm | CrewAI | AutoGen | Paperclip |
|------|--------------|--------|---------|-----------|
| 메타포 | Agency(CEO+직원) | Crew(역할) | GroupChat | Company |
| 통신 통제 | ⭐ `>` 명시 | sequential/hier | manager | 큐 기반 |
| 폴더 구조 | ⭐ 폴더=직원 | YAML+Python | Python | YAML |
| Type-safe Tool | ⭐ Pydantic | 일부 | 일부 | (직원마다) |
| OpenAI 의존도 | 높음 | 낮음 | 중간 | 무관 |
| ★ | 4.4k | 52k | 58.3k | 67k |

## 🆚 1:1 비교

### vs CrewAI
- Agency Swarm: **CEO 중심 + 폴더 구조 + 명시적 흐름**
- CrewAI: **평등 협업 + YAML + 유연 흐름**
- 챗봇형 시스템 → Agency Swarm, 워크플로우 → CrewAI

### vs Paperclip
- 둘 다 "회사" 메타포지만 추상화 수준 다름
- **Agency Swarm**: 라이브러리 (코드 내부)
- **Paperclip**: 운영 OS (외부 인프라)
- 조합 가능: Agency Swarm로 코드 작성 + Paperclip에 직원으로 등록

## 🌐 함께 쓰는 스택

| 역할 | 도구 |
|------|------|
| LLM 라우팅 | LiteLLM (Anthropic/Google 등) |
| Type validation | Pydantic v2 |
| RAG | OpenAI Assistants file_search |
| 외부 API | OpenAPI schema → 자동 도구화 |
| Observability | Logfire, LangSmith (가능) |
| Deploy | FastAPI 래핑 |

## 🔥 동향
- 4.4k★지만 VRSEN YouTube 채널을 통한 영향력 큼
- OpenAI Agents SDK가 표준화되면서 안정성 ↑
- Pydantic AI와 컨셉 겹침 — 향후 통합 가능성

## 🔗 다음 → [03-references.md](03-references.md)
