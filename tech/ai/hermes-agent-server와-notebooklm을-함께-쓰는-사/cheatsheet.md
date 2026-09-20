---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Hermes Agent Server와 NotebookLM — Cheatsheet

> [[README|목차로 돌아가기]]

## 한눈에 보는 역할

| 무엇을 저장하는가 | 어디에 두는가 | 규칙 |
|---|---|---|
| 현재 작업 context | Hermes session | task가 끝나면 축소 |
| 반복되는 선호·검증된 안정적 사실 | Hermes memory / external provider | `memory.write_approval`으로 검토 |
| 원문·claim·인용·오답·다음 학습 | Google Doc Study Note | provenance와 revision을 남김 |
| source 기반 질의·quiz·briefing | NotebookLM | 결과를 원문 노트에 환류 |

## Study Note 최소 template

```markdown
# <Topic> — Study Note

Updated: YYYY-MM-DD
Scope: <이 문서가 답할 질문>
Version: 0.1
Sensitivity: personal | internal | restricted
Confidence: high | medium | low

## Source URLs
- https://...

## Claims
### <Claim>
- Evidence: <source 직접 사실 요약>
- Source: https://...
- Confidence: medium

## Hermes interpretation
- <가설 또는 연결. source 직접 주장과 구분>

## Open questions
- <검증하지 못한 질문>

## Questions / mistakes
- <복습 중 틀린 내용>

## Change log
- YYYY-MM-DD: <변경 이유>
```

## Publish 전 60초 점검

- [ ] claim마다 원문 URL이 있는가?
- [ ] source 사실과 Hermes interpretation이 분리됐는가?
- [ ] URL이 실제 원문을 가리키는가?
- [ ] `Updated`, `Scope`, `Confidence`, `Open questions`가 본문에 있는가?
- [ ] footnote/comments에만 중요한 내용이 있지 않은가?
- [ ] secret, access token, 개인·민감 정보가 없는가?
- [ ] Drive 대상 folder/Doc ID와 변경 diff를 확인했는가?

## NotebookLM source 점검

| 항목 | 확인 |
|---|---|
| 권장 source | 주제별 living Google Doc |
| 지원 형식 예시 | Google Docs, Markdown, PDF, DOCX, TXT, CSV, Slides, Sheets, Web URL, YouTube |
| Free 한도 안내 | source당 최대 50만 단어 또는 upload 200MB, notebook당 50 source |
| auto-sync | Drive source에서 원본 변경 반영 여부를 계정에서 확인 |
| import 주의 | Google Docs footnote/comments는 import되지 않음 |
| 권한 주의 | Drive access 상실 또는 원본 삭제 시 source 사용 불가 |

## Hermes API Server 보안

```text
기본: loopback binding + Bearer key + narrow CORS
원칙: 필요한 MCP tool만 연결 + memory/document write 승인
금지: terminal 권한 agent endpoint를 인증 없이 public exposure
```

## 선택 빠른 판단

| 요구 | 선택 |
|---|---|
| 개인 학습, 갱신 가능한 문서 | Google Docs + NotebookLM auto-sync |
| 한 번만 읽을 snapshot | Markdown/PDF upload |
| agent의 장기 recall | Hermes external memory provider |
| agent가 knowledge를 양방향 API로 써야 함 | Custom RAG + vector DB + MCP |
| 조직 단위 source 자동 ingest | Gemini Notebook Enterprise API 검토 |

## Sources

- https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/api-server.md
- https://hermes-agent.nousresearch.com/docs/user-guide/features/memory
- https://support.google.com/gemininotebook/answer/16215270?co=GENIE.Platform%3DDesktop&hl=en-6
- https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks-sources
