---
date: 2026-08-12
tags: [tech]
type: tech-tool-study
status: draft
---

# Diagram Design — Getting Started

> [[../03-references|이전: References]] · [[../README|목차로 돌아가기]] · [[02-deep-dive|다음: Deep Dive]]

## 1. 안전하게 가져오기

versioned release가 없으므로 먼저 검토할 commit을 정한다.

```bash
git clone https://github.com/cathrynlavery/diagram-design.git
cd diagram-design
git log -1 --oneline
git rev-parse HEAD
```

학습 단계에서는 repository의 `skills/diagram-design/`을 읽고, 설치할 때는 사용하는 agent가 요구하는 skill/plugin discovery 경로를 공식 README에서 확인한다. production에서는 기록한 commit SHA로 pin하거나 editable fork를 운영한다.

## 2. 첫 요청의 네 요소

좋은 요청은 content, audience, output, style을 분리한다.

```text
결제 요청이 API Gateway → Payment Service → PSP로 흐르고,
timeout이면 Retry Queue를 거치는 sequence를 그려라.

- audience: mixed
- format: html
- size: doc-wide
- detail: balanced
- style: default minimal light
```

| 요소 | 질문 |
|---|---|
| Content | 어떤 entity와 relation이 핵심인가? |
| Audience | engineer, mixed, executive 중 누구인가? |
| Output | HTML, SVG, PNG, HTML+PNG 중 무엇인가? |
| Style | default인가, website brand token을 적용할 것인가? |

## 3. Type 선택을 검토하기

Agent가 type을 골랐다고 바로 layout을 승인하지 않는다.

- 시간 순서와 message 교환이 핵심이면 `Sequence`
- component와 boundary가 핵심이면 `Architecture`
- 상태 전이와 조건이 핵심이면 `State machine`
- 책임 주체별 handoff가 핵심이면 `Swimlane`
- executive trade-off가 핵심이면 `Consultant 2×2` 또는 `Quadrant`

하나의 diagram이 여러 질문에 답하려 하면 density가 올라간다. audience별로 diagram을 나누는 편이 낫다.

## 4. Brand onboarding

default style이 아닌 website 기반 style을 원하면 agent가 다음 mapping을 제안하도록 한다.

| Website signal | Diagram token |
|---|---|
| `<body>` background | `paper` |
| Primary text | `ink` |
| Secondary text | `muted` |
| Card/container background | `paper-2` |
| CTA·link·brand color | `accent` |
| `<h1>` font | title font |
| `<body>` font | node-name font |
| `<code>/<pre>` font | technical sublabel font |

적용 전 token diff를 확인하고 작은 label에서도 `ink`/`paper`가 WCAG AA contrast를 만족하는지 점검한다. website fetch와 web font는 agent의 network 환경에 의존하므로 offline fallback도 정한다.

## 5. 결과 검수

```text
[ ] 핵심 메시지를 한 문장으로 설명할 수 있다.
[ ] accent는 1–2개 focal element에만 쓰였다.
[ ] 모든 좌표·폭·간격은 4px grid를 따른다.
[ ] connector는 node를 관통하지 않고 관계가 모호하지 않다.
[ ] monospace는 기술 sublabel에만 쓰였다.
[ ] shadow가 없고 border radius는 10px 이하이다.
[ ] SVG에 role="img", title, desc, 고유 aria-labelledby가 있다.
[ ] output size에서 label이 실제로 읽힌다.
```

## 6. 첫 실습

1. component 5개 이하의 작은 architecture를 prose로 작성한다.
2. `audience: mixed`, `detail: balanced`, `format: html`로 생성한다.
3. 같은 내용을 `audience: executive`로 다시 생성한다.
4. 두 결과에서 생략된 정보와 accent 위치를 비교한다.
5. source prompt와 pin한 commit SHA를 결과 옆에 기록한다.

## Sources

- [Diagram Design README](https://github.com/cathrynlavery/diagram-design/blob/main/README.md)
- [SKILL.md](https://github.com/cathrynlavery/diagram-design/blob/main/skills/diagram-design/SKILL.md)
- [Onboarding spec](https://github.com/cathrynlavery/diagram-design/blob/main/skills/diagram-design/references/onboarding.md)
- [Security Policy](https://github.com/cathrynlavery/diagram-design/blob/main/SECURITY.md)

