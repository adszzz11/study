---
date: 2026-11-18
tags: [tech, devtools, expo, mobile, cicd]
type: tech-tool-study
status: researched
---

# 전체 구조와 책임 경계

| 단계 | 입력과 산출물 | 확인할 것 |
|---|---|---|
| Build | 소스·빌드 설정 → 서명된 Android/iOS 바이너리 | 플랫폼, profile, 인증서, 빌드 번호 |
| Submit | 바이너리 → 스토어 업로드 | 제출 대상 앱과 track, 처리 결과 |
| Update | JS·asset → 호환 설치본용 업데이트 | channel, runtimeVersion, platform |
| Workflows | YAML → 빌드·테스트·제출 등의 작업 연결 | 트리거, 의존 순서, 실패 시 중단 |

Build는 Expo/React Native 프로젝트를 위한 호스팅 빌드 환경이며 서명 정보를 직접 제공하거나 서비스에 관리를 맡길 수 있다. 개발용 빌드와 내부 배포, 스토어용 빌드는 목적이 다르므로 같은 산출물로 취급하지 않는다. [Build 소개](https://docs.expo.dev/build/introduction/)

Submit 성공은 스토어 공개 성공과 다르다. iOS 업로드는 처리 후 TestFlight에서 사용하며, App Store 출시는 메타데이터·스크린샷과 심사 단계를 거친다. Android는 선택한 track 및 release 설정에 따라 배포 효과가 달라진다. Android 첫 제출 전에는 Play Console에 앱을 만들고 제출용 서비스 계정을 설정해야 한다. 현재 공식 안내는 기본 `eas submit`이 새 앱의 첫 릴리스를 internal testing track에 만들 수 있다고 설명하며, 수동 첫 업로드는 선택 사항이다. [Android 제출 전제](https://docs.expo.dev/submit/android/) [스토어 제출](https://docs.expo.dev/deploy/submit-to-app-stores/)

## 배포 경로

```text
검토한 소스 → Build → 내부 테스트 → Submit → 스토어 심사·출시
호환되는 JS·asset 변경 → Update → 선택한 채널의 호환 설치본
```

이는 설계 흐름이다. 테스트 통과, 배포 승인, 스토어 승인이라는 서로 다른 판단을 하나의 성공 표시로 합치지 않는다.

## 관련 노트

- [[tech/devtools/expo-services-mobile-cicd/README|연구 목차]]
