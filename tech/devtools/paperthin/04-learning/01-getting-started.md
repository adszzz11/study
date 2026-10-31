---
date: 2026-08-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Paperthin — Getting Started

> [[../03-references|이전: References]] · [[../README|목차]] · [[02-deep-dive|다음: Deep Dive]]

## 1. 설치 전 확인

- Node.js와 `npx`를 실행할 수 있는지 확인한다.
- global skill directory와 host agent가 읽는 directory를 확인한다.
- third-party `SKILL.md`, script, hook은 실행 전 source를 review한다.
- shared/production 환경에서는 global install의 filesystem 권한과 update 방식을 먼저 정한다.

## 2. 설치

공식 quickstart는 모든 지원 agent를 대상으로 global install한다.

```bash
npx skills@latest add LilMGenius/paperthin --global --agent '*'
```

설치 감지는 주로 다음 local path를 사용한다.

```text
~/.agents/skills
~/.claude/skills
~/.re0/          # update notice state
```

> `--global --agent '*'`는 편리하지만 범위가 넓다. installer가 제시하는 대상과 변경 내용을 확인한 뒤 승인한다.

## 3. 설치 검증

host agent를 새 session에서 시작하고 discovery 목록에서 `re0`, `readchk`, `factchk` 등을 확인한다. skill이 보이지 않으면 다음 순서로 진단한다.

1. 실제 설치 directory가 host의 discovery path와 일치하는지 확인한다.
2. 각 skill directory에 `SKILL.md`가 있는지 확인한다.
3. YAML frontmatter의 `name`, `description`이 parse되는지 확인한다.
4. symlink를 썼다면 host가 symlink target을 허용하는지 확인한다.
5. session-start discovery가 필요하면 agent를 재시작한다.

## 4. 첫 적용: 작은 artifact에 `re0`

연습용 README나 plan을 선택하고 다음 조건을 명시한다.

```text
이 문서를 re0 관점으로 검토하라.
현재 진실에 필요 없는 stale delta, 중복, scaffolding residue만 제거하라.
고칠 것이 없으면 파일을 변경하지 마라.
```

검토 기준:

- 과거 변경 과정이 현재 사용법보다 앞에 나오는가?
- 같은 내용이 다른 표현으로 반복되는가?
- placeholder와 임시 heading이 남아 있는가?
- rewrite가 의미를 보존했는가?
- 불필요한 변경이면 실제로 no-op 했는가?

## 5. 다음 적용: claim에 `factchk`

```text
“이 API는 지원되지 않는다”는 claim을 factchk하라.
가능하다는 증거와 불가능하다는 증거를 모두 공식 source에서 찾아라.
확인한 시점과 불확실성을 분리해서 보고하라.
```

`factchk`는 검색 결과의 수가 아니라 claim을 직접 지지하는 external evidence를 요구한다. source가 없으면 certainty를 낮춰야 한다.

## 6. Invocation boundary 지키기

- model-invoked: description의 trigger가 맞을 때 agent가 자동 선택할 수 있다.
- user-invoked: `disable-model-invocation: true`; 사람이 명시적으로 호출한다.
- publication, merge, upgrade처럼 외부 상태를 바꾸는 procedure는 자동 실행으로 추정하지 않는다.
- `hate`, `macrothink`, `feynman`, `prism`도 비용과 bias 때문에 필요할 때만 사람이 호출한다.

## 7. Upgrade

설치 후 catalog 갱신에는 `/re0-upgrade`를 사용한다. 이 skill은 현재 설치를 전체 catalog로 수렴시키되, 먼저 추가·제거·변경 계획을 보여주고 confirmation을 받도록 설계됐다.

```text
/re0-upgrade
```

## Sources

- https://github.com/LilMGenius/paperthin
- https://github.com/LilMGenius/paperthin/blob/main/skills/depth/re0/SKILL.md
- https://github.com/LilMGenius/paperthin/blob/main/skills/breadth/re0-upgrade/SKILL.md

