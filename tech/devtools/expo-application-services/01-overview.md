---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview — What / Why / 특징

> **검증 범위:** EAS = Expo Application Services라는 잠정 해석이다. ‘Eas’의 정확한 의미와 현재 기능·요금·정책·명령어는 확인이 필요하다. 제공된 자료·URL은 없으며 웹 검색이나 URL 열기는 수행하지 않았다.

## What

EAS는 잠정적으로 Expo Application Services를 가리킨다. Expo·React Native 앱의 Native binary 생성, Store 제출, 호환되는 JavaScript·Asset 업데이트를 지원하는 서비스 모음으로 이해한다.

## Why

모바일 배포에서 팀이 직접 관리하는 작업은 다음과 같다.

- iOS·Android별 Build 환경과 Native dependencies
- Signing certificates·Provisioning profiles·Keystore
- 배포 Binary 생성과 App Store·Google Play 제출
- 설치된 Binary에 호환되는 Update와 실패 복구
- Development·Preview·Production 환경 분리

판단 기준은 Build 속도 하나가 아니라 **팀이 운영할 인프라와 절차가 얼마나 줄어드는가**다. 서비스 의존성, 대기 시간, 비용, Credential 정책, 장애 대응 범위의 실제 수준은 아직 판단할 수 없다.

## 핵심 구성

| 구성 | 역할 | 검토 사항 |
|---|---|---|
| EAS Build | 소스·설정으로 Native binary 생성 | Native dependencies, Signing, 환경별 설정 |
| EAS Submit | Binary의 Store 제출 자동화 | 계정 권한, 제출 설정, 심사와의 경계 |
| EAS Update | 호환되는 JavaScript·Asset 배포 | Runtime, 대상 선택, 복구 |
| CLI·프로젝트 설정 | 로컬·자동화 작업 정의와 실행 | 재현성, 인증, Secret 관리 |

```text
Source + Dependencies + Build configuration
                    ↓
             Native binary 생성
                    ↓
              Store 제출·심사
                    ↓
               사용자 설치
                    ↓
      호환되는 JavaScript·Asset 업데이트
```

## 반드시 구분할 경계

Native code나 Native dependency가 바뀌면 새 Binary가 필요할 수 있다. JavaScript만 바뀌어도 설치된 Binary의 Native 기능과 호환되어야 한다. Update는 Store 배포의 완전한 대체 수단이 아니다.

1. **재현성:** Commit 외에 Dependency·Toolchain·환경변수도 결과에 영향을 준다.
2. **호환성:** Update가 대상으로 삼는 Runtime을 명시해야 한다.
3. **추적성:** Commit → Build artifact → Store release → Update의 연결을 기록한다.

Runtime 식별 방식과 배포 분기 설정의 정확한 동작은 공식 문서 확인이 필요하다.

## 다음 학습

[[tech/devtools/expo-application-services/04-learning/01-getting-started|시작하기]] · [[tech/devtools/expo-application-services/README|학습 진입점]]

## Sources

제공 dossier를 기반으로 작성했다. 아래 URL은 후속 확인용 공식 문서 후보이며, 본문을 직접 열어 확인한 근거는 아니다.

- Expo EAS 문서: https://docs.expo.dev/eas/
- EAS Build: https://docs.expo.dev/build/introduction/
- EAS Submit: https://docs.expo.dev/submit/introduction/
- EAS Update: https://docs.expo.dev/eas-update/introduction/
