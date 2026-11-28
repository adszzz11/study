---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기 — 기준 commit과 질문 만들기

## 준비

특정 도구를 설치하기 전에 공식 프로젝트·버전·실행 방식·데이터 처리 조건을 확인한다. 현재는 제품을 식별할 근거가 없으므로 제품별 설치 명령을 제시하지 않는다.

개념 실습에는 읽기 권한이 있고 구조를 파악할 수 있는 작은 repository를 사용한다. 공개 vault에는 비공개 코드·경로·요약을 옮기지 않는다.

## 실습 순서

1. 기준 commit을 고정하고 하나의 기능을 선택한다.
2. Entry point, 핵심 symbol, 저장소 접근, 외부 호출, 테스트 위치를 직접 정리한다.
3. 코드로 검증할 수 있는 질문 3~5개를 만든다.
4. 텍스트 검색·symbol navigation·사용 가능한 AI 설명을 같은 snapshot에서 비교한다.
5. 중요한 문장을 주장 단위로 나눠 근거 일치 여부를 검토한다.

로컬 Git repository에서 snapshot을 확인하는 예시다. 특정 CodeWiki 명령이 아니다.

```sh
git rev-parse HEAD
git status --short
git show <commit-sha>:<path/to/file>
```

Working tree에 변경이 있으면 HEAD와 파일 내용이 다를 수 있다. 수동 기준 답안과 평가 대상 모두 동일 commit의 내용을 사용한다.

## 질문 예시와 기록표

- 요청의 인증은 어디에서 수행되는가?
- 외부 호출 실패 시 재시도되는가? 설정에 따라 달라지는가?
- 데이터 저장 직전에 어떤 검증을 거치는가?

| 질문 | 수동 기준 답안 | commit·path·symbol | 탐색 방식 | 소요 시간 | 누락·오류 |
|---|---|---|---|---|---|
| 인증 위치 | 실습 후 작성 | 실습 후 작성 | text / symbol / AI | 측정 | 기록 |

## 완료 기준

- [ ] 모든 질문에 기준 답안 또는 답할 수 없는 이유가 있다.
- [ ] 주요 주장마다 동일 commit의 원본 근거가 있다.
- [ ] 구조·실제 동작·설계 의도를 혼동하지 않았다.
- [ ] AI 도구가 없으면 해당 비교를 ‘미실시’로 기록했다.

## 다음 단계

[[tech/devtools/codewiki-analysis/04-learning/02-deep-dive|변경과 검색 품질 평가]] · [[tech/devtools/codewiki-analysis/03-references|제품 식별 체크리스트]] · [[tech/devtools/codewiki-analysis/README|진입점]]

## Sources

- 사용자 제공 dossier: 제품을 식별할 URL과 수집 자료 없음.
- 아래 URL은 일반 개념의 추가 참고자료이며, 특정 CodeWiki의 사양을 입증하지 않는다. 이번 작성에서는 웹 페이지를 열어 검증하지 않았다.
- Git revision 지정: https://git-scm.com/docs/gitrevisions
- Tree-sitter 소개: https://tree-sitter.github.io/tree-sitter/
- Retrieval-Augmented Generation 논문: https://arxiv.org/abs/2005.11401
- ADR 개념: https://adr.github.io/
