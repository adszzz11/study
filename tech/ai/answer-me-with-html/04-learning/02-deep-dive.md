---
date: 2026-10-05
tags: [tech]
type: tech-tool-study
status: draft
---

# Answer me with HTML — 심화

> [[../README|목차로 돌아가기]] | [[../05-projects|다음: 프로젝트]]

## Design the Draft Before Rendering

좋은 artifact는 component를 많이 쓰는 문서가 아니라, 독자가 답을 찾는 순서가 명확한 문서다. 먼저 one-sentence verdict를 정하고 근거를 panel로 분해한다.

| 정보 형태 | 우선 component |
|---|---|
| 단계와 분기 | `flow` |
| 시간 순서의 송수신 | `sequence` |
| parent-child 구조 | `tree` |
| 사건의 시간대 | `timeline` |
| 제약·범위 | `limits` / `callout` |
| key-value 사실 | `kv` |
| 비교와 trade-off | Markdown table + verdict panel |

`sheet`는 병렬적으로 읽을 수 있는 3–8개 패널에, `doc`은 긴 논증·튜토리얼처럼 목차 순서가 중요한 설명에 맞춘다. 모든 정보를 diagram으로 바꾸기보다 prose/table로 충분한 곳을 남긴다.

## Source-preserving Update

생성 HTML에는 원본 Markdown이 embed된다. `am patch <page.html> --panel "<title>"`는 이 source를 읽어 해당 panel을 수정하고 재렌더링하는 흐름을 제공한다. 이 설계의 핵심은 결과 HTML을 hand-edit하는 것이 아니라 **draft를 source of truth로 유지**하는 데 있다.

권장 순서:

1. version control에서 `.md` source와 결과 HTML을 함께 관리할지 정책을 정한다.
2. 수정 전 panel title의 안정성을 확인한다.
3. patch 뒤 전체 페이지에서 연결·표·diagram 영향 범위를 확인한다.
4. Markdown과 HTML 어느 쪽도 사실 검증의 책임을 자동으로 지지 않음을 명확히 한다.

## Lint as a Review Signal

`am lint`는 ASD-STE100에서 영감을 받은 controlled-writing check이며 `off`, warning, `strict` mode를 선택할 수 있다. strict mode는 장황한 문장, 모호한 지시어, 과도한 복문을 찾는 연습에 좋다. 다만 API name, product name, security terminology, 코드 식별자는 tool이 맥락을 모를 수 있으므로 reviewer가 판단한다.

## Video and MP4

`am video`는 동일한 초안에 narration beat를 더해 explainer player를 만든다. 음성은 ElevenLabs, system TTS, local OpenAI-compatible TTS 중 환경에 맞는 provider를 사용할 수 있다. MP4 export는 Chrome, `ffmpeg`, Node.js 22+가 필요할 수 있으므로, CI나 폐쇄망 배포 전에는 dependency와 license·network policy를 검토한다.

## Evaluation Plan

프로젝트 benchmark를 조직 의사결정으로 일반화하지 않는다. 동일 주제·난이도·model을 고정해 다음을 직접 기록한다.

```text
quality = factual accuracy + reader task success + visual clarity
cost   = model tokens + agent turns + human review time
speed  = drafting + rendering + correction latency
```

## Sources

- https://raw.githubusercontent.com/QingYunA/answer-me-with-html/main/skills/answer-me-with-html/SKILL.md
- https://raw.githubusercontent.com/QingYunA/answer-me-with-html/main/src/cli.js
- https://raw.githubusercontent.com/QingYunA/answer-me-with-html/main/bench/README.md
