# Part 2. Paperclip의 생태계 위치

## 🗺️ 카테고리 안에서의 좌표

```
                  ↑ 거버넌스/예산 중시
                  │
        Paperclip ●
                  │
                  │
        Agency Swarm ●
                  │
   ────────────────┼───────────────→ 코드/라이브러리 중시
        CrewAI ●    │
                  │     ● LangGraph
        AutoGen ●   │
                  │
                  │     ● OpenAI Swarm
                  ↓ 학습/실험 중시
```

## 🆚 핵심 비교 (의사결정용)

| 축 | Paperclip | CrewAI | LangGraph | Agency Swarm | AutoGen | MetaGPT | Dify |
|----|-----------|--------|-----------|--------------|---------|---------|------|
| **본질** | 운영 OS | 라이브러리 | 라이브러리 | 라이브러리 | 라이브러리 | 라이브러리 | 플랫폼 |
| **에이전트 런타임** | 자유 (어댑터) | Python 종속 | Python 종속 | OpenAI SDK | Python | Python | Python |
| **예산 통제** | ⭐⭐⭐⭐⭐ Native | ✗ | ✗ | ✗ | ✗ | ✗ | ⭐ 부분 |
| **거버넌스/승인** | ⭐⭐⭐⭐⭐ | ✗ | HITL | ✗ | ✗ | SOP | 부분 |
| **다중 회사/팀** | ⭐⭐⭐⭐⭐ | ✗ | ✗ | ✗ | ✗ | ✗ | ⭐ tenant |
| **시각 대시보드** | ⭐ React | ✗ | LangSmith | ✗ | Studio (β) | ✗ | ⭐ 캔버스 |
| **에이전트 코드 작성** | 직원별 별도 | YAML+Python | Python | Python+folder | Python | YAML | 노코드 |
| **러닝 커브** | 낮음(UI) | ⭐ 가장 낮음 | 높음 | 낮음 | 중 | 중 | 가장 낮음 |
| **장점** | 운영 단단함 | 빠른 시작 | 상태 머신 | OpenAI 안정 | 합의/디베이트 | SW 회사 시뮬 | 노코드 + RAG |
| **단점** | 직원 코드 별도 | 큰 시스템 약함 | 학습 곡선 | OpenAI 종속 | maintenance 모드 | 코드 외엔 약함 | 커스텀 한계 |

## 🔄 함께 쓰는 패턴 (가장 흔한 조합)

**Paperclip + 다른 프레임워크들**:

```
┌──────────────────────────────────┐
│  Paperclip (관제탑/예산/거버넌스)  │
└──────┬───────────┬────────┬──────┘
       │           │        │
   ┌───▼──┐   ┌───▼──┐   ┌─▼────────┐
   │CrewAI│   │Lang  │   │OpenClaw  │
   │ 크루 │   │Graph │   │  봇      │
   └──────┘   └──────┘   └──────────┘
   (도메인     (복잡     (메신저 응대)
   협업)       워크플로우)
```

각 직원은 자기 영역에서 최적 프레임워크를 쓰고, Paperclip은 그걸 묶어 운영.

## 🆚 1:1 비교

### Paperclip vs Agency Swarm (가장 비슷한 두 개)

| 항목 | Paperclip | Agency Swarm |
|------|-----------|--------------|
| 메타포 | "Company" | "Agency (CEO+직원)" |
| 구현 형태 | 외부 OS (TS) | Python 라이브러리 |
| 직원 런타임 | 무관 | OpenAI Agents SDK |
| 에이전트 간 통신 | 큐 기반 | 직접 채널 (`>`) |
| 예산 | hard-stop | 미지원 |
| 대시보드 | React UI | 없음 |
| **결론** | **운영자 친화** | **개발자 친화** |

### Paperclip vs CrewAI

| 항목 | Paperclip | CrewAI |
|------|-----------|--------|
| 시작 시간 | npx 1줄 | pip 1줄 |
| 첫 워크플로우까지 | 30분 (UI 클릭) | 30분 (Python 작성) |
| 운영 부담 | Postgres+UI | Python 스크립트 |
| 협업 모델 | 직원 → 큐 | 크루 안에서 직접 |
| **결론** | **장기 운영** | **빠른 프로토타입** |

### Paperclip vs LangGraph

| 항목 | Paperclip | LangGraph |
|------|-----------|-----------|
| 추상화 단위 | 직원 | 상태 그래프 노드 |
| 상태 관리 | DB | 체크포인터 (DB) |
| HITL | 거버넌스 승인 | Interrupt + state edit |
| 모니터링 | 자체 대시보드 | LangSmith |
| **결론** | **운영 시점** | **개발 시점** |

## 🌐 함께 쓸 만한 스택

| 역할 | 추천 |
|------|------|
| Paperclip의 직원으로 채용 가능한 것 | Claude Code, OpenClaw, **Hermes**, Codex, Cursor, Bash, Python, CrewAI 스크립트, LangGraph 그래프 |
| 데이터 저장 | Postgres (권장), SQLite (소규모) |
| 메시지 큐 | (불필요 — DB 큐) |
| 모니터링 | 내장 대시보드 + Grafana(선택) |
| 외부 접근 | Tailscale, Cloudflare Tunnel |
| 시크릿 | env, 1Password CLI, Vault |

## 🔥 최신 동향 (2026 Q1-Q2)

1. **30k★ → 67k★ 폭발 성장**: 출시 후 두 달 만에 카테고리 표준 후보로
2. **"Zero-human company" 밈화**: 1인 운영자/인디 해커 사이에서 인기
3. **OpenClaw 사태 반사이익**: 보안 이슈로 흔들린 OpenClaw 사용자가 "관리 레이어 별도" 패턴으로 이동
4. **ClawHost 매니지드 등장**: Paperclip + OpenClaw 묶음 호스팅 $9.99/월
5. **A2A 프로토콜과의 관계**: Google ADK의 A2A가 표준화되면 직원 등록이 더 쉬워질 전망

## 🔗 다음

- 공식 자료 → [03-references.md](03-references.md)
- 실제 띄우기 → [04-learning/01-install-and-onboard.md](04-learning/01-install-and-onboard.md)
