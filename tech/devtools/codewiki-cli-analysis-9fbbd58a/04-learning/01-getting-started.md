---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기

## 준비

Node.js 20 이상과 pnpm을 준비하고 원본 저장소를 checkout한다. 아래 build 명령은 checkout 디렉터리에서 실행한다.

```bash
git clone https://github.com/miinhho/codewiki-cli.git
cd codewiki-cli
pnpm install
pnpm build
node bin/run.js search fastify --limit 5
node bin/run.js sections fastify/demo
```

## 첫 본문 조회

직전 목록에서 질문과 관련된 제목·요약·anchor를 보고 ID를 선택한다. 아래 `1`은 예시이므로 실제 ID로 바꾼다. 예제 저장소의 wiki 제공 여부와 현재 ID는 실행 시 확인해야 한다.

```bash
node bin/run.js content fastify/demo 1
node bin/run.js content fastify/demo 1 --chunks
node bin/run.js cache directory
```

- [ ] `sections`가 본문 없이 읽을 범위를 판단하게 해주는지 확인한다.
- [ ] 선택한 섹션 제목과 선택 이유를 기록한다.
- [ ] 일반 출력과 chunk 출력의 읽기 단위를 비교한다.

패키지가 command로 설치되어 있다면 `node bin/run.js` 대신 `codewiki`를 쓴다. 일반 command 설치의 구체적 배포 절차는 제공된 자료에 없다.

## Agent skill 설치

```bash
npx skills add miinhho/codewiki-cli --skill codewiki-cli -a codex --copy -y
```

`-g`를 추가하면 사용자 전체 범위에 설치한다. 이 명령은 실제 설치를 수행하므로 원하는 범위에서 실행한다. 저장소에는 `.agents/skills/codewiki-cli`가 있으며 built CLI가 포함된다. CLI를 수정한 개발자는 `pnpm build:skill`로 bundled copy도 갱신한다. Skill 내부의 추가 행동 규칙은 제공된 자료로 확인할 수 없다.

다음: [[tech/devtools/codewiki-cli-analysis-9fbbd58a/04-learning/02-deep-dive|Deep Dive]] · [[tech/devtools/codewiki-cli-analysis-9fbbd58a/cheatsheet|명령 참조]] · [[tech/devtools/codewiki-cli-analysis-9fbbd58a/README|학습 진입점]]


## Sources

- https://github.com/miinhho/codewiki-cli — 제공된 dossier의 README 기반 정리. 실습 및 성능 검증은 미실행.
