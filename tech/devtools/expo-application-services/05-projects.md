---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects — 실전 적용과 비교 실험

> **검증 범위:** EAS = Expo Application Services라는 잠정 해석이다. ‘Eas’의 정확한 의미와 현재 기능·요금·정책·명령어는 확인이 필요하다. 제공된 자료·URL은 없으며 웹 검색이나 URL 열기는 수행하지 않았다.

## 1. 소규모 팀용 배포 파이프라인

- Pull request에서 정적 검사와 테스트를 실행한다.
- 승인된 Commit으로 Preview build를 생성한다.
- 검증 후 Production build와 Store 제출을 진행한다.
- Commit·Artifact·Release 연결 기록을 유지한다.

**산출물:** 환경별 설정표, 승인 흐름, 배포 기록, 실패 조사 절차.

**완료 기준:** 다른 팀원도 동일 절차를 재현하고 실패 지점을 식별한다. 한 번의 배포 성공만으로 완료하지 않는다.

## 2. Update 안전성 검증

- Runtime별 테스트 앱과 호환성 표를 작성한다.
- JavaScript 변경과 Native 변경 사례를 분리한다.
- 잘못된 배포 대상 선택을 막는 사전 검사를 설계한다.
- Update 실패와 복구 시나리오를 검증한다.

**산출물:** 호환성 표, 사전 검사 조건, 사고별 복구 절차와 도달 시간 기록.

**완료 기준:** 비호환 대상을 배제하는 근거와 각 사고의 복구 검증 결과가 있다. 실제 배포 제어·복구 기능은 지원 여부 확인 후 사용한다.

## 3. 관리형 서비스와 자체 CI 비교

동일 앱·동일 Commit으로 EAS와 자체 CI 구성을 비교한다.

| 측정 항목 | 기록 방법 |
|---|---|
| 초기 설정 시간 | 작업 시작부터 재현 가능한 첫 성공까지 |
| Build 시간 | 대기 시간과 실행 시간을 분리 |
| 실패 분석 시간 | 실패 인지부터 원인 식별까지 |
| Credential 부담 | 보관·권한·교체 작업 기록 |
| 비용 | 현재 요금과 실제 사용량으로 계산 |

**완료 기준:** 동일 조건의 측정 자료와 운영 부담 비교표가 있다. 자료가 없으면 더 빠르거나 저렴하다고 결론 내리지 않는다.

## 연결

[[tech/devtools/expo-application-services/02-ecosystem|비교 관점]] · [[tech/devtools/expo-application-services/04-learning/02-deep-dive|검증 설계]] · [[tech/devtools/expo-application-services/README|학습 진입점]]

## Sources

제공 dossier를 기반으로 작성했다. 아래 URL은 후속 확인용 공식 문서 후보이며, 본문을 직접 열어 확인한 근거는 아니다.

- Expo EAS 문서: https://docs.expo.dev/eas/
- EAS Build: https://docs.expo.dev/build/introduction/
- EAS Submit: https://docs.expo.dev/submit/introduction/
- EAS Update: https://docs.expo.dev/eas-update/introduction/
