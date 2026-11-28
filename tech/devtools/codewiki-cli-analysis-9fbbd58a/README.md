---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# codewiki-cli: Agent를 위한 선택적 저장소 문서 조회 도구

> **한 줄 정의**: Google CodeWiki의 저장소 문서를 검색하고, 섹션 목록에서 필요한 Markdown만 선택해 읽도록 설계된 비공식 CLI다.

## Overview

문서 전체를 Agent context에 넣기 전에 `sections`로 ID·제목·요약·anchor를 확인하고, `content`로 필요한 본문만 읽는다. CodeWiki와 터미널·Agent 사이의 **조회 계층**이며, 자체 문서 생성이나 소스 indexing·embedding·LLM 추론 엔진으로 볼 근거는 없다.

- 기본 흐름: `search` → `sections` → `content` → 필요하면 `--chunks`.
- 출력은 선택적이지만 최초 요청은 **full wiki fetch** 후 저장소별 JSON cache를 만든다.
- 개인용 Unofficial 도구이며 undocumented RPC 변경에 영향을 받을 수 있다.

## Learning Path

- [ ] [[tech/devtools/codewiki-cli-analysis-9fbbd58a/01-overview|Overview]] — 역할, 구조, 제약 이해
- [ ] [[tech/devtools/codewiki-cli-analysis-9fbbd58a/02-ecosystem|Ecosystem]] — 대안 작업 방식과 비교
- [ ] [[tech/devtools/codewiki-cli-analysis-9fbbd58a/04-learning/01-getting-started|시작하기]] — 로컬 build와 첫 조회
- [ ] [[tech/devtools/codewiki-cli-analysis-9fbbd58a/04-learning/02-deep-dive|Deep Dive]] — cache·chunk·ID 수명 실습
- [ ] [[tech/devtools/codewiki-cli-analysis-9fbbd58a/05-projects|Projects]] — 적용 프로젝트 설계
- [ ] [[tech/devtools/codewiki-cli-analysis-9fbbd58a/03-references|References]] — 근거와 미확인 항목 확인
- [ ] [[tech/devtools/codewiki-cli-analysis-9fbbd58a/cheatsheet|Cheatsheet]] — 명령 빠른 참조
- [ ] [[tech/devtools/codewiki-cli-analysis-9fbbd58a/README|학습 진입점 다시 보기]] — 적합한 사용 시나리오 정리

## When To Use

- CodeWiki에 문서가 있는 저장소를 탐색하거나 onboarding할 때.
- Agent 질문에 관련된 문서만 context에 넣고 싶을 때.
- 터미널에서 반복 조회하며 local cache를 재사용할 때.

## When Not To Use

- 자체 문서 생성, 소스 indexing 또는 독립적인 AI 코드 분석 엔진이 필요할 때.
- 최초 네트워크 전송도 섹션 단위로 제한해야 할 때.
- 안정적인 공개 API 계약이나 영구 section ID가 필수인 자동화.
- 문서만으로 실제 구현의 정확성을 보장해야 하는 작업.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/codewiki-cli-analysis-9fbbd58a/01-overview|codewiki-cli의 조회 구조와 한계]] — 이 study의 관련 tech 노트


## Sources

- https://github.com/miinhho/codewiki-cli — 제공된 dossier의 README 기반 정리. 실습 및 성능 검증은 미실행.
