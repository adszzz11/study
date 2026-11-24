---
date: 2026-11-25
tags: [tech]
type: tech-tool-study
status: draft
---

# Genesis Cheatsheet

## 사용 진입점

| 환경 | 사용 |
|---|---|
| Claude Code | `/genesis map`, `/genesis review main` |
| Codex | `$genesis` skill에서 map·review 요청 |
| 결과 화면 | `.genesis/out/latest/view.html` |
| PR용 요약 | `.genesis/out/latest/summary.md` |

`main`은 실제 존재하는 비교 revision으로 바꾼다. Slash command와 skill 호출은 shell 명령이 아니다. 설치는 공식 가이드를 확인한다.

## Test verdict

| 화면 | summary 값 | 읽는 법 |
|---|---|---|
| 🔴 No coverage found | `not reached` | 도달 테스트를 찾지 못함 |
| 🟡 Behavior not checked | `reached only` | 실행하지만 동작을 확인하지 않음 |
| ⚪ Coverage unclear | `unknown` | 읽은 근거로 판단 불가 |
| ✅ Behavior checked | `covered` | 동작 검증 근거 있음; assertion 의미 재확인 |

## 리뷰 체크리스트

- [ ] 비교 revision과 실제 diff가 맞는가?
- [ ] 영향받는 entry point가 실제 호출 경로에 있는가?
- [ ] 코드 인용이 설명의 의미도 뒷받침하는가?
- [ ] Assertion은 변경 동작이 깨질 때 실패하는가?
- [ ] Timeout·retry·경계값·동시성 사례를 확인했는가?
- [ ] 외부 package의 근거 부족을 `unknown`으로 남겼는가?
- [ ] Review의 `summary.md`에서 partial 여부를 확인했는가?
- [ ] 실제 테스트 실행과 정적 판정을 구분했는가?

## 기억할 경계

- CLI: model 호출·외부 전송·프로젝트 코드/테스트 실행 없음. Risk rule engine 없음.
- Agent: 의미·위험·verdict 해석 담당. Agent 데이터 처리는 별도 확인.
- Python: 직접 parsing으로 누락 branch의 `partial` 표시 가능.
- 다른 언어: 코드 읽기·인용 검증은 지원하지만 같은 누락 탐지 보장 없음.
- Benchmark: 프로젝트 측 Python commit 10개. 전체 정확도와 일반화에 주의.

## 연결

[[tech/devtools/genesis-agent-change-map/README|학습 경로]] · [[tech/devtools/genesis-agent-change-map/04-learning/01-getting-started|시작하기]] · [[tech/devtools/genesis-agent-change-map/04-learning/02-deep-dive|심화 학습]]

## Sources

- https://github.com/GenesisAgentInfra/genesis — 제공된 dossier의 GitHub 수집 본문 근거.
- https://raw.githubusercontent.com/GenesisAgentInfra/genesis/main/docs/install.md — 본문에서 안내한 설치 가이드. 내용은 별도 열람하지 않음.
