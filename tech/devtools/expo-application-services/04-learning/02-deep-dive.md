---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# 심화 학습 — 재현성·호환성·복구

> **검증 범위:** EAS = Expo Application Services라는 잠정 해석이다. ‘Eas’의 정확한 의미와 현재 기능·요금·정책·명령어는 확인이 필요하다. 제공된 자료·URL은 없으며 웹 검색이나 URL 열기는 수행하지 않았다.

## Build 재현성

1. Commit·Lockfile·Toolchain·Build profile·환경 설정을 고정한다.
2. 동일 조건의 Build를 반복하고 성공 여부·시간·로그·Artifact를 비교한다.
3. 차이가 나면 Dependency 해석, 환경변수, Toolchain, 외부 서비스부터 조사한다.

성공 여부와 실행 환경을 재현하는 것과 Binary의 Byte 단위 동일성은 구분한다. 동일 Commit만으로 동일 결과를 보장하지 않는다.

## Update 호환성 실습

다음 표는 제품 설정 예제가 아닌 가상의 설계 모델이다.

| Binary | Native 기능 | Update A: 기존 기능만 사용 | Update B: 새 Native 기능 사용 |
|---|---|---|---|
| A | 기존 기능 | 호환성 테스트 필요 | 대상으로 삼지 않음 |
| B | 기존 기능 + 새 기능 | 호환성 테스트 필요 | 호환성 테스트 필요 |

- Runtime 식별과 배포 분기 설정의 실제 동작을 먼저 확인한다.
- 각 Update가 요구하는 Native 기능과 대상 Binary를 기록한다.
- 배포 전에 호환성 검증을 통과했는지 확인한다.

## 복구 경로 분리

| 사고 유형 | 검토할 복구 경로 | 측정할 항목 |
|---|---|---|
| 잘못된 JavaScript·Asset Update | 수정 Update 또는 제공되는 복구 기능 확인 | 대상 Runtime, 사용자 도달 시간, 재발 방지 |
| 잘못된 Native binary | 수정 Binary 생성·검증·Store 배포 | 심사·설치 지연, 기존 사용자 영향 |

복구·배포 제어 기능의 현재 지원 여부는 미확인이다. 모든 사용자가 즉시 같은 버전을 받는다고 가정하지 않는다.

## 추적성 기록

```text
Commit → Build profile / Toolchain → Artifact
       → Store release → 대상 Runtime → Update
       → 검증 결과 / 사고 기록 / 복구 결과
```

## 완료 기준

- [ ] Build 결과 차이를 조사할 기록이 남아 있다.
- [ ] 호환되지 않는 Binary에 Update를 보내지 않는 사전 검사를 설계했다.
- [ ] Update 사고와 Native 사고의 복구 경로·도달 시간을 별도로 검토했다.

## 연결

[[tech/devtools/expo-application-services/05-projects|실전 프로젝트]] · [[tech/devtools/expo-application-services/README|학습 진입점]]

## Sources

제공 dossier를 기반으로 작성했다. 아래 URL은 후속 확인용 공식 문서 후보이며, 본문을 직접 열어 확인한 근거는 아니다.

- Expo EAS 문서: https://docs.expo.dev/eas/
- EAS Build: https://docs.expo.dev/build/introduction/
- EAS Submit: https://docs.expo.dev/submit/introduction/
- EAS Update: https://docs.expo.dev/eas-update/introduction/
