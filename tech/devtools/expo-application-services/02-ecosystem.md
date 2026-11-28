---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem — 배포 접근 방식 비교

> **검증 범위:** EAS = Expo Application Services라는 잠정 해석이다. ‘Eas’의 정확한 의미와 현재 기능·요금·정책·명령어는 확인이 필요하다. 제공된 자료·URL은 없으며 웹 검색이나 URL 열기는 수행하지 않았다.

## 접근 방식 비교

최신 기능·가격 비교가 아닌 운영 방식의 비교다. 현재 지원 범위와 연동 방식은 별도 확인한다.

| 접근 방식 | 대표 도구·조합 | 적합한 상황 | 검토할 부담 |
|---|---|---|---|
| Expo 중심 관리형 서비스 | EAS | Expo·React Native 배포 운영 통합 | 서비스 의존성, 지원 범위, 사용량 비용 |
| 범용 CI 직접 구성 | GitHub Actions 등 + Fastlane | 기존 CI 통합과 세부 제어 | Runner, Signing, Cache, Toolchain 유지보수 |
| 모바일 중심 CI/CD | Bitrise, Codemagic 등 | 모바일 Workflow와 여러 프로젝트 운영 | 플랫폼별 설정, 비용, 이전 난이도 |
| 로컬 Native 도구 중심 | Xcode, Gradle | 초기 검증과 직접적인 Native 제어 | 환경 편차, 수동 작업, 팀 확장성 |

## 함께 쓰는 구성

범용 CI에서 테스트·승인을 수행하고 EAS 작업을 호출하는 구성을 고려할 수 있다. 구체적인 인증 방식·권한·연동 절차는 검증 전이다.

```text
Pull request → 정적 검사·테스트 → 승인
                                  ↓
                           EAS Build / Submit
```

## 비교 실험의 공통 조건

- 동일 앱·동일 Commit과 유사한 Build 환경을 사용한다.
- 월간 배포량, 동시 실행 요구, Native customization을 고정한다.
- Credential 보관·접근·교체 정책과 장애 대응 책임을 비교한다.
- 초기 설정 시간, 대기 시간, 실행 시간, 실패 분석 시간을 나누어 기록한다.
- 현재 요금과 실제 사용량을 확보한 뒤 비용을 계산한다.

현재 근거로 어떤 방식이 더 빠르거나 저렴하다고 결론 낼 수 없다.

## 연결

[[tech/devtools/expo-application-services/05-projects|비교 실험 프로젝트]] · [[tech/devtools/expo-application-services/README|학습 진입점]]

## Sources

제공 dossier를 기반으로 작성했다. 아래 URL은 후속 확인용 공식 문서 후보이며, 본문을 직접 열어 확인한 근거는 아니다.

- Expo EAS 문서: https://docs.expo.dev/eas/
- EAS Build: https://docs.expo.dev/build/introduction/
- EAS Submit: https://docs.expo.dev/submit/introduction/
- EAS Update: https://docs.expo.dev/eas-update/introduction/
