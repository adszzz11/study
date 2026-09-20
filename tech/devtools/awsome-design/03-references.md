---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# awesome-design-md — References

> [[02-ecosystem|이전: Ecosystem]] · [[README|목차로 돌아가기]] · [[04-learning/01-getting-started|다음: Getting Started]]

## 핵심 자료

| 자료 | 읽을 내용 | 신뢰 수준/주의 |
|---|---|---|
| [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) | category별 reference 목록, 각 `DESIGN.md`와 preview | collection 자체의 primary source지만 브랜드 공식 system은 아님 |
| [Google DESIGN.md repository](https://github.com/google-labs-code/design.md) | format, schema, CLI reference, example | 공식 format source, 현재 `alpha` |
| [Google Labs announcement](https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-design-md/) | 공개 배경과 Stitch 맥락 | 공식 발표 |
| [W3C Design Tokens Community Group](https://www.w3.org/community/design-tokens/) | Design Tokens Specification 2025.10 stable 발표와 표준 활동 | vendor-neutral token 표준의 공식 source |
| [Vercel DESIGN.md raw](https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md/vercel/DESIGN.md) | YAML tokens, Geist typography, 4px spacing, component mappings와 prose | collection의 구체적 사례; Vercel 공식 문서로 오인하지 않기 |

## Collection 탐색 포인트

공개 README 기준 약 73개 분석은 다음 범주를 포함한다.

- **AI/LLM**: Claude, Mistral, Ollama, Runway, xAI
- **Developer tools**: Cursor, Expo, Raycast, Vercel, Warp
- **Backend/DevOps**: ClickHouse, HashiCorp, MongoDB, Sentry, Supabase
- **SaaS**: Linear, Notion, Mintlify, Resend
- **Design**: Figma, Framer, Miro, Webflow
- **기타**: fintech, commerce, media, automotive, retro web

reference를 고를 때 브랜드 이름보다 아래 속성을 비교한다.

| 속성 | 확인 질문 |
|---|---|
| Density | data-heavy 화면인가, marketing 중심인가? |
| Typography | content, dashboard, code 중 무엇을 우선하는가? |
| Color role | accent가 action, status, decoration 중 어디에 쓰이는가? |
| Depth | border, shadow, surface layering을 어떻게 조합하는가? |
| Spacing | base unit과 dense/comfortable mode가 제품에 맞는가? |
| Motion | transition이 feedback인가, 장식인가? |

## 구분해야 할 동명 저장소

- [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md): 이 노트의 대상. AI agent용 `DESIGN.md` reference collection.
- [gztchan/awesome-design](https://github.com/gztchan/awesome-design): 일반 UI/UX resource link collection. 철자는 비슷하지만 목적과 구조가 다르다.

## 읽기 순서

1. collection README에서 제품 성격이 비슷한 reference 2~3개를 고른다.
2. `preview.html`과 `preview-dark.html`로 시각적 결과를 비교한다.
3. 해당 `DESIGN.md`의 YAML token과 Markdown rationale이 서로 맞는지 읽는다.
4. Google 공식 format과 schema를 확인해 지원되는 key와 section order를 구분한다.
5. W3C DTCG 문서로 export 이후의 interchange boundary를 이해한다.
6. reference를 복사하지 말고 product constraint, accessibility, brand/IP 조건에 맞게 재작성한다.

## 검증 체크리스트

- [ ] collection reference와 공식 brand design system을 구분했는가?
- [ ] token 값의 출처와 관찰 시점을 기록했는가?
- [ ] proprietary font, logo, photo, trademark 사용 권한을 별도로 확인했는가?
- [ ] 외부 `DESIGN.md`의 명령과 URL을 untrusted input으로 review했는가?
- [ ] official schema와 CLI version을 고정했는가?
- [ ] contrast 외 keyboard, focus, semantics, motion을 별도 검증하는가?

## Sources

- https://github.com/VoltAgent/awesome-design-md
- https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md/vercel/DESIGN.md
- https://github.com/google-labs-code/design.md
- https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-design-md/
- https://www.w3.org/community/design-tokens/
- https://github.com/gztchan/awesome-design

