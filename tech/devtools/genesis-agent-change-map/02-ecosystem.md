---
date: 2026-11-25
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem — 기존 리뷰 도구와의 관계

## 역할 비교

수집 자료에는 특정 경쟁 제품의 기능 비교가 없다. 아래는 직접 비교 baseline과 일반적인 검토 방식의 역할 비교다.

| 접근 | 주로 답하는 질문 | Genesis와의 관계 | 한계·확인 사항 |
|---|---|---|---|
| Claude Code·Codex 단독 리뷰 | 무엇이 바뀌었고 위험한가? | Benchmark의 직접 baseline | 해당 표본에서 검출력 부족 테스트 누락과 false alarm이 더 많았음 |
| Genesis + coding agent | 어느 flow의 변경이며 테스트 근거는 무엇인가? | 인용 검증과 시각화 추가 | 의미·위험 해석은 agent 의존 |
| Git diff 리뷰 | 어떤 코드 줄이 바뀌었나? | Business flow 설명과 실제 변경 대조 | Genesis 결과와 diff를 함께 읽어야 함 |
| 테스트 실행·coverage 측정 | 통과하는가, 어떤 코드가 실행됐나? | 정적 테스트 읽기 보완 | Genesis 자체는 실행·runtime coverage 측정을 하지 않음 |
| Static analysis·rule 검사 | 정해진 규칙에 위배되는가? | 별도의 위험 근거 제공 | Genesis risk 설명에는 rule engine이 없음 |

## 선택 기준

1. 줄 단위 변경은 diff로 확인한다.
2. 사용자 경로와 변경 의미는 Genesis 결과로 정리한다.
3. Assertion이 해당 오류를 잡는지 직접 읽는다.
4. 실제 테스트와 필요한 static analysis를 별도로 수행한다.

이는 권장 학습 절차이며 Genesis가 자동 수행하는 pipeline이라는 뜻은 아니다.

## 라이선스와 성숙도

Apache-2.0으로 제공되며 bundled component에는 각각의 라이선스가 적용된다. 수집 화면의 70 stars·10 forks·146 commits는 당시 snapshot이다. 현재 수치나 품질·성숙도 보증으로 해석하지 않는다.

## 연결

[[tech/devtools/genesis-agent-change-map/01-overview|Benchmark와 한계]] · [[tech/devtools/genesis-agent-change-map/README|학습 경로]]

## Sources

- https://github.com/GenesisAgentInfra/genesis — 제공된 dossier의 GitHub 수집 본문 근거.
- https://raw.githubusercontent.com/GenesisAgentInfra/genesis/main/docs/install.md — 본문에서 안내한 설치 가이드. 내용은 별도 열람하지 않음.
