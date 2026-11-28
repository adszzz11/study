---
date: 2026-11-25
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기 — 첫 map과 review

## 사전 준비

- Git repository와 Claude Code 또는 Codex 사용 환경을 준비한다.
- 설치 가이드에서 현재 OS·runtime 요구사항과 agent별 설치 절차를 확인한다. 제공된 dossier는 설치 조건 도중 끊겼으므로 이 노트에는 검증하지 않은 설치 명령을 싣지 않는다.
- CLI의 local 동작과 별개로 사용하는 agent의 데이터 처리 정책을 확인한다.
- 리뷰할 비교 revision을 정한다. 아래 `main`은 실제 repository에 존재할 때 사용하는 예시다.

```sh
# Git 상태와 비교 기준 확인용 명령. Genesis 설치 명령이 아니다.
git status --short
git rev-parse --verify main
git diff --stat main
```

## Claude Code에서 실행

설치를 완료한 뒤 Claude Code 대화에서 다음을 사용한다. Shell 명령이 아니다.

```text
/genesis map
/genesis review main
```

1. `map`으로 사용자 행동의 entry point와 flow step을 읽는다.
2. `review main`으로 변경된 step과 테스트 판정을 확인한다.
3. Step을 클릭해 변경 설명과 코드 인용을 실제 diff·테스트에 대조한다.

## Codex에서 실행

Codex에서는 `$genesis` skill을 사용한다. 아래는 요청 예시이며 별도 CLI 문법을 의미하지 않는다.

```text
$genesis
현재 repository의 business flow를 map으로 정리하고,
main 기준 변경의 영향과 테스트 검증 근거를 review해 줘.
```

## 산출물 확인

```text
.genesis/out/latest/
├── view.html
└── summary.md
```

- `view.html`: Flow와 각 step의 변경·test verdict·코드 확인.
- `summary.md`: PR에 붙일 수 있는 요약. 사람 검토 후 사용한다.
- Python 누락 경로의 `partial` 여부를 점검한다. `map` 페이지는 상단에 “Partial”을 표시하지만 `review` 페이지는 그렇지 않으므로 리뷰에서는 반드시 `summary.md`도 읽는다.

## 완료 기준

- [ ] 현재 flow와 변경 flow의 차이를 설명할 수 있다.
- [ ] 최소 한 개 verdict의 테스트 인용과 assertion을 직접 확인했다.
- [ ] 불확실한 근거와 추가 테스트 과제를 기록했다.
- [ ] 실제 테스트는 별도로 실행하고 결과를 Genesis의 정적 판정과 구분했다.

## 다음 학습

[[tech/devtools/genesis-agent-change-map/04-learning/02-deep-dive|심화 학습]] · [[tech/devtools/genesis-agent-change-map/cheatsheet|빠른 참조]] · [[tech/devtools/genesis-agent-change-map/README|학습 경로]]

## Sources

- https://github.com/GenesisAgentInfra/genesis — 제공된 dossier의 GitHub 수집 본문 근거.
- https://raw.githubusercontent.com/GenesisAgentInfra/genesis/main/docs/install.md — 본문에서 안내한 설치 가이드. 내용은 별도 열람하지 않음.
