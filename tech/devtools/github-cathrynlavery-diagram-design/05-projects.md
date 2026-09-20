---
date: 2026-08-12
tags: [tech]
type: tech-tool-study
status: draft
---

# Diagram Design — Projects

> [[04-learning/02-deep-dive|이전: Deep Dive]] · [[README|목차로 돌아가기]] · [[cheatsheet|다음: Cheatsheet]]

## 프로젝트 1: Prose에서 architecture diagram 만들기

### 목표

짧은 system description을 mixed audience용 `doc-wide` architecture로 변환한다.

### 입력 예시

```text
Web Client는 API Gateway를 호출한다.
Gateway는 Auth Service에서 token을 검증한 뒤 Order Service로 전달한다.
Order Service는 PostgreSQL에 저장하고 Event Bus에 OrderCreated를 발행한다.
Analytics Worker가 event를 소비한다.
```

### 산출물과 완료 조건

- [ ] HTML + inline SVG 한 파일
- [ ] external boundary, synchronous call, asynchronous event가 구분됨
- [ ] component가 원문보다 임의로 추가되지 않음
- [ ] focal element가 1–2개를 넘지 않음
- [ ] accessible title과 description 포함

## 프로젝트 2: Mermaid를 audience별로 redraw

### 목표

하나의 Mermaid source에서 engineer용과 executive용 결과를 각각 만든다.

| Variant | 설정 | 기대 결과 |
|---|---|---|
| Engineer | `faithful`, `engineer`, `doc-wide` | relation과 technical label 보존 |
| Executive | `simplified`, `executive`, `slide-16x9` | outcome과 major boundary 중심 |

### 검수

- 두 variant의 fidelity ledger를 비교한다.
- executive 결과에서 생략한 detail이 의사결정을 왜곡하지 않는지 확인한다.
- 원본 Mermaid source는 변경하지 않고 별도 artifact로 보존한다.

## 프로젝트 3: Website-to-brand onboarding

### 목표

website signal을 `paper`, `ink`, `muted`, `paper-2`, `accent`와 font role로 mapping한다.

### 절차

1. `<body>`, heading, body, code, CTA의 computed style 후보를 수집한다.
2. semantic token mapping diff를 작성한다.
3. 작은 label 크기에서 `ink`/`paper` contrast를 확인한다.
4. accent 사용을 focal element 1–2개로 제한한다.
5. network 없이 font를 못 가져올 때의 fallback을 시험한다.

> [!warning]
> managed update가 local `style-guide.md` 수정을 덮을 수 있다. 지속적인 skin은 editable clone이나 fork에서 관리한다.

## 프로젝트 4: Import fidelity review

### 목표

복잡한 draw.io diagram을 `balanced`, `mixed` 설정으로 redraw하고 의미 보존을 감사한다.

```text
[ ] node/entity inventory 비교
[ ] edge direction 비교
[ ] group/boundary 비교
[ ] cycle와 hub 보존 확인
[ ] merged/omitted item 기록
[ ] 원본 coordinate·palette 비보존을 이해관계자에게 알림
```

결과에는 다음 형식의 ledger를 붙인다.

| 분류 | 내용 | 이유 |
|---|---|---|
| Preserved | 핵심 system boundary와 dependency | architecture 이해에 필수 |
| Merged | 반복 worker node | density 4/10 유지 |
| Omitted | field-level metadata | mixed audience에 과도함 |
| Changed | diagonal edge를 orthogonal elbow로 변경 | connector readability |

## 프로젝트 5: Pinned production workflow

### 목표

release가 없는 빠른 `main`을 직접 추종하지 않고 재현 가능한 운영 절차를 만든다.

- [ ] 검토한 commit SHA 기록
- [ ] `SKILL.md`, reference, parser 변경 diff 검토
- [ ] 대표 golden input 3개로 semantic regression 확인
- [ ] accessibility attribute 검사
- [ ] custom `style-guide.md` merge 정책 정의
- [ ] security update 시 새 SHA로 재검증

## Sources

- [Diagram Design README](https://github.com/cathrynlavery/diagram-design/blob/main/README.md)
- [Onboarding spec](https://github.com/cathrynlavery/diagram-design/blob/main/skills/diagram-design/references/onboarding.md)
- [Commit history](https://github.com/cathrynlavery/diagram-design/commits/main/)
- [Security Policy](https://github.com/cathrynlavery/diagram-design/blob/main/SECURITY.md)

