---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# References — 출처와 확인할 정보

## 증거 범위

제공된 dossier에는 특정 제품의 공식 URL, 버전, 수집 자료가 없다. 따라서 CodeWiki의 운영 주체·설치 명령·가격·라이선스·지원 언어를 이 노트로 확정할 수 없다. 이름이 같은 도구를 동일 제품으로 간주하지 않는다.

## 제품 식별 체크리스트

| 확인 항목 | 필요한 자료 | 현재 상태 |
|---|---|---|
| 정체·버전 | 공식 사이트, repository, release | 확인 필요 |
| 지원 범위 | 언어·repository 유형·배포 방식 문서 | 확인 필요 |
| 데이터 처리 | 전송·보관·학습 이용·삭제 조건 | 확인 필요 |
| 접근 권한 | repository ACL과 파생 결과 권한 문서 | 확인 필요 |
| 비용·권리 | 가격표, 라이선스 원문 | 확인 필요 |

## 자료 읽는 순서

1. 공식 URL과 repository 소유자를 대조해 제품을 식별한다.
2. 버전과 문서 확인 날짜를 기록한다.
3. 기능 주장은 공식 문서와 재현 실험을 구분해 적는다.
4. 아래 일반 참고자료로 revision, parser, RAG, ADR 개념을 보충한다. 제품 기능의 증거로 인용하지 않는다.

## 근거 기록 양식

```text
주장:
분류: 확인한 사실 / 추론 / 확인 필요
출처 URL 또는 repository:
대상 버전 또는 commit SHA:
path / symbol:
근거가 지지하는 범위와 한계:
확인 날짜:
```

## 연결

[[tech/devtools/codewiki-analysis/04-learning/01-getting-started|제품 식별 후 시작하기]] · [[tech/devtools/codewiki-analysis/README|진입점]]

## Sources

- 사용자 제공 dossier: 제품을 식별할 URL과 수집 자료 없음.
- 아래 URL은 일반 개념의 추가 참고자료이며, 특정 CodeWiki의 사양을 입증하지 않는다. 이번 작성에서는 웹 페이지를 열어 검증하지 않았다.
- Git revision 지정: https://git-scm.com/docs/gitrevisions
- Tree-sitter 소개: https://tree-sitter.github.io/tree-sitter/
- Retrieval-Augmented Generation 논문: https://arxiv.org/abs/2005.11401
- ADR 개념: https://adr.github.io/
