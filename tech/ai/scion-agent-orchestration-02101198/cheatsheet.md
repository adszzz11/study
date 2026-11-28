---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Scion Cheatsheet

## 개념 빠른 참조

| 용어 | 기억할 점 |
|---|---|
| Harness | 실제 agent의 작업 수행 환경 |
| Agent | Identity·역할·설정·credentials 단위 |
| Project | 보통 repository와 대응하는 namespace |
| Template | System prompt + skills의 blueprint |
| Hub | State·identity·dispatch; 로컬 CLI도 사용 |
| Runtime Broker | Containerized agent provision·실행 |
| Skill Bank | Skills publishing·versioning·resolution |

## 최소 실행 흐름

아래는 README의 Quick Start에 기반한 예제다. 연습용 repository에서 사용하고 설치 버전의 문서와 대조한다.

```sh
brew tap homebrew-scion/scion
brew install homebrew-scion/scion/scion
scion server start
# 브라우저 onboarding 완료 후, 연습용 repository에서:
scion init
scion start my-agent "저장소를 읽고 개선 제안을 보고하라. 파일은 수정하지 마라."
```

- Onboarding: `http://127.0.0.1:8080/onboarding`
- `scion attach`: 실행 중인 agent의 tmux session 연결. 지원 harness와 인자 문법 확인 필요.
- 종료·삭제·message·delegation 명령: 추정하지 말고 설치 버전의 help에서 확인.

## 선택과 주의

| 선택 | 운영 규칙 |
|---|---|
| Shared directories | 파일 소유권·동시 수정 조정 |
| Git worktrees | 분리된 변경·review·통합 담당 |
| Separate clones | 결과 전달·동기화 절차 |
| Hosted Hub | Access·secrets·storage·장애 대응 검증 |

- Local ≠ Hub 없음. Workstation server가 실행의 중심이다.
- Container 분리 ≠ 검증된 보안 격리 보장.
- Workspace 분리 ≠ 자동 merge·충돌 해결 보장.
- 사례 소개 ≠ 정량 생산성·비용 효과 입증.
- Pre-1.0: API·configuration 변경 가능. Google의 공식 지원 제품이 아니다.

## 팀 실행 전 5문항

1. 누가 어떤 작업과 파일을 소유하는가?
2. 근거와 산출물을 어디에 남기는가?
3. 언제 동료 또는 사람에게 도움을 요청하는가?
4. 누가 검토하고 통합 완료를 선언하는가?
5. 어떤 baseline과 비교해 결과를 평가하는가?

## Navigation

- [[tech/ai/scion-agent-orchestration-02101198/README|Scion 학습 진입점]]

## Sources

- https://github.com/GoogleCloudPlatform/scion — README 및 제공된 dossier의 프로젝트 설명.
