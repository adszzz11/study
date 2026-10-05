---
date: 2026-10-05
tags: [tech]
type: tech-tool-study
status: draft
---

# Answer me with HTML — Overview

> [[README|목차로 돌아가기]] | [[02-ecosystem|다음: 생태계]]

## What

Answer me with HTML은 agent 답변을 설명용 standalone HTML artifact로 바꾸는 Agent Skill과 `am` CLI다. agent는 frontmatter, `##` panel, fenced component block을 포함한 extended Markdown 초안을 작성한다. renderer는 이를 해석해 HTML/CSS/SVG와 layout을 만든다.

```text
User question
  → AI agent + SKILL.md
  → extended Markdown draft
  → am render / am video
  → parser + component renderer + theme + Dagre layout + STE lint
  → self-contained HTML (선택: narrated video/MP4)
```

## Why

직접 HTML 생성을 요청하면 모델은 설명뿐 아니라 CSS, wrapper `div`, SVG 좌표도 매번 출력한다. 이 방식은 output token과 대기시간을 키우고 diagram 좌표 오류를 유발하기 쉽다. 이 도구는 다음처럼 책임을 나눈다.

| 담당 | 책임 |
|---|---|
| LLM / agent | 무엇을 설명할지, 정보 순서와 component data 작성 |
| `am` renderer | panel grid, theme, Markdown 변환, SVG layout, writing lint |
| 사용자 | source 검토, 사실 확인, artifact 공유 |

프로젝트 자체 benchmark(Claude Sonnet 5.5, 2026-10-02, 세 주제 각 3회 median)는 직접 HTML 대비 output token `6,873 → 923`(7.4×), 시간 `46s → 13s`(3.6×)를 제시한다. 반면 extra agent turn이 context를 다시 읽어 비용은 `$0.22 → $0.26`으로 줄지 않았다. 이 수치는 프로젝트 측정치이므로 자신의 model·prompt·작업 길이에서 재현해 판단해야 한다.

## Key Features

- template: `sheet` multi-panel grid, `doc` table-of-contents single column
- components: `flow`, `sequence`, `tree`, `timeline`, `limits`, `annot`, `kv`, `callout`, Markdown table
- presentation: `blueprint`, `shadcn` theme과 `light`/`dark` mode
- maintenance: embed된 원본 Markdown을 이용하는 `am patch` panel-level update
- writing: ASD-STE100에서 영감을 받은 `am lint`의 `off`/warning/`strict` mode
- video: narration beat 기반 explainer player; provider와 로컬 도구가 있으면 MP4 export

## Technical Boundaries

현재 package metadata 기준 runtime은 Node.js `>=20`이며 의존성은 `marked`, `@dagrejs/dagre`다. Dagre는 flow graph 자동 배치를 돕지만, 복잡한 데이터 시각화나 완전한 diagram notation 표준을 대신하지는 않는다.

`am video`의 MP4 export는 선택 기능이다. Chrome, `ffmpeg`, Node.js 22+와 TTS provider(ElevenLabs, system TTS 또는 local OpenAI-compatible TTS 중 선택)가 추가로 필요할 수 있다.

## Sources

- https://github.com/QingYunA/answer-me-with-html
- https://raw.githubusercontent.com/QingYunA/answer-me-with-html/main/src/cli.js
- https://raw.githubusercontent.com/QingYunA/answer-me-with-html/main/package.json
- https://raw.githubusercontent.com/QingYunA/answer-me-with-html/main/bench/README.md
