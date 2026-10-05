---
date: 2026-10-05
tags: [tech]
type: tech-tool-study
status: draft
---

# Answer me with HTML — Ecosystem

> [[README|목차로 돌아가기]] | [[03-references|다음: 참고자료]]

## Positioning

Answer me with HTML은 단일 diagram renderer라기보다 **agent answer presentation layer**에 가깝다. Markdown draft에서 설명 페이지 전체를 만들고, 그 안의 `flow` layout에는 Dagre를 사용한다.

| 도구 | 핵심 역할 | 차이와 적합한 경우 |
|---|---|---|
| Answer me with HTML | agent 답변을 standalone HTML artifact로 생성 | complex explanation, 비교, 기술 개요를 빠르게 소비할 때 |
| 직접 HTML 생성 | LLM이 HTML/CSS/SVG 전체 작성 | pixel-level bespoke UI가 필요할 때; token·대기시간·좌표 오류 부담은 커짐 |
| Mermaid | text definition에서 diagram 생성 | diagram 자체를 docs/site에 삽입할 때; 페이지 panel/template은 별도 구성 필요 |
| Quarto | Markdown + executable code를 HTML/PDF/Word로 publishing | data report, notebook, 재현 가능한 분석 문서에 적합 |
| Marp/Marpit | Markdown → slide deck | 발표 자료가 최종 산출물일 때 적합 |

## Choosing Deliberately

```text
읽는 기술 설명 페이지 전체가 필요한가? ── yes → Answer me with HTML
diagram 하나가 필요한가?              ── yes → Mermaid 등
실행 코드·분석 재현이 핵심인가?         ── yes → Quarto
발표 화면 전환이 필요한가?              ── yes → Marp/Marpit
완전 맞춤 UI가 필요한가?                ── yes → 직접 HTML/CSS/JS
```

Mermaid와는 경쟁 관계만은 아니다. Mermaid는 Markdown-inspired syntax로 다양한 diagram을 렌더링하며, Answer me with HTML은 한 번의 agent 답변을 layout·theme·component와 함께 읽기 좋은 페이지로 패키징한다. 기존 docs가 Mermaid를 지원한다면 Mermaid를 유지하고, 설명 자체를 독립 artifact로 전달해야 할 때 이 도구를 추가하는 방식이 자연스럽다.

## Evaluation Criteria

- **정보 구조**: question 하나를 panel로 나누는 규칙이 team에 맞는가?
- **rendering**: offline single-file 요구와 branding/theme 요구를 충족하는가?
- **maintenance**: source Markdown 및 `am patch` 흐름으로 변경 이력이 이해 가능한가?
- **quality**: lint가 문장 명료성을 돕는가, 도메인 용어를 과도하게 방해하는가?
- **economics**: token 절감뿐 아니라 agent turn, human review, render time을 함께 측정했는가?

## Sources

- https://mermaid.js.org/intro/
- https://mermaid.js.org/config/usage
- https://quarto.org/docs/get-started/hello/text-editor.html
- https://github.com/marp-team/marp
- https://github.com/QingYunA/answer-me-with-html
