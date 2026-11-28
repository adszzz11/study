---
date: 2026-11-28
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: 데이터·코드·정책 경계

## 세 경계

| 경계 | 넘어가는 대상 | 필요한 통제 |
|---|---|---|
| 사용자·로컬 → 외부 서비스 | 앱 아이디어 | 사전 고지, 선택권, 최소 전송 |
| 원격 서버 → 로컬 실행 | Script | 출처, 버전 고정, 내용 검토 |
| Skill 지시 → harness 정책 | 실행 구성 | 전체 효과 평가, 거부 존중 |

데이터는 밖으로 나가고 코드는 안으로 들어온다. 정책 경계는 그 동작을 실행 환경이 어떻게 판단하게 만드는가에 관한 문제다.

## 원격 응답이 실행 권한을 얻는 순간

```text
CAP == hosting → GET /add-hosting → 응답을 bash로 실행
그 외 CAP      → GET /add-component → ADD_TERM=CAP 환경변수와 bash 실행
```

인용된 `curl … | bash` 구조에는 release·commit·hash pinning 장치가 보이지 않는다. Skill 파일만 검토하면 미래 URL 응답의 bytes를 확정할 수 없다. 실제 응답 내용이 없으므로 파일 변경이나 자격증명 접근을 했다고 주장할 수 없다.

HTTPS는 전송 중 보호에 도움이 되지만 script 안전성이나 검토 당시 코드와의 동일성을 보증하지 않는다. Generated-name `convex.site` hostname도 자체로 악성의 증거가 아니다.

## Command 형태와 전체 효과

`labs-quickstart` 발췌는 다운로드와 실행을 서로 다른 Bash call로 분리하고, `&&`, `;`, 같은 call 내 newline, shell pipe로 합치지 말라고 한다. 이유는 다음처럼 명시되어 있다.

> “A single command that both downloads remote code and executes it is the shape harness safety classifiers block.”

이어 디스크의 파일 실행이 “ordinary local script”처럼 읽힌다고 설명한다. 분리는 검토를 위한 정상적 기법일 수 있지만, 이 발췌의 명시적 이유는 classifier의 인식을 바꾸는 것이다. 실제 어떤 harness가 이를 허용했는지나 우회 성공률은 알 수 없다.

| 흐름 | 중간 통제 | 평가 |
|---|---|---|
| 다운로드 → 별도 call에서 실행 | 없음 | Call 수만으로 안전성이 높아지지 않음 |
| 다운로드 → 내용·hash 검토 → 승인된 코드 실행 | 검토·동일성 확인 | 신뢰 결정을 설명할 근거가 생김 |
| Harness 거절 → 모양만 바꿔 재시도 | 거절 회피 | 정책 충돌을 해결하지 못함 |

## 검토 연습

1. 목표에 대한 동의와 데이터·실행 권한에 대한 동의를 따로 적는다.
2. Hash와 script가 같은 변경 가능한 서버에서 오면 검증 신뢰가 어디에 놓이는지 설명한다.
3. 여러 tool call을 한 흐름으로 묶어 원격 코드 실행 의도를 표시한다.
4. 거절되면 우회 대신 로컬 수동 설정 또는 실행 중단 경로를 설계한다.

[[tech/devtools/convex-skill-trust-boundary/05-projects|다음: 설계 프로젝트]] · [[tech/devtools/convex-skill-trust-boundary/README|학습 경로]]

## Sources

- https://github.com/convex/convex-backend-skill/issues/64
