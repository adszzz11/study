---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet

## 로컬 build와 조회

저장소 checkout 디렉터리에서 실행한다. Node.js 20 이상 필요.

```bash
pnpm install
pnpm build
node bin/run.js search fastify --limit 5
node bin/run.js sections fastify/demo
# 직전 sections에서 선택한 실제 ID로 교체한다.
node bin/run.js content fastify/demo 1
node bin/run.js content fastify/demo 1 --chunks
```

Command로 설치된 환경에서는 `node bin/run.js`를 `codewiki`로 바꾼다. `<repo>`에는 `owner/repo` 또는 GitHub URL을 쓴다. `--limit` 범위는 1~50이다.

## 갱신과 cache

```bash
node bin/run.js sections fastify/demo --refresh
# refresh 뒤 ID를 다시 선택한다. 아래 1은 예시다.
node bin/run.js content fastify/demo 1
node bin/run.js cache directory
node bin/run.js cache directory /tmp/codewiki-study-cache
# cached wiki documents를 삭제할 때만 실행
node bin/run.js cache clear
```

`content <repo> <section-id> --refresh`도 지원한다. ID 재선택이 필요한 자동화에서는 `sections --refresh`부터 실행한다.

| 기억할 점 | 의미 |
|---|---|
| sections는 본문 생략 | 제목·요약·anchor로 먼저 선택 |
| 최초 fetch는 full wiki | 선택적 출력 ≠ 선택적 네트워크 수집 |
| ID는 갱신 시 변경 가능 | 최신 목록으로 재선택 |
| chunks는 heading·block 기준 | token 상한 보장 미확인 |
| cache 경로 | 환경변수 → 저장 설정 → XDG → ~/.cache |
| upstream은 undocumented RPC | 변경·실패 대응 검토 필요 |

## 개발 명령

```bash
pnpm format:check
pnpm lint
pnpm typecheck
pnpm test
pnpm build:skill
```

실습 설명: [[tech/devtools/codewiki-cli-analysis-9fbbd58a/04-learning/01-getting-started|시작하기]] · [[tech/devtools/codewiki-cli-analysis-9fbbd58a/04-learning/02-deep-dive|Deep Dive]] · [[tech/devtools/codewiki-cli-analysis-9fbbd58a/README|학습 진입점]]


## Sources

- https://github.com/miinhho/codewiki-cli — 제공된 dossier의 README 기반 정리. 실습 및 성능 검증은 미실행.
